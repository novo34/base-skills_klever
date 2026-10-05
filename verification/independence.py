from __future__ import annotations

from dataclasses import dataclass


class VerificationIndependenceError(PermissionError):
    pass


@dataclass(frozen=True)
class VerificationAssignment:
    task_id: str
    risk: str
    implementer_agent_id: str
    verifier_agent_id: str
    implementer_provider: str
    verifier_provider: str
    implementer_model: str
    verifier_model: str


HIGH_RISK_DISTINCT_PROVIDER = {"R3", "R4"}


def validate_verification_independence(
    assignment: VerificationAssignment,
) -> None:
    if assignment.implementer_agent_id == assignment.verifier_agent_id:
        raise VerificationIndependenceError("self_verification_forbidden")

    if assignment.risk in HIGH_RISK_DISTINCT_PROVIDER:
        if assignment.implementer_provider == assignment.verifier_provider:
            raise VerificationIndependenceError(
                "high_risk_verifier_provider_must_differ"
            )

    if (
        assignment.implementer_provider == assignment.verifier_provider
        and assignment.implementer_model == assignment.verifier_model
        and assignment.risk in {"R2", "R3", "R4"}
    ):
        raise VerificationIndependenceError(
            "elevated_risk_verifier_model_must_differ"
        )
