from __future__ import annotations

from staging.adapter import StagingDeploymentRequest


class StagingProviderPolicyError(PermissionError):
    pass


FORBIDDEN_SECRET_MARKERS = {
    "production",
    "prod_db",
    "prod-database",
    "production_database",
    "production-db",
}


def validate_staging_request(request: StagingDeploymentRequest) -> None:
    if request.environment_kind != "PERMANENT_STAGING":
        raise StagingProviderPolicyError("environment_must_be_permanent_staging")

    if request.source_branch in {"main", "master"}:
        raise StagingProviderPolicyError("task_source_branch_must_not_be_production")

    if request.staging_branch in {"main", "master"}:
        raise StagingProviderPolicyError("staging_branch_must_not_be_production")

    if request.source_branch == request.staging_branch:
        raise StagingProviderPolicyError("source_and_staging_branch_must_differ")

    if not request.staging_url:
        raise StagingProviderPolicyError("staging_url_required")

    if not request.database_ref:
        raise StagingProviderPolicyError("staging_database_ref_required")

    database_lower = request.database_ref.lower()
    if any(marker in database_lower for marker in FORBIDDEN_SECRET_MARKERS):
        raise StagingProviderPolicyError("production_database_reference_forbidden")

    for secret_ref in request.secret_refs:
        lower = secret_ref.lower()
        if any(marker in lower for marker in FORBIDDEN_SECRET_MARKERS):
            raise StagingProviderPolicyError("production_secret_reference_forbidden")
