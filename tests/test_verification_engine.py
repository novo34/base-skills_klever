import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from verification.runtime import VerificationEvidence
from verification.service import VerificationService


def full_evidence(**overrides):
    data = dict(
        requirement_ids=("REQ-API-001",),
        ci_passed=True,
        unit_passed=True,
        integration_passed=True,
        e2e_passed=True,
        diff_reviewed=True,
        backend_verified=True,
        frontend_verified=True,
        database_verified=True,
    )
    data.update(overrides)
    return VerificationEvidence(**data)


def test_backend_task_verifies_with_complete_evidence():
    result = VerificationService().evaluate(
        triggers={"backend", "api"},
        evidence=full_evidence(),
    )
    assert result.status == "VERIFIED"
    assert result.failures == ()


def test_missing_requirement_traceability_fails():
    result = VerificationService().evaluate(
        triggers={"backend"},
        evidence=full_evidence(requirement_ids=()),
    )
    assert result.status == "FAILED"
    assert "missing_requirement_traceability" in result.failures


def test_frontend_task_requires_frontend_verification():
    result = VerificationService().evaluate(
        triggers={"frontend", "ui"},
        evidence=full_evidence(frontend_verified=False),
    )
    assert result.status == "FAILED"
    assert "frontend_not_verified" in result.failures


def test_database_task_requires_database_verification():
    result = VerificationService().evaluate(
        triggers={"database", "migration"},
        evidence=full_evidence(database_verified=False),
    )
    assert result.status == "FAILED"
    assert "database_not_verified" in result.failures


def test_missing_e2e_blocks_non_documentation_task():
    result = VerificationService().evaluate(
        triggers={"backend"},
        evidence=full_evidence(e2e_passed=False),
    )
    assert result.status == "FAILED"
    assert "e2e_failed_or_missing" in result.failures


def test_documentation_only_does_not_require_e2e():
    result = VerificationService().evaluate(
        triggers={"documentation"},
        evidence=full_evidence(e2e_passed=False),
    )
    assert result.status == "VERIFIED"
