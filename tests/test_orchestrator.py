import importlib.util
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


def test_r1_full_happy_path():
    task = create_task_execution("TASK-101", {"backend", "implementation"}, set())
    task = advance(task, "READY")
    task = advance(task, "RUNNING")
    task = advance(task, "VERIFYING")
    task = advance(task, "VERIFIED", verification_passed=True)
    task = advance(task, "DONE")
    assert task["state"] == "DONE"


def test_r4_done_requires_human_approval():
    task = create_task_execution(
        "TASK-102",
        {"database", "implementation"},
        {"destructive_data_change"},
    )
    task = advance(task, "READY")
    task = advance(task, "RUNNING")
    task = advance(task, "VERIFYING")
    task = advance(task, "VERIFIED", verification_passed=True)

    try:
        advance(task, "DONE", human_approved=False)
    except TransitionError:
        pass
    else:
        raise AssertionError("R4 must require human approval")

    task = advance(task, "DONE", human_approved=True)
    assert task["state"] == "DONE"
