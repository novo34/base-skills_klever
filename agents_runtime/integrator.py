from __future__ import annotations

from dataclasses import dataclass

from agents_runtime.conflicts import IntegrationConflict
from agents_runtime.handoff import AgentHandoff, validate_handoff


@dataclass(frozen=True)
class IntegrationDecision:
    task_id: str
    status: str
    reason: str
    developer_handoff_id: str
    verifier_handoff_id: str


class IntegratorAgent:
    def evaluate_adaptive(
        self,
        *,
        developer_handoff: AgentHandoff,
        verifier_handoff: AgentHandoff,
        verification_status: str,
        human_approved: bool,
        approved_blueprint_revision: int,
        delivered_blueprint_revision: int,
        approved_promotion_scope: tuple[str, ...],
        requested_promotion_scope: tuple[str, ...],
        conflicts: tuple[IntegrationConflict, ...] = (),
    ) -> IntegrationDecision:
        if approved_blueprint_revision < 1:
            raise ValueError("approved_blueprint_revision_required")
        if delivered_blueprint_revision != approved_blueprint_revision:
            return IntegrationDecision(
                task_id=developer_handoff.task_id,
                status="BLOCKED",
                reason="blueprint_revision_mismatch",
                developer_handoff_id=developer_handoff.handoff_id,
                verifier_handoff_id=verifier_handoff.handoff_id,
            )

        approved_scope = set(approved_promotion_scope)
        requested_scope = set(requested_promotion_scope)
        if not requested_scope or not requested_scope.issubset(approved_scope):
            return IntegrationDecision(
                task_id=developer_handoff.task_id,
                status="BLOCKED",
                reason="promotion_scope_not_approved",
                developer_handoff_id=developer_handoff.handoff_id,
                verifier_handoff_id=verifier_handoff.handoff_id,
            )

        return self.evaluate(
            developer_handoff=developer_handoff,
            verifier_handoff=verifier_handoff,
            verification_status=verification_status,
            human_approved=human_approved,
            conflicts=conflicts,
        )

    def evaluate(
        self,
        *,
        developer_handoff: AgentHandoff,
        verifier_handoff: AgentHandoff,
        verification_status: str,
        human_approved: bool,
        conflicts: tuple[IntegrationConflict, ...] = (),
    ) -> IntegrationDecision:
        for handoff in (developer_handoff, verifier_handoff):
            ok, failures = validate_handoff(handoff)
            if not ok:
                raise ValueError(",".join(failures))

        if developer_handoff.task_id != verifier_handoff.task_id:
            raise ValueError("handoff_task_mismatch")

        if developer_handoff.from_agent == verifier_handoff.from_agent:
            raise ValueError("developer_and_verifier_must_be_distinct")

        unresolved = [
            conflict
            for conflict in conflicts
            if conflict.status != "RESOLVED"
        ]
        if unresolved:
            return IntegrationDecision(
                task_id=developer_handoff.task_id,
                status="BLOCKED",
                reason="integration_conflict_unresolved",
                developer_handoff_id=developer_handoff.handoff_id,
                verifier_handoff_id=verifier_handoff.handoff_id,
            )

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
