from __future__ import annotations

ALLOWED = {
    "PLANNED": {"READY", "BLOCKED"},
    "READY": {"RUNNING", "BLOCKED"},
    "RUNNING": {"VERIFYING", "FAILED", "BLOCKED"},
    "BLOCKED": {"READY", "FAILED"},
    "VERIFYING": {"VERIFIED", "FAILED", "BLOCKED"},
    "VERIFIED": {"DONE"},
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
    human_approved: bool = False,
) -> str:
    if target not in ALLOWED.get(current, set()):
        raise TransitionError(f"invalid transition: {current} -> {target}")

    if target == "VERIFIED" and not verification_passed:
        raise TransitionError("verification gate not satisfied")

    if target == "DONE":
        if current != "VERIFIED":
            raise TransitionError("task must be VERIFIED before DONE")
        if risk == "R4" and not human_approved:
            raise TransitionError("R4 completion requires human approval")

    return target
