from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from events.runtime import OperationalEvent
from models.gateway import ModelGateway
from models.gateway_contract import ModelRequest
from notifications.event_router import NotificationEventRouter
from verification.evidence_builder import EvidenceBuilder
from verification.report import build_report
from verification.service import VerificationService


@dataclass(frozen=True)
class VerifierTask:
    task_id: str
    project_id: str
    requirement_ids: tuple[str, ...]
    acceptance_criteria: tuple[str, ...]
    triggers: tuple[str, ...]
    provider: str
    model: str
    fallback_chain: tuple[tuple[str, str], ...] = ()


class VerifierAgent:
    def __init__(
        self,
        *,
        gateway: ModelGateway,
        verification: VerificationService | None = None,
        event_router: NotificationEventRouter | None = None,
    ):
        self.gateway = gateway
        self.verification = verification or VerificationService()
        self.evidence_builder = EvidenceBuilder()
        self.event_router = event_router

    def build_prompt(self, task: VerifierTask, diff_summary: str) -> str:
        criteria = "\n".join(f"- {item}" for item in task.acceptance_criteria)
        requirements = ", ".join(task.requirement_ids)
        return (
            f"Verify task {task.task_id}.\n"
            f"Requirements: {requirements}\n"
            f"Acceptance criteria:\n{criteria}\n"
            f"Diff summary:\n{diff_summary}\n"
            "Review independently. Do not propose code edits. "
            "Return verification findings only."
        )

    def inspect(
        self,
        task: VerifierTask,
        *,
        diff_summary: str,
    ) -> dict[str, Any]:
        response = self.gateway.execute(
            ModelRequest(
                request_id=f"MODEL-{task.task_id}-VERIFY",
                project_id=task.project_id,
                task_id=task.task_id,
                agent_role="verifier",
                provider=task.provider,
                model=task.model,
                prompt=self.build_prompt(task, diff_summary),
            ),
            fallback_chain=task.fallback_chain,
        )
        return {
            "provider": response.provider,
            "model": response.model,
            "findings": response.content,
            "usage": response.usage,
        }

    def evaluate(
        self,
        task: VerifierTask,
        *,
        ci_status: str,
        unit_exit_code: int | None,
        integration_exit_code: int | None,
        e2e_exit_code: int | None,
        diff_reviewed: bool,
        backend_verified: bool = False,
        frontend_verified: bool = False,
        database_verified: bool = False,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        evidence = self.evidence_builder.from_sources(
            requirement_ids=list(task.requirement_ids),
            ci_status=ci_status,
            unit_exit_code=unit_exit_code,
            integration_exit_code=integration_exit_code,
            e2e_exit_code=e2e_exit_code,
            diff_reviewed=diff_reviewed,
            backend_verified=backend_verified,
            frontend_verified=frontend_verified,
            database_verified=database_verified,
            notes=notes,
        )
        result = self.verification.evaluate(
            triggers=set(task.triggers),
            evidence=evidence,
        )
        if result.status == "FAILED" and self.event_router is not None:
            self.event_router.handle(OperationalEvent(
                event_id=f"{task.task_id}-VERIFICATION-FAILED",
                project_id=task.project_id,
                event_type="VERIFICATION_FAILED",
                target_type="task",
                target_id=task.task_id,
                title="Verification failed",
                message="Independent verification found blocking failures.",
                metadata={"failures": list(result.failures)},
            ))
        return {
            "result": result,
            "report": build_report(task.task_id, result),
        }
