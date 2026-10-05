import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from quality.ingestion import QualityTraceIngestor
from quality.trace_service import TraceDrivenQualityService
from scripts.trace_requirement import build_record


def trace(
    requirement_id,
    *,
    status="VERIFYING",
    files=None,
    unit=None,
    integration=None,
    e2e=None,
    result="NOT_RUN",
):
    return build_record(
        requirement_id=requirement_id,
        source="SPEC.md",
        status=status,
        task_id="TASK-1",
        branch="feat/TASK-1",
        pull_request=42,
        files=files or [],
        unit_tests=unit or [],
        integration_tests=integration or [],
        e2e_tests=e2e or [],
        result=result,
    )


def test_quality_is_derived_from_trace_record():
    record = trace(
        "REQ-API-001",
        status="VERIFIED",
        files=["api/contact.py"],
        unit=["tests/test_contact.py"],
        integration=["tests/test_contact_api.py"],
        e2e=["tests/e2e/contact.spec.ts"],
        result="PASS",
    )

    items = QualityTraceIngestor().from_trace_dicts([record])
    item = items[0]

    assert item.implemented is True
    assert item.unit_covered is True
    assert item.integration_covered is True
    assert item.e2e_covered is True
    assert item.verification_status == "VERIFIED"


def test_missing_files_can_never_be_marked_implemented_by_trace_ingestion():
    record = trace(
        "REQ-UI-002",
        status="VERIFIED",
        files=[],
        unit=["tests/test_ui.py"],
        result="PASS",
    )

    item = QualityTraceIngestor().from_trace_dicts([record])[0]
    assert item.implemented is False


def test_not_run_verification_never_becomes_green():
    record = trace(
        "REQ-DB-003",
        status="VERIFYING",
        files=["db/migration.sql"],
        unit=["tests/test_db.py"],
        result="NOT_RUN",
    )

    result = TraceDrivenQualityService().summarize_trace_dicts([record])
    assert result["verified"] == 0
    assert result["unverified"] == 1


def test_failed_verification_is_reflected_automatically():
    record = trace(
        "REQ-API-004",
        status="VERIFYING",
        files=["api/a.py"],
        unit=["tests/test_a.py"],
        result="FAIL",
    )
    result = TraceDrivenQualityService().summarize_trace_dicts([record])
    assert result["failed"] == 1
