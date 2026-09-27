from __future__ import annotations

ALLOWED = {
    "PLANNED": {"READY", "BLOCKED"},
    "READY": {"RUNNING", "BLOCKED"},
    "RUNNING": {"VERIFYING", "FAILED", "BLOCKED"},
    "BLOCKED": {"READY", "FAILED"},
    "VERIFYING": {"VERIFIED", "FAILED", "BLOCKED"},
    "VERIFIED": {"STAGING"},
    "STAGING": {"AWAITING_HUMAN", "FAILED", "BLOCKED"},
    "AWAITING_HUMAN": {"APPROVED", "CHANGES_REQUESTED", "REJECTED"},
    "CHANGES_REQUESTED": {"READY"},
    "REJECTED": {"READY"},
    "APPROVED": {"DONE"},
    "FAILED": {"READY"},
    "DONE": set(),
}


class TransitionError(RuntimeError):
    pass


def transition(
    current: str,
    target: str,
    *,
    risk: str,
    task_id: str | None = None,
    verification_passed: bool = False,
    staging_ready: bool = False,
    human_approved: bool = False,
    production_promotion=None,
) -> str:
    if target not in ALLOWED.get(current, set()):
        raise TransitionError(f"invalid transition: {current} -> {target}")

    if target == "VERIFIED" and not verification_passed:
        raise TransitionError("verification gate not satisfied")

    if target == "AWAITING_HUMAN" and not staging_ready:
        raise TransitionError("staging readiness gate not satisfied")

    if target == "APPROVED" and not human_approved:
        raise TransitionError("human approval gate not satisfied")

    if target == "DONE":
        if current != "APPROVED":
            raise TransitionError("task must be APPROVED before DONE")
        if production_promotion is None:
            raise TransitionError("production promotion required before DONE")
        if task_id is None:
            raise TransitionError("task_id required for production promotion gate")
        if getattr(production_promotion, "task_id", None) != task_id:
            raise TransitionError("production promotion task mismatch")
        if getattr(production_promotion, "status", None) != "PROMOTED_TO_MAIN":
            raise TransitionError("production promotion must be PROMOTED_TO_MAIN")
        if not getattr(production_promotion, "promoted_commit", None):
            raise TransitionError("promoted commit required before DONE")
        if getattr(production_promotion, "production_pr", None) is None:
            raise TransitionError("production PR required before DONE")

    return target
