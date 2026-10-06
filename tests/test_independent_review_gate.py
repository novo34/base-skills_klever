import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.independent_review import review_pull_request


def test_normal_r1_change_passes_without_manual_acknowledgement():
    result = review_pull_request(
        {"docs/example.md"},
        declared_risk="R1",
        pr_body="JEV-RISK: R1\n",
    )
    assert result["review_mode"] == "single_operator_base_controlled_automation"
    assert result["requires_acknowledgement"] is False


def test_self_protection_change_requires_r4():
    try:
        review_pull_request(
            {".github/workflows/validate-skills.yml"},
            declared_risk="R3",
            pr_body="JEV-RISK: R3\nJEV-INDEPENDENT-REVIEW: acknowledged\n",
        )
    except PermissionError as exc:
        assert "declared_risk_too_low" in str(exc) or "self_protection_change_requires_R4" in str(exc)
        return
    raise AssertionError("self-protection changes must require R4")


def test_self_protection_change_requires_explicit_acknowledgement():
    try:
        review_pull_request(
            {"scripts/independent_review.py"},
            declared_risk="R4",
            pr_body="JEV-RISK: R4\n",
        )
    except PermissionError as exc:
        assert "independent_review_acknowledgement_required" in str(exc)
        return
    raise AssertionError("self-protection changes require acknowledgement")


def test_self_protection_r4_with_acknowledgement_passes():
    result = review_pull_request(
        {".github/CODEOWNERS"},
        declared_risk="R4",
        pr_body=(
            "JEV-RISK: R4\n"
            "JEV-INDEPENDENT-REVIEW: acknowledged\n"
        ),
    )
    assert result["acknowledged"] is True
    assert result["self_protection_paths"] == [".github/CODEOWNERS"]


def test_rename_source_is_reviewed_when_api_supplies_previous_filename():
    result = review_pull_request(
        {"authz/policy.py", "lib/policy.py"},
        declared_risk="R3",
        pr_body="JEV-RISK: R3\n",
    )
    assert result["derived_risk"] == "R3"
