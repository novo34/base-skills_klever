from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


class DevelopmentControlError(ValueError):
    pass


TERMINAL = {"DONE", "DEFERRED"}
ACTIVE = {"READY", "IN_PROGRESS", "VERIFYING"}
ALLOWED_START = {"TODO", "READY"}


@dataclass(frozen=True)
class DevelopmentControlDecision:
    scope: str
    decision: str
    selected_task_id: str | None
    first_incomplete_task_id: str | None
    blocking_dependencies: tuple[str, ...]
    unauthorized_active_tasks: tuple[str, ...]
    requires_operator_authorization: bool
    reason: str


def _scope_tasks(tasks: Iterable[dict], scope: str) -> tuple[dict, ...]:
    return tuple(task for task in tasks if task.get("scope") == scope)


def next_task_decision(tasks: Iterable[dict], *, scope: str = "PLATFORM") -> DevelopmentControlDecision:
    scoped = _scope_tasks(tasks, scope)
    by_id = {task.get("id"): task for task in tasks}

    if not scoped:
        return DevelopmentControlDecision(
            scope=scope,
            decision="COMPLETE",
            selected_task_id=None,
            first_incomplete_task_id=None,
            blocking_dependencies=(),
            unauthorized_active_tasks=(),
            requires_operator_authorization=False,
            reason="no_tasks_in_scope",
        )

    first = next((task for task in scoped if task.get("status") not in TERMINAL), None)
    active = tuple(task for task in scoped if task.get("status") in ACTIVE)

    if first is None:
        if active:
            return DevelopmentControlDecision(
                scope=scope,
                decision="INVALID",
                selected_task_id=None,
                first_incomplete_task_id=None,
                blocking_dependencies=(),
                unauthorized_active_tasks=tuple(task["id"] for task in active),
                requires_operator_authorization=False,
                reason="active_task_exists_after_scope_complete",
            )
        return DevelopmentControlDecision(
            scope=scope,
            decision="COMPLETE",
            selected_task_id=None,
            first_incomplete_task_id=None,
            blocking_dependencies=(),
            unauthorized_active_tasks=(),
            requires_operator_authorization=False,
            reason="all_tasks_terminal",
        )

    first_id = first["id"]
    unauthorized_active = tuple(
        task["id"] for task in active if task["id"] != first_id
    )
    if len(active) > 1 or unauthorized_active:
        return DevelopmentControlDecision(
            scope=scope,
            decision="INVALID",
            selected_task_id=first_id,
            first_incomplete_task_id=first_id,
            blocking_dependencies=(),
            unauthorized_active_tasks=unauthorized_active or tuple(task["id"] for task in active[1:]),
            requires_operator_authorization=False,
            reason="later_or_multiple_active_tasks_forbidden",
        )

    blocking = tuple(
        dep for dep in first.get("depends_on") or []
        if by_id.get(dep, {}).get("status") != "DONE"
    )
    if blocking:
        return DevelopmentControlDecision(
            scope=scope,
            decision="BLOCKED",
            selected_task_id=first_id,
            first_incomplete_task_id=first_id,
            blocking_dependencies=blocking,
            unauthorized_active_tasks=(),
            requires_operator_authorization=False,
            reason="first_incomplete_task_has_unsatisfied_dependencies",
        )

    status = first.get("status")
    if status == "BLOCKED":
        return DevelopmentControlDecision(
            scope=scope,
            decision="BLOCKED",
            selected_task_id=first_id,
            first_incomplete_task_id=first_id,
            blocking_dependencies=(),
            unauthorized_active_tasks=(),
            requires_operator_authorization=False,
            reason="first_incomplete_task_is_blocked",
        )

    if status in ACTIVE:
        return DevelopmentControlDecision(
            scope=scope,
            decision="ACTIVE_TASK",
            selected_task_id=first_id,
            first_incomplete_task_id=first_id,
            blocking_dependencies=(),
            unauthorized_active_tasks=(),
            requires_operator_authorization=False,
            reason=f"current_task_{status.lower()}",
        )

    if status == "TODO":
        return DevelopmentControlDecision(
            scope=scope,
            decision="NEXT_TASK",
            selected_task_id=first_id,
            first_incomplete_task_id=first_id,
            blocking_dependencies=(),
            unauthorized_active_tasks=(),
            requires_operator_authorization=True,
            reason="first_incomplete_task_is_eligible",
        )

    return DevelopmentControlDecision(
        scope=scope,
        decision="INVALID",
        selected_task_id=first_id,
        first_incomplete_task_id=first_id,
        blocking_dependencies=(),
        unauthorized_active_tasks=(),
        requires_operator_authorization=False,
        reason=f"unsupported_non_terminal_status:{status}",
    )


def assert_start_allowed(
    tasks: Iterable[dict],
    *,
    requested_task_id: str,
    operator_authorized_task_id: str | None,
    scope: str = "PLATFORM",
) -> DevelopmentControlDecision:
    decision = next_task_decision(tasks, scope=scope)
    if decision.decision != "NEXT_TASK":
        raise DevelopmentControlError(
            f"task_start_not_allowed:{decision.decision}:{decision.reason}"
        )
    if requested_task_id != decision.selected_task_id:
        raise DevelopmentControlError(
            f"task_jump_forbidden:{requested_task_id}!={decision.selected_task_id}"
        )
    if operator_authorized_task_id != requested_task_id:
        raise DevelopmentControlError(
            "operator_authorization_required_for_exact_next_task"
        )
    return decision


def validate_done_transition(
    task: dict,
    *,
    completion_evidence: Iterable[str],
    verified_by: str | None,
) -> None:
    evidence = tuple(item for item in completion_evidence if str(item).strip())
    criteria = tuple(task.get("acceptance") or ())
    if not criteria:
        raise DevelopmentControlError("acceptance_criteria_required")
    if len(evidence) < len(criteria):
        raise DevelopmentControlError(
            f"completion_evidence_incomplete:{len(evidence)}<{len(criteria)}"
        )
    if not verified_by or not verified_by.strip():
        raise DevelopmentControlError("independent_verification_metadata_required")
