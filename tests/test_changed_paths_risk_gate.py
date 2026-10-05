import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_changed_paths_risk import validate_changed_paths_risk


def test_declared_risk_lower_than_authz_diff_fails():
    try:
        validate_changed_paths_risk(
            {"authz/policy.py"},
            declared_risk="R1",
        )
    except PermissionError as exc:
        assert "declared_risk_too_low:R1<derived:R3" in str(exc)
        return
    raise AssertionError("authz change must reject understated declared risk")


def test_declared_risk_lower_than_workflow_diff_fails():
    try:
        validate_changed_paths_risk(
            {".github/workflows/validate-skills.yml"},
            declared_risk="R3",
        )
    except PermissionError as exc:
        assert "declared_risk_too_low:R3<derived:R4" in str(exc)
        return
    raise AssertionError("workflow change must require R4")


def test_rename_source_and_destination_preserve_sensitive_source_risk():
    payload = validate_changed_paths_risk(
        {"authz/policy.py", "lib/policy.py"},
        declared_risk="R3",
    )
    assert payload["derived_risk"] == "R3"
    assert "auth_or_authorization_change" in payload["derived_flags"]


def test_matching_declared_risk_passes():
    payload = validate_changed_paths_risk(
        {".github/workflows/ci.yml"},
        declared_risk="R4",
    )
    assert payload["declared_risk"] == "R4"
    assert payload["derived_risk"] == "R4"
