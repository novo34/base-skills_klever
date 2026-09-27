from __future__ import annotations

from dataclasses import dataclass

from agents_runtime.handoff import AgentHandoff, validate_handoff


@dataclass(frozen=True)
class IntegrationDecision:
    task_id: str
    status: str
    reason: str
    developer_handoff_id: str
    verifier_handoff_id: str


class IntegratorAgent:
    def evaluate(
        self,
        *,
        developer_handoff: AgentHandoff,
        verifier_handoff: AgentHandoff,
        verification_status: str,
        human_approved: bool,
    ) -> IntegrationDecision:
        for handoff in (developer_handoff, verifier_handoff):
            ok, failures = validate_handoff(handoff)
            if not ok:
                raise ValueError(",".join(failures))

        if developer_handoff.task_id != verifier_handoff.task_id:
            raise ValueError("handoff_task_mismatch")

        if developer_handoff.from_agent == verifier_handoff.from_agent:
            raise ValueError("developer_and_verifier_must_be_distinct")

        if verification_status != "VERIFIED":
            return IntegrationDecision(
                task_id=developer_handoff.task_id,
                status="BLOCKED",
                reason="verification_required",
                developer_handoff_id=developer_handoff.handoff_id,
                verifier_handoff_id=verifier_handoff.handoff_id,
            )

        if not human_approved:
            return IntegrationDecision(
                task_id=developer_handoff.task_id,
                status="AWAITING_HUMAN",
                reason="human_approval_required",
                developer_handoff_id=developer_handoff.handoff_id,
                verifier_handoff_id=verifier_handoff.handoff_id,
            )

        return IntegrationDecision(
            task_id=developer_handoff.task_id,
            status="READY_TO_MERGE",
            reason="all_gates_passed",
            developer_handoff_id=developer_handoff.handoff_id,
            verifier_handoff_id=verifier_handoff.handoff_id,
        )
