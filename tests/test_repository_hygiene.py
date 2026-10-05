import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.hygiene import (
    CleanupEvidence,
    HygieneContractError,
    RepositoryHealth,
    classify_candidate,
    decide_reuse,
    detect_temporary_artifacts,
    validate_cleanup_evidence,
    validate_health_delta,
)


def test_dynamic_candidate_is_never_auto_deleted():
    result = classify_candidate(
        "plugin.php",
        referenced=False,
        dynamic_or_reflection=True,
    )
    assert result.classification == "POSSIBLY_DYNAMIC"


def test_unreferenced_candidate_is_only_likely_dead_without_explicit_proof():
    result = classify_candidate("legacy.php", referenced=False)
    assert result.classification == "LIKELY_DEAD"


def test_temp_detector_finds_backup_debug_and_tmp_paths():
    found = detect_temporary_artifacts(
        ("src/a.py", "tmp/output.json", "src/file.backup", "debug/debug.log")
    )
    assert "tmp/output.json" in found
    assert "src/file.backup" in found
    assert "debug/debug.log" in found


def test_reuse_guard_blocks_strong_duplicate_without_rationale():
    result = decide_reuse(
        proposed_surface="src/NewInvoiceService.php",
        candidates=(("src/InvoiceService.php", 0.93),),
        searched=True,
    )
    assert result.decision == "BLOCK_DUPLICATE"
    assert result.selected_candidate == "src/InvoiceService.php"


def test_reuse_guard_requires_search_before_creation():
    try:
        decide_reuse(
            proposed_surface="src/New.php",
            candidates=(),
            searched=False,
        )
    except HygieneContractError as exc:
        assert "reuse_search_required" in str(exc)
        return
    raise AssertionError("creation without grounded search must fail")


def test_cleanup_requires_replaced_code_to_be_removed_or_justified():
    evidence = CleanupEvidence(
        added=("new.py",),
        replaced=("old.py",),
        removed=(),
        retained_for_compatibility=(),
        temporary_created=(),
        temporary_removed=(),
        residual_debt=(),
    )
    try:
        validate_cleanup_evidence(evidence)
    except HygieneContractError as exc:
        assert "incomplete_cleanup:old.py" in str(exc)
        return
    raise AssertionError("replaced code cannot be abandoned")


def test_cleanup_requires_task_temporaries_to_be_removed():
    evidence = CleanupEvidence(
        added=(),
        replaced=(),
        removed=(),
        retained_for_compatibility=(),
        temporary_created=("tmp/debug.json",),
        temporary_removed=(),
        residual_debt=(),
    )
    try:
        validate_cleanup_evidence(evidence)
    except HygieneContractError as exc:
        assert "temporary_artifacts_not_cleaned" in str(exc)
        return
    raise AssertionError("temporary artifact must be cleaned or promoted")


def test_repository_cleanup_debt_cannot_silently_increase():
    health = RepositoryHealth(
        dead_code_candidates=1,
        duplicate_blocks=0,
        orphan_files=0,
        temporary_artifacts=0,
        unused_dependencies=1,
        stale_todos=0,
        generated_drift=0,
        cleanup_debt_score=12,
        baseline_cleanup_debt_score=10,
    )
    try:
        validate_health_delta(health)
    except HygieneContractError as exc:
        assert "cleanup_debt_regression" in str(exc)
        return
    raise AssertionError("cleanup debt regression must fail")
