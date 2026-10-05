import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from verification.checks import command_exit_code, github_ci_status
from verification.evidence_builder import EvidenceBuilder


def test_evidence_builder_maps_real_sources():
    evidence = EvidenceBuilder().from_sources(
        requirement_ids=["REQ-API-001"],
        ci_status="success",
        unit_exit_code=0,
        integration_exit_code=0,
        e2e_exit_code=0,
        diff_reviewed=True,
        backend_verified=True,
    )
    assert evidence.ci_passed is True
    assert evidence.unit_passed is True
    assert evidence.integration_passed is True
    assert evidence.e2e_passed is True
    assert evidence.backend_verified is True


def test_failed_command_becomes_failed_evidence():
    evidence = EvidenceBuilder().from_sources(
        requirement_ids=["REQ-API-002"],
        ci_status="success",
        unit_exit_code=1,
        integration_exit_code=0,
        e2e_exit_code=0,
        diff_reviewed=True,
    )
    assert evidence.unit_passed is False


def test_github_ci_normalization():
    assert github_ci_status({"conclusion": "success"}) == "success"
    assert github_ci_status({"status": "completed", "success": True}) == "success"
    assert github_ci_status({"status": "in_progress"}) == "in_progress"


def test_command_exit_code_normalization():
    assert command_exit_code({"exit_code": 0}) == 0
    assert command_exit_code({"exit_code": 2}) == 2
    assert command_exit_code({}) is None
