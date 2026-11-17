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


def backlog_tasks(
    *,
    gate_done: bool = True,
    plt002_status: str | None = None,
    plt003_status: str | None = None,
    plt004_status: str | None = None,
    plt005_status: str | None = None,
    plt006_status: str | None = None,
    plt007_status: str | None = None,
    plt008_status: str | None = None,
    plt009_status: str | None = None,
    status_overrides: dict[str, str] | None = None,
):
    data = yaml.safe_load(
        (ROOT / "backlog" / "jev-master-tasks.yaml").read_text(encoding="utf-8")
    ) or {}
    tasks = list(data["tasks"])
    by_id = {task["id"]: task for task in tasks}
    by_id["FND-071"]["status"] = "DONE" if gate_done else "TODO"
    if plt002_status is not None:
        by_id["PLT-002"]["status"] = plt002_status
    if plt003_status is not None:
        by_id["PLT-003"]["status"] = plt003_status
    if plt004_status is not None:
        by_id["PLT-004"]["status"] = plt004_status
    if plt005_status is not None:
        by_id["PLT-005"]["status"] = plt005_status
    if plt006_status is not None:
        by_id["PLT-006"]["status"] = plt006_status
    if plt007_status is not None:
        by_id["PLT-007"]["status"] = plt007_status
    if plt008_status is not None:
        by_id["PLT-008"]["status"] = plt008_status
    if plt009_status is not None:
        by_id["PLT-009"]["status"] = plt009_status
    for task_id, status in (status_overrides or {}).items():
        by_id[task_id]["status"] = status
    return tasks


def test_completed_plt_012_exposes_plt_052_without_authorizing_its_start():
    tasks = backlog_tasks()
    by_id = {task["id"]: task for task in tasks}
    assert by_id["PLT-010"]["status"] == "DONE"
    assert by_id["PLT-050"]["status"] == "DONE"
    assert by_id["PLT-051"]["status"] == "DONE"
    assert by_id["PLT-011"]["status"] == "DONE"
    assert by_id["PLT-012"]["status"] == "DONE"
    assert by_id["PLT-052"]["status"] == "TODO"
    decision = next_task_decision(tasks, scope="PLATFORM")
    assert decision.decision == "NEXT_TASK"
    assert decision.selected_task_id == "PLT-052"
    assert decision.reason == "first_incomplete_task_is_eligible"
    assert decision.requires_operator_authorization is True
    try:
        assert_start_allowed(
            tasks,
            requested_task_id="PLT-052",
            operator_authorized_task_id=None,
        )
    except DevelopmentControlError as exc:
        assert "operator_authorization_required" in str(exc)
        return
    raise AssertionError("closing PLT-012 must not authorize starting PLT-052")


def test_cannot_jump_from_next_task_to_later_task():
    try:
        assert_start_allowed(
            backlog_tasks(plt002_status="TODO", plt003_status="TODO", plt004_status="TODO", plt005_status="TODO", plt006_status="TODO", plt007_status="TODO", plt009_status="TODO"),
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
            backlog_tasks(plt002_status="TODO", plt003_status="TODO", plt004_status="TODO", plt005_status="TODO", plt006_status="TODO", plt007_status="TODO", plt009_status="TODO"),
            requested_task_id="PLT-002",
            operator_authorized_task_id=None,
        )
    except DevelopmentControlError as exc:
        assert "operator_authorization_required" in str(exc)
        return
    raise AssertionError("start without operator approval must fail")


def test_exact_next_task_can_be_authorized():
    decision = assert_start_allowed(
        backlog_tasks(plt002_status="TODO", plt003_status="TODO", plt004_status="TODO", plt005_status="TODO", plt006_status="TODO", plt007_status="TODO", plt009_status="TODO"),
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
    tasks = copy.deepcopy(backlog_tasks(plt003_status="TODO", plt004_status="TODO", plt005_status="TODO", plt006_status="TODO", plt007_status="TODO", plt009_status="TODO"))
    by_id = {task["id"]: task for task in tasks}
    by_id["PLT-002"]["status"] = "BLOCKED"
    decision = next_task_decision(tasks)
    assert decision.decision == "BLOCKED"
    assert decision.selected_task_id == "PLT-002"


def test_unsatisfied_dependency_blocks_first_task():
    tasks = copy.deepcopy(backlog_tasks(gate_done=False, plt002_status="TODO", plt003_status="TODO", plt004_status="TODO", plt005_status="TODO", plt006_status="TODO", plt007_status="TODO", plt009_status="TODO"))
    decision = next_task_decision(tasks)
    assert decision.decision == "BLOCKED"
    assert decision.selected_task_id == "PLT-002"
    assert "FND-071" in decision.blocking_dependencies


def test_new_work_inserted_before_current_takes_precedence():
    tasks = copy.deepcopy(backlog_tasks(plt003_status="TODO", plt004_status="TODO", plt005_status="TODO", plt006_status="TODO", plt007_status="TODO", plt009_status="TODO"))
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


def test_token_cost_priority_order_advances_next_task_in_chain():
    # Operator decision 2026-11-17 (novo34/jev-platform#37): token-cost priority.
    chain = ["PLT-052", "PLT-040", "PLT-041", "PLT-017", "PLT-042", "PLT-014"]
    tasks = backlog_tasks()
    pending = [t["id"] for t in tasks if t["scope"] == "PLATFORM" and t["status"] != "DONE"]
    assert pending[: len(chain)] == chain

    by_id = {t["id"]: t for t in tasks}
    assert by_id["PLT-052"]["depends_on"] == ["PLT-009"]
    assert by_id["PLT-052"]["status"] == "TODO"
    assert by_id["PLT-052"]["priority"] == "P0"

    done: dict[str, str] = {}
    for current, following in zip(chain, chain[1:]):
        done[current] = "DONE"
        decision = next_task_decision(
            backlog_tasks(status_overrides=dict(done)), scope="PLATFORM"
        )
        assert decision.decision == "NEXT_TASK", (current, decision)
        assert decision.selected_task_id == following
        assert decision.blocking_dependencies == ()
        assert decision.requires_operator_authorization is True


def test_no_task_in_new_order_depends_on_a_later_non_done_task():
    tasks = backlog_tasks()
    pending = [t for t in tasks if t["scope"] == "PLATFORM" and t["status"] != "DONE"]
    # Scope: the reprioritized chain PLT-052..PLT-014. Later tasks (e.g. PLT-035
    # depending on PLT-043..049) have pre-existing forward dependencies.
    pending = pending[:6]
    position = {t["id"]: i for i, t in enumerate(pending)}
    for task in pending:
        for dep in task.get("depends_on") or []:
            if dep in position:
                assert position[dep] < position[task["id"]], (task["id"], dep)


def test_plt_041_carries_bounded_context_pack_requirements():
    by_id = {t["id"]: t for t in backlog_tasks()}
    text = " ".join(by_id["PLT-041"]["acceptance"])
    assert "REQ-CTX-009" in text and "REQ-CTX-010" in text
