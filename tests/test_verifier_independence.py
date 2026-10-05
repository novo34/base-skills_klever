import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from verification.independence import (
    VerificationAssignment,
    VerificationIndependenceError,
    validate_verification_independence,
)


def assignment(**overrides):
    data = dict(
        task_id="TASK-1",
        risk="R2",
        implementer_agent_id="developer-run-1",
        verifier_agent_id="verifier-run-1",
        implementer_provider="deepseek",
        verifier_provider="openai",
        implementer_model="deepseek-code",
        verifier_model="gpt-verifier",
    )
    data.update(overrides)
    return VerificationAssignment(**data)


def test_self_verification_is_forbidden():
    try:
        validate_verification_independence(
            assignment(verifier_agent_id="developer-run-1")
        )
    except VerificationIndependenceError as exc:
        assert "self_verification_forbidden" in str(exc)
        return
    raise AssertionError("implementer cannot verify its own work")


def test_high_risk_requires_distinct_provider():
    try:
        validate_verification_independence(
            assignment(
                risk="R3",
                verifier_provider="deepseek",
                verifier_model="other-model",
            )
        )
    except VerificationIndependenceError as exc:
        assert "high_risk_verifier_provider_must_differ" in str(exc)
        return
    raise AssertionError("high-risk verification must use distinct provider")


def test_r2_requires_distinct_model_when_same_provider():
    try:
        validate_verification_independence(
            assignment(
                risk="R2",
                verifier_provider="deepseek",
                verifier_model="deepseek-code",
            )
        )
    except VerificationIndependenceError as exc:
        assert "elevated_risk_verifier_model_must_differ" in str(exc)
        return
    raise AssertionError("R2 verifier must not reuse same provider/model pair")


def test_independent_assignment_is_allowed():
    validate_verification_independence(assignment())
