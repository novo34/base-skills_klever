import copy
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.development_control import (
    DevelopmentControlError,
    assert_start_allowed,
    next_task_decision,
    validate_done_transition,
)


def backlog_tasks(*, gate_done: bool = True):
    data = yaml.safe_load(
        (ROOT / "backlog" / "jev-master-tasks.yaml").read_text(encoding="utf-8")
    ) or {}
    tasks = list(data["tasks"])
    by_id = {task["id"]: task for task in tasks}
    by_id["FND-071"]["status"] = "DONE" if gate_done else "TODO"
    return tasks


def test_current_next_platform_task_is_plt_002():
    decision = next_task_decision(backlog_tasks(), scope="PLATFORM")
    assert decision.decision == "NEXT_TASK"
    assert decision.selected_task_id == "PLT-002"
    assert decision.requires_operator_authorization is True


def test_cannot_jump_from_next_task_to_later_task():
    try:
        assert_start_allowed(
            backlog_tasks(),
            requested_task_id="PLT-020",
            operator_authorized_task_id="PLT-020",
        )
    except DevelopmentControlError as exc:
        assert "task_jump_forbidden" in str(exc)
        return
    raise AssertionError("later task jump must fail")


def test_exact_next_task_requires_operator_authorization():
    try:
        assert_start_allowed(
            backlog_tasks(),
            requested_task_id="PLT-002",
            operator_authorized_task_id=None,
        )
    except DevelopmentControlError as exc:
        assert "operator_authorization_required" in str(exc)
        return
    raise AssertionError("start without operator approval must fail")


def test_exact_next_task_can_be_authorized():
    decision = assert_start_allowed(
        backlog_tasks(),
        requested_task_id="PLT-002",
        operator_authorized_task_id="PLT-002",
    )
    assert decision.selected_task_id == "PLT-002"


def test_later_active_task_is_invalid_even_if_dependencies_are_met():
    tasks = copy.deepcopy(backlog_tasks())
    by_id = {task["id"]: task for task in tasks}
    by_id["PLT-020"]["status"] = "IN_PROGRESS"
    decision = next_task_decision(tasks)
    assert decision.decision == "INVALID"
    assert "PLT-020" in decision.unauthorized_active_tasks


def test_blocked_first_task_prevents_later_execution():
    tasks = copy.deepcopy(backlog_tasks())
    by_id = {task["id"]: task for task in tasks}
    by_id["PLT-002"]["status"] = "BLOCKED"
    decision = next_task_decision(tasks)
    assert decision.decision == "BLOCKED"
    assert decision.selected_task_id == "PLT-002"


def test_unsatisfied_dependency_blocks_first_task():
    tasks = copy.deepcopy(backlog_tasks(gate_done=False))
    by_id = {task["id"]: task for task in tasks}
    decision = next_task_decision(tasks)
    assert decision.decision == "BLOCKED"
    assert "FND-071" in decision.blocking_dependencies


def test_new_work_inserted_before_current_takes_precedence():
    tasks = copy.deepcopy(backlog_tasks())
    first_platform = next(i for i, task in enumerate(tasks) if task["scope"] == "PLATFORM")
    tasks.insert(
        first_platform + 1,
        {
            "id": "PLT-099",
            "title": "Discovered prerequisite",
            "scope": "PLATFORM",
            "target_repo": "novo34/jev-platform",
            "priority": "P0",
            "status": "TODO",
            "depends_on": ["PLT-001"],
            "acceptance": ["prerequisite complete"],
        },
    )
    decision = next_task_decision(tasks)
    assert decision.selected_task_id == "PLT-099"


def test_done_requires_evidence_for_every_acceptance_criterion_and_verifier():
    task = {
        "id": "PLT-002",
        "acceptance": ["a", "b"],
    }
    try:
        validate_done_transition(
            task,
            completion_evidence=("proof-a",),
            verified_by="verifier",
        )
    except DevelopmentControlError as exc:
        assert "completion_evidence_incomplete" in str(exc)
        return
    raise AssertionError("partial acceptance evidence must fail")


def test_done_with_complete_evidence_and_verifier_passes():
    validate_done_transition(
        {"id": "PLT-002", "acceptance": ["a", "b"]},
        completion_evidence=("proof-a", "proof-b"),
        verified_by="verifier-independent-1",
    )
