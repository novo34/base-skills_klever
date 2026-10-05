import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from quality.runtime import RequirementQuality
from quality.service import QualityService


def test_quality_center_reports_requirement_coverage():
    result = QualityService().summarize([
        RequirementQuality(
            requirement_id="REQ-API-001",
            implemented=True,
            files=("api/contact.py",),
            unit_covered=True,
            integration_covered=True,
            e2e_covered=True,
            verification_status="VERIFIED",
        ),
        RequirementQuality(
            requirement_id="REQ-UI-002",
            implemented=False,
        ),
        RequirementQuality(
            requirement_id="REQ-DB-003",
            implemented=True,
            files=("db/migration.sql",),
            unit_covered=True,
            verification_status="FAILED",
        ),
    ])

    assert result["total"] == 3
    assert result["verified"] == 1
    assert result["missing_implementation"] == 1
    assert result["failed"] == 1
    assert result["coverage_pct"] == 33.33


def test_verified_requirement_without_unit_coverage_is_not_green():
    result = QualityService().summarize([
        RequirementQuality(
            requirement_id="REQ-X-001",
            implemented=True,
            verification_status="VERIFIED",
            unit_covered=False,
        )
    ])
    assert result["requirements"][0]["status"] == "MISSING_UNIT"
