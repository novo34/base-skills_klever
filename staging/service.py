from __future__ import annotations

from staging.runtime import (
    Promotion,
    StagingEnvironment,
    approve,
    mark_in_staging,
    mark_promoted,
    mark_ready_for_human,
    reject,
    request_changes,
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
        source_commit: str,
        migration_ids: tuple[str, ...] = (),
    ) -> Promotion:
        return Promotion(
            task_id=task_id,
            task_branch=task_branch,
            staging_branch=staging_branch,
            source_pr=source_pr,
            source_commit=source_commit,
            migration_ids=tuple(migration_ids),
        )

    def deployed_to_staging(
        self,
        promotion: Promotion,
        *,
        staging_commit: str,
        staging_evidence_id: str | None = None,
    ) -> Promotion:
        return mark_in_staging(
            promotion,
            staging_commit=staging_commit,
            staging_evidence_id=staging_evidence_id,
        )

    def ready_for_human(self, promotion: Promotion, *, env: StagingEnvironment) -> Promotion:
        validation = self.validate_project_staging(env)
        return mark_ready_for_human(
            promotion,
            environment_ready=validation["ready"],
        )

    def decide(self, promotion: Promotion, *, decision: str, approval_id: str) -> Promotion:
        if decision == "APPROVED":
            return approve(promotion, approval_id=approval_id)
        if decision == "CHANGES_REQUESTED":
            return request_changes(promotion, approval_id=approval_id)
        if decision == "REJECTED":
            return reject(promotion, approval_id=approval_id)
        raise ValueError("invalid_staging_decision")

    def promoted_to_main(
        self,
        promotion: Promotion,
        *,
        production_pr: int,
        promoted_commit: str,
        promoted_migration_ids: tuple[str, ...] = (),
    ) -> Promotion:
        return mark_promoted(
            promotion,
            production_pr=production_pr,
            promoted_commit=promoted_commit,
            promoted_migration_ids=promoted_migration_ids,
        )
