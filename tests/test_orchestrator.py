import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "orchestrator"))

from task_orchestrator import create_task_execution, advance
from state_machine import TransitionError


def test_normal_task_cannot_skip_to_done():
    task = create_task_execution("TASK-100", {"backend", "implementation"}, set())
    try:
        advance(task, "DONE")
    except TransitionError:
        return
    raise AssertionError("task must not skip gates")


def test_full_happy_path_requires_staging_and_human_approval():
    task = create_task_execution("TASK-101", {"backend", "implementation"}, set())
    task = advance(task, "READY")
    task = advance(task, "RUNNING")
    task = advance(task, "VERIFYING")
    task = advance(task, "VERIFIED", verification_passed=True)
    task = advance(task, "STAGING")

    try:
        advance(task, "AWAITING_HUMAN", staging_ready=False)
    except TransitionError:
        pass
    else:
        raise AssertionError("human review requires ready staging")

    task = advance(task, "AWAITING_HUMAN", staging_ready=True)

    try:
        advance(task, "APPROVED", human_approved=False)
    except TransitionError:
        pass
    else:
        raise AssertionError("approval requires explicit human decision")

    task = advance(task, "APPROVED", human_approved=True)
    task = advance(task, "DONE")
    assert task["state"] == "DONE"


def test_verified_cannot_go_directly_to_done():
    task = create_task_execution("TASK-102", {"frontend", "implementation"}, set())
    task = advance(task, "READY")
    task = advance(task, "RUNNING")
    task = advance(task, "VERIFYING")
    task = advance(task, "VERIFIED", verification_passed=True)

    try:
        advance(task, "DONE", human_approved=True)
    except TransitionError:
        return
    raise AssertionError("VERIFIED must go through staging and human review")


def test_request_changes_returns_task_to_ready():
    task = create_task_execution("TASK-103", {"ui", "implementation"}, set())
    task = advance(task, "READY")
    task = advance(task, "RUNNING")
    task = advance(task, "VERIFYING")
    task = advance(task, "VERIFIED", verification_passed=True)
    task = advance(task, "STAGING")
    task = advance(task, "AWAITING_HUMAN", staging_ready=True)
    task = advance(task, "CHANGES_REQUESTED")
    task = advance(task, "READY")
    assert task["state"] == "READY"


def test_rejected_task_can_only_reenter_through_ready():
    task = create_task_execution("TASK-104", {"ui", "implementation"}, set())
    task = advance(task, "READY")
    task = advance(task, "RUNNING")
    task = advance(task, "VERIFYING")
    task = advance(task, "VERIFIED", verification_passed=True)
    task = advance(task, "STAGING")
    task = advance(task, "AWAITING_HUMAN", staging_ready=True)
    task = advance(task, "REJECTED")
    task = advance(task, "READY")
    assert task["state"] == "READY"
