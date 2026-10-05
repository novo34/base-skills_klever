from __future__ import annotations

from approvals.runtime import Approval, decide, request_approval
from events.runtime import OperationalEvent
from notifications.event_router import NotificationEventRouter
from staging.evidence_store import StagingEvidenceStore
from staging.readiness import evaluate_readiness
from staging.runtime import Promotion, StagingEnvironment
from staging.service import StagingService


class StagingPipeline:
    def __init__(
        self,
        staging: StagingService | None = None,
        event_router: NotificationEventRouter | None = None,
        evidence_store: StagingEvidenceStore | None = None,
    ):
        self.staging = staging or StagingService()
        self.event_router = event_router
        self.evidence_store = evidence_store

    def _require_current_evidence(
        self,
        *,
        evidence_id: str | None,
        task_id: str,
        project_id: str,
        staging_url: str,
        staging_commit: str,
    ):
        if not evidence_id:
            raise RuntimeError("staging_evidence_required")
        if self.evidence_store is None:
            raise RuntimeError("staging_evidence_store_required")

        evidence = self.evidence_store.get(evidence_id)
        if evidence.task_id != task_id:
            raise RuntimeError("staging_evidence_task_mismatch")
        if evidence.project_id != project_id:
            raise RuntimeError("staging_evidence_project_mismatch")
        if evidence.staging_url != staging_url:
            raise RuntimeError("staging_evidence_url_mismatch")
        if evidence.revision != staging_commit:
            raise RuntimeError("staging_evidence_stale_revision")

        readiness = evaluate_readiness(evidence)
        if not readiness.ready:
            raise RuntimeError(
                "staging_evidence_not_ready:" + ",".join(readiness.failures)
            )
        return evidence

    def send_verified_task_to_staging(
        self,
        *,
        execution: dict,
        source_pr: int,
        source_commit: str,
        staging_branch: str,
        staging_commit: str,
        environment: StagingEnvironment,
        migration_ids: tuple[str, ...] = (),
        staging_evidence_id: str | None = None,
    ) -> dict:
        if execution.get("state") != "VERIFIED":
            raise RuntimeError("task_must_be_verified_before_staging")

        project_id = execution.get("project_id") or environment.project_id
        evidence = self._require_current_evidence(
            evidence_id=staging_evidence_id,
            task_id=execution["task_id"],
            project_id=project_id,
            staging_url=environment.url,
            staging_commit=staging_commit,
        )

        promotion = self.staging.create_promotion(
            task_id=execution["task_id"],
            task_branch=execution["branch"],
            staging_branch=staging_branch,
            source_pr=source_pr,
            source_commit=source_commit,
            migration_ids=migration_ids,
        )
        promotion = self.staging.deployed_to_staging(
            promotion,
            staging_commit=staging_commit,
            staging_evidence_id=evidence.evidence_id,
        )
        promotion = self.staging.ready_for_human(
            promotion,
            env=environment,
        )

        approval = request_approval(
            approval_id=f'APR-{execution["task_id"]}',
            task_id=execution["task_id"],
            action="MERGE_PULL_REQUEST",
            requested_by="integrator",
            requested_at=evidence.collected_at,
            staging_evidence_id=evidence.evidence_id,
            staging_url=evidence.staging_url,
            staging_revision=evidence.revision,
            source_pr=source_pr,
            source_commit=source_commit,
        )

        if self.event_router is not None:
            metadata = {
                "staging_evidence_id": evidence.evidence_id,
                "staging_revision": evidence.revision,
            }
            self.event_router.handle(OperationalEvent(
                event_id=f'{execution["task_id"]}-STAGING',
                project_id=project_id,
                event_type="STAGING_READY",
                target_type="task",
                target_id=execution["task_id"],
                title="Staging ready",
                message="The task is ready for online manual review.",
                action_url=evidence.staging_url,
                metadata=metadata,
            ))
            self.event_router.handle(OperationalEvent(
                event_id=f'{execution["task_id"]}-APPROVAL',
                project_id=project_id,
                event_type="APPROVAL_REQUIRED",
                target_type="task",
                target_id=execution["task_id"],
                title="Approval required",
                message="Manual approval is required before production promotion.",
                action_url=evidence.staging_url,
                metadata=metadata,
            ))

        return {
            "promotion": promotion,
            "approval": approval,
            "staging_url": evidence.staging_url,
            "staging_evidence_id": evidence.evidence_id,
        }

    def human_decision(
        self,
        *,
        promotion: Promotion,
        approval: Approval,
        decision: str,
        decided_by: str,
        decided_at: str,
        note: str | None = None,
    ) -> dict:
        if approval.staging_evidence_id != promotion.staging_evidence_id:
            raise RuntimeError("approval_staging_evidence_mismatch")
        if approval.staging_revision != promotion.staging_commit:
            raise RuntimeError("approval_staging_revision_mismatch")
        if approval.source_pr != promotion.source_pr:
            raise RuntimeError("approval_source_pr_mismatch")
        if approval.source_commit != promotion.source_commit:
            raise RuntimeError("approval_source_commit_mismatch")

        decided_approval = decide(
            approval,
            decision=decision,
            decided_by=decided_by,
            decided_at=decided_at,
            note=note,
        )

        decided_promotion = self.staging.decide(
            promotion,
            decision=decision,
            approval_id=decided_approval.approval_id,
        )

        return {
            "promotion": decided_promotion,
            "approval": decided_approval,
        }

    def create_production_promotion(
        self,
        *,
        promotion: Promotion,
        production_pr: int,
        promoted_commit: str,
        promoted_migration_ids: tuple[str, ...] = (),
    ) -> Promotion:
        return self.staging.promoted_to_main(
            promotion,
            production_pr=production_pr,
            promoted_commit=promoted_commit,
            promoted_migration_ids=promoted_migration_ids,
        )
