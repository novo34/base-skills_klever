from __future__ import annotations

from dataclasses import dataclass


class StagingPolicyError(RuntimeError):
    pass


@dataclass(frozen=True)
class StagingEnvironment:
    project_id: str
    repository: str
    staging_branch: str
    url: str
    status: str = "UNKNOWN"
    web_reachable: bool = False
    backend_reachable: bool = False
    database_connected: bool = False
    migration_status: str = "UNKNOWN"


@dataclass(frozen=True)
class Promotion:
    task_id: str
    task_branch: str
    staging_branch: str
    source_pr: int
    source_commit: str
    migration_ids: tuple[str, ...] = ()
    status: str = "PENDING"
    staging_commit: str | None = None
    staging_evidence_id: str | None = None
    human_approval_id: str | None = None
    production_pr: int | None = None
    promoted_commit: str | None = None
    promoted_migration_ids: tuple[str, ...] = ()


def validate_environment(env: StagingEnvironment) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if env.staging_branch in {"main", "master"}:
        failures.append("staging_branch_must_differ_from_production")
    if not env.url:
        failures.append("staging_url_missing")
    if env.status != "READY":
        failures.append("staging_not_ready")
    if not env.web_reachable:
        failures.append("staging_web_not_reachable")
    if not env.backend_reachable:
        failures.append("staging_backend_not_reachable")
    if not env.database_connected:
        failures.append("staging_database_not_connected")
    if env.migration_status != "CURRENT":
        failures.append("staging_migrations_not_current")
    return not failures, failures


def mark_in_staging(
    promotion: Promotion,
    *,
    staging_commit: str,
    staging_evidence_id: str | None = None,
) -> Promotion:
    if promotion.status not in {"PENDING", "IN_STAGING"}:
        raise StagingPolicyError("invalid_staging_transition")
    return Promotion(
        **{
            **promotion.__dict__,
            "status": "IN_STAGING",
            "staging_commit": staging_commit,
            "staging_evidence_id": staging_evidence_id,
        }
    )


def mark_ready_for_human(promotion: Promotion, *, environment_ready: bool) -> Promotion:
    if promotion.status != "IN_STAGING":
        raise StagingPolicyError("task_not_in_staging")
    if not environment_ready:
        raise StagingPolicyError("staging_environment_not_ready")
    return Promotion(**{**promotion.__dict__, "status": "READY_FOR_HUMAN"})


def approve(promotion: Promotion, *, approval_id: str) -> Promotion:
    if promotion.status != "READY_FOR_HUMAN":
        raise StagingPolicyError("task_not_ready_for_human_approval")
    return Promotion(
        **{**promotion.__dict__, "status": "APPROVED", "human_approval_id": approval_id}
    )


def request_changes(promotion: Promotion, *, approval_id: str) -> Promotion:
    if promotion.status != "READY_FOR_HUMAN":
        raise StagingPolicyError("task_not_ready_for_human_approval")
    return Promotion(
        **{
            **promotion.__dict__,
            "status": "CHANGES_REQUESTED",
            "human_approval_id": approval_id,
        }
    )


def reject(promotion: Promotion, *, approval_id: str) -> Promotion:
    if promotion.status != "READY_FOR_HUMAN":
        raise StagingPolicyError("task_not_ready_for_human_approval")
    return Promotion(
        **{**promotion.__dict__, "status": "REJECTED", "human_approval_id": approval_id}
    )


def mark_promoted(
    promotion: Promotion,
    *,
    production_pr: int,
    promoted_commit: str,
    promoted_migration_ids: tuple[str, ...] = (),
) -> Promotion:
    if promotion.status != "APPROVED":
        raise StagingPolicyError("task_not_approved")
    if promoted_commit != promotion.source_commit:
        raise StagingPolicyError("promotion_commit_must_match_approved_task_commit")
    if tuple(promoted_migration_ids) != tuple(promotion.migration_ids):
        raise StagingPolicyError("promotion_migrations_must_match_approved_task")
    if promotion.staging_commit == promoted_commit and promotion.staging_commit != promotion.source_commit:
        raise StagingPolicyError("whole_staging_commit_promotion_forbidden")

    return Promotion(
        **{
            **promotion.__dict__,
            "status": "PROMOTED_TO_MAIN",
            "production_pr": production_pr,
            "promoted_commit": promoted_commit,
            "promoted_migration_ids": tuple(promoted_migration_ids),
        }
    )
