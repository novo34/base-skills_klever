import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.scheduler import (
    DependencyScheduler,
    ScheduledAssignment,
    SchedulerError,
)


def test_scheduler_returns_runnable_assignments_deterministically():
    scheduler = DependencyScheduler()
    scheduler.add(ScheduledAssignment("B", "TASK-1", "developer"))
    scheduler.add(ScheduledAssignment("A", "TASK-1", "architect"))
    scheduler.add(ScheduledAssignment(
        "C",
        "TASK-1",
        "verifier",
        dependency_ids=("A", "B"),
    ))
    scheduler.validate_graph()

    assert [item.assignment_id for item in scheduler.runnable()] == ["A", "B"]


def test_dependencies_must_complete_before_assignment_runs():
    scheduler = DependencyScheduler()
    scheduler.add(ScheduledAssignment("ARCH", "TASK-1", "architect"))
    scheduler.add(ScheduledAssignment(
        "DEV",
        "TASK-1",
        "developer",
        dependency_ids=("ARCH",),
    ))

    try:
        scheduler.transition("DEV", "RUNNING")
    except SchedulerError as exc:
        assert "assignment_dependencies_not_satisfied" in str(exc)
    else:
        raise AssertionError("developer must wait for architect")

    scheduler.transition("ARCH", "RUNNING")
    scheduler.transition("ARCH", "COMPLETED")
    scheduler.transition("DEV", "RUNNING")
    assert scheduler.get("DEV").status == "RUNNING"


def test_failed_dependency_blocks_dependents():
    scheduler = DependencyScheduler()
    scheduler.add(ScheduledAssignment("DEV", "TASK-1", "developer"))
    scheduler.add(ScheduledAssignment(
        "VER",
        "TASK-1",
        "verifier",
        dependency_ids=("DEV",),
    ))

    scheduler.transition("DEV", "RUNNING")
    scheduler.transition("DEV", "FAILED")

    assert scheduler.get("VER").status == "BLOCKED"


def test_cycle_is_rejected():
    scheduler = DependencyScheduler()
    scheduler.add(ScheduledAssignment(
        "A", "TASK-1", "architect", dependency_ids=("B",)
    ))
    scheduler.add(ScheduledAssignment(
        "B", "TASK-1", "developer", dependency_ids=("A",)
    ))

    try:
        scheduler.validate_graph()
    except SchedulerError as exc:
        assert "dependency_cycle" in str(exc)
        return
    raise AssertionError("dependency cycle must fail")


def test_unknown_dependency_is_rejected():
    scheduler = DependencyScheduler()
    scheduler.add(ScheduledAssignment(
        "DEV", "TASK-1", "developer", dependency_ids=("MISSING",)
    ))

    try:
        scheduler.validate_graph()
    except SchedulerError as exc:
        assert "unknown_dependency" in str(exc)
        return
    raise AssertionError("unknown dependency must fail")
