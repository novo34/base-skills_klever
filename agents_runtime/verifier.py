from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from events.runtime import OperationalEvent
from models.gateway import ModelGateway
from models.gateway_contract import ModelRequest
from notifications.event_router import NotificationEventRouter
from verification.collector_service import CollectorService
from verification.collectors import VerificationCollectors, VerificationContext
from verification.report import build_report
from verification.runtime import VerificationResult
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
        collectors: VerificationCollectors | None = None,
    ):
        self.gateway = gateway
        self.verification = verification or VerificationService()
        self.event_router = event_router
        self.collector_service = (
            CollectorService(collectors) if collectors is not None else None
        )

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
        context: VerificationContext,
    ) -> dict[str, Any]:
        if self.collector_service is None:
            raise RuntimeError("verification_collectors_required")
        if context.task_id != task.task_id:
            raise RuntimeError("verification_context_task_mismatch")
        if context.project_id != task.project_id:
            raise RuntimeError("verification_context_project_mismatch")

        bundle = self.collector_service.collect(
            context=context,
            triggers=set(task.triggers),
            requirement_ids=task.requirement_ids,
        )

        if bundle.blocked:
            result = VerificationResult(
                status="BLOCKED",
                failures=tuple(
                    f"collector_blocked:{name}"
                    for name in bundle.blocked_collectors
                ),
                evidence=bundle.evidence,
            )
        else:
            result = self.verification.evaluate(
                triggers=set(task.triggers),
                evidence=bundle.evidence,
            )

        if result.status in {"FAILED", "BLOCKED"} and self.event_router is not None:
            self.event_router.handle(OperationalEvent(
                event_id=f"{task.task_id}-VERIFICATION-{result.status}",
                project_id=task.project_id,
                event_type="VERIFICATION_FAILED",
                target_type="task",
                target_id=task.task_id,
                title=f"Verification {result.status.lower()}",
                message="Independent verification did not reach VERIFIED.",
                metadata={
                    "status": result.status,
                    "failures": list(result.failures),
                },
            ))

        return {
            "result": result,
            "report": build_report(task.task_id, result),
            "collector_results": bundle.results,
        }
