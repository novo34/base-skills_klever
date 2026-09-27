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
    verification_passed: bool = False,
    staging_ready: bool = False,
    human_approved: bool = False,
    production_promoted: bool = False,
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
        if not production_promoted:
            raise TransitionError("production promotion gate not satisfied")

    return target
