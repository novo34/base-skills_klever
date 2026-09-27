from __future__ import annotations

from staging.adapter import (
    StagingDeploymentRequest,
    StagingProviderAdapter,
    StagingStepResult,
)
from staging.provider_policy import StagingReferencePolicy, validate_staging_request


class StagingProviderService:
    def __init__(
        self,
        adapter: StagingProviderAdapter,
        *,
        reference_policy: StagingReferencePolicy,
    ):
        self.adapter = adapter
        self.reference_policy = reference_policy

    def prepare(self, request: StagingDeploymentRequest) -> dict:
        validate_staging_request(
            request,
            reference_policy=self.reference_policy,
        )

        steps: list[tuple[str, StagingStepResult]] = []
        operations = (
            ("deploy", self.adapter.deploy),
            ("database", self.adapter.verify_database),
            ("migrations", self.adapter.apply_migrations),
            ("seed", self.adapter.seed_test_data),
            ("health", self.adapter.health_check),
            ("e2e", self.adapter.run_online_e2e),
        )

        for name, operation in operations:
            result = operation(request)
            steps.append((name, result))
            if not result.ok:
                return {
                    "ready": False,
                    "failed_step": name,
                    "steps": {
                        step_name: step_result
                        for step_name, step_result in steps
                    },
                }

        return {
            "ready": True,
            "failed_step": None,
            "steps": {
                step_name: step_result
                for step_name, step_result in steps
            },
        }
