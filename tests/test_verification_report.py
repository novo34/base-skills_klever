import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from verification.report import build_report
from verification.runtime import VerificationEvidence, VerificationResult


def test_report_exposes_failures_and_checks():
    evidence = VerificationEvidence(
        requirement_ids=("REQ-UI-001",),
        ci_passed=True,
        unit_passed=True,
        integration_passed=True,
        e2e_passed=False,
        diff_reviewed=True,
        frontend_verified=True,
    )
    result = VerificationResult(
        status="FAILED",
        failures=("e2e_failed_or_missing",),
        evidence=evidence,
    )
    report = build_report("TASK-1", result)

    assert report["status"] == "FAILED"
    assert report["checks"]["ci"] is True
    assert report["checks"]["e2e"] is False
    assert report["failures"] == ["e2e_failed_or_missing"]
