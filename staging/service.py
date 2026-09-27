from __future__ import annotations

from staging.runtime import (
    Promotion,
    StagingEnvironment,
    approve,
    mark_in_staging,
    mark_promoted,
    mark_ready_for_human,
    reject,
    validate_environment,
)


class StagingService:
    def validate_project_staging(self, env: StagingEnvironment) -> dict:
        ok, failures = validate_environment(env)
        return {"ready": ok, "failures": failures}

    def create_promotion(
        self,
        *,
        task_id: str,
        task_branch: str,
        staging_branch: str,
        source_pr: int,
    ) -> Promotion:
        return Promotion(
            task_id=task_id,
            task_branch=task_branch,
            staging_branch=staging_branch,
            source_pr=source_pr,
        )

    def deployed_to_staging(self, promotion: Promotion, *, staging_commit: str) -> Promotion:
        return mark_in_staging(promotion, staging_commit=staging_commit)

    def ready_for_human(self, promotion: Promotion, *, env: StagingEnvironment) -> Promotion:
        validation = self.validate_project_staging(env)
        return mark_ready_for_human(
            promotion,
            environment_ready=validation["ready"],
        )

    def decide(self, promotion: Promotion, *, approved: bool, approval_id: str) -> Promotion:
        return approve(promotion, approval_id=approval_id) if approved else reject(
            promotion, approval_id=approval_id
        )

    def promoted_to_main(self, promotion: Promotion, *, production_pr: int) -> Promotion:
        return mark_promoted(promotion, production_pr=production_pr)
