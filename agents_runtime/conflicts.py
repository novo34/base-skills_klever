from __future__ import annotations

from dataclasses import dataclass


class ConflictResolutionError(RuntimeError):
    pass


@dataclass(frozen=True)
class IntegrationConflict:
    conflict_id: str
    task_id: str
    repository: str
    branch_a: str
    branch_b: str
    paths: tuple[str, ...]
    status: str = "DETECTED"
    resolution_strategy: str | None = None
    resolved_by: str | None = None
    resolution_note: str | None = None


ALLOWED_CONFLICT_STATES = {
    "DETECTED",
    "RESOLUTION_REQUIRED",
    "RESOLVED",
    "REJECTED",
}

ALLOWED_RESOLUTION_STRATEGIES = {
    "REBASE",
    "MANUAL_MERGE",
    "REIMPLEMENT",
    "DROP_ONE_CHANGE",
}


def require_resolution(conflict: IntegrationConflict) -> None:
    if conflict.status != "RESOLVED":
        raise ConflictResolutionError("integration_conflict_unresolved")


def mark_resolution_required(conflict: IntegrationConflict) -> IntegrationConflict:
    if conflict.status != "DETECTED":
        raise ConflictResolutionError("invalid_conflict_transition")
    return IntegrationConflict(
        **{**conflict.__dict__, "status": "RESOLUTION_REQUIRED"}
    )


def resolve_conflict(
    conflict: IntegrationConflict,
    *,
    strategy: str,
    resolved_by: str,
    note: str,
) -> IntegrationConflict:
    if conflict.status not in {"DETECTED", "RESOLUTION_REQUIRED"}:
        raise ConflictResolutionError("conflict_not_resolvable")
    if strategy not in ALLOWED_RESOLUTION_STRATEGIES:
        raise ConflictResolutionError("invalid_resolution_strategy")
    if not resolved_by:
        raise ConflictResolutionError("resolver_required")
    if not note:
        raise ConflictResolutionError("resolution_note_required")

    return IntegrationConflict(
        **{
            **conflict.__dict__,
            "status": "RESOLVED",
            "resolution_strategy": strategy,
            "resolved_by": resolved_by,
            "resolution_note": note,
        }
    )
