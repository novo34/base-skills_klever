from __future__ import annotations

from approvals.runtime import Approval, decide, request_approval
from staging.runtime import Promotion, StagingEnvironment
from staging.service import StagingService


class StagingPipeline:
    def __init__(self, staging: StagingService | None = None):
        self.staging = staging or StagingService()

    def send_verified_task_to_staging(
        self,
        *,
        execution: dict,
        source_pr: int,
        staging_branch: str,
        staging_commit: str,
        environment: StagingEnvironment,
    ) -> dict:
        if execution.get("state") != "VERIFIED":
            raise RuntimeError("task_must_be_verified_before_staging")

        promotion = self.staging.create_promotion(
            task_id=execution["task_id"],
            task_branch=execution["branch"],
            staging_branch=staging_branch,
            source_pr=source_pr,
        )
        promotion = self.staging.deployed_to_staging(
            promotion,
            staging_commit=staging_commit,
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
        )

        return {
            "promotion": promotion,
            "approval": approval,
            "staging_url": environment.url,
        }

    def human_decision(
        self,
        *,
        promotion: Promotion,
        approval: Approval,
        decision: str,
        decided_by: str,
        note: str | None = None,
    ) -> dict:
        decided_approval = decide(
            approval,
            decision=decision,
            decided_by=decided_by,
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
    ) -> Promotion:
        return self.staging.promoted_to_main(
            promotion,
            production_pr=production_pr,
        )
