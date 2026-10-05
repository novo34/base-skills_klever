from __future__ import annotations

from dataclasses import dataclass

from staging.adapter import StagingDeploymentRequest


class StagingProviderPolicyError(PermissionError):
    pass


@dataclass(frozen=True)
class StagingReferencePolicy:
    database_refs: frozenset[str]
    secret_refs: frozenset[str]


def validate_staging_request(
    request: StagingDeploymentRequest,
    *,
    reference_policy: StagingReferencePolicy,
) -> None:
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

    if request.database_ref not in reference_policy.database_refs:
        raise StagingProviderPolicyError("staging_database_reference_not_allowed")

    unknown_secrets = set(request.secret_refs) - set(reference_policy.secret_refs)
    if unknown_secrets:
        raise StagingProviderPolicyError(
            "staging_secret_reference_not_allowed:" + ",".join(sorted(unknown_secrets))
        )
