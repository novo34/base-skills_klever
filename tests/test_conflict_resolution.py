import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.conflicts import (
    ConflictResolutionError,
    IntegrationConflict,
    mark_resolution_required,
    require_resolution,
    resolve_conflict,
)


def conflict():
    return IntegrationConflict(
        conflict_id="CONFLICT-1",
        task_id="TASK-1",
        repository="novo34/example",
        branch_a="feat/A",
        branch_b="feat/B",
        paths=("app/page.tsx",),
    )


def test_unresolved_conflict_blocks_integration():
    try:
        require_resolution(conflict())
    except ConflictResolutionError as exc:
        assert "integration_conflict_unresolved" in str(exc)
        return
    raise AssertionError("unresolved conflict must block integration")


def test_conflict_requires_explicit_resolution_record():
    item = mark_resolution_required(conflict())
    resolved = resolve_conflict(
        item,
        strategy="MANUAL_MERGE",
        resolved_by="integrator-run-1",
        note="Merged both UI changes and reran verification.",
    )
    assert resolved.status == "RESOLVED"
    assert resolved.resolution_strategy == "MANUAL_MERGE"
    assert resolved.resolved_by == "integrator-run-1"
    require_resolution(resolved)


def test_invalid_resolution_strategy_is_rejected():
    try:
        resolve_conflict(
            conflict(),
            strategy="LAST_WRITER_WINS",
            resolved_by="integrator-run-1",
            note="Unsafe",
        )
    except ConflictResolutionError as exc:
        assert "invalid_resolution_strategy" in str(exc)
        return
    raise AssertionError("silent overwrite strategy must never be accepted")
