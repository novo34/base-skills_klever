from __future__ import annotations

import pathlib
import sys
import yaml

try:
    from scripts.development_control import ACTIVE, TERMINAL, next_task_decision
except ModuleNotFoundError:
    from development_control import ACTIVE, TERMINAL, next_task_decision

ROOT = pathlib.Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "backlog" / "jev-master-tasks.yaml"


def main() -> None:
    data = yaml.safe_load(BACKLOG.read_text(encoding="utf-8")) or {}
    tasks = list(data.get("tasks") or [])
    control = data.get("development_control") or {}
    errors: list[str] = []

    required = {
        "enabled": True,
        "controlled_scope": "PLATFORM",
        "order_source": "declaration_order",
        "require_operator_authorization_to_start": True,
        "require_completion_evidence_for_done": True,
        "new_task_policy": "INSERT_VIA_PLAN_REVISION",
        "skip_policy": "FORBIDDEN_WITHOUT_PLAN_REVISION",
        "max_active_tasks": 1,
    }
    for key, expected in required.items():
        if control.get(key) != expected:
            errors.append(
                f"development_control.{key} must be {expected!r}, "
                f"got {control.get(key)!r}"
            )

    if set(control.get("terminal_statuses") or []) != TERMINAL:
        errors.append("development_control terminal_statuses drift")
    if set(control.get("executable_statuses") or []) != ACTIVE:
        errors.append("development_control executable_statuses drift")
    if set(control.get("dependency_satisfied_statuses") or []) != {"DONE"}:
        errors.append("only DONE may satisfy dependencies")

    controlled_scope = control.get("controlled_scope", "PLATFORM")
    scoped = [task for task in tasks if task.get("scope") == controlled_scope]

    ids = [task.get("id") for task in scoped]
    if len(ids) != len(set(ids)):
        errors.append("controlled scope contains duplicate task ids")

    active = [task for task in scoped if task.get("status") in ACTIVE]
    if len(active) > int(control.get("max_active_tasks", 1)):
        errors.append(
            "more than one PLATFORM task is active: "
            + ",".join(task["id"] for task in active)
        )

    first = next(
        (task for task in scoped if task.get("status") not in TERMINAL),
        None,
    )
    if first and active and any(task["id"] != first["id"] for task in active):
        errors.append(
            "later task active before first non-terminal task: "
            f"first={first['id']} active={','.join(task['id'] for task in active)}"
        )

    if first:
        first_index = scoped.index(first)
        later_done = [
            task["id"]
            for task in scoped[first_index + 1 :]
            if task.get("status") == "DONE"
        ]
        if later_done:
            errors.append(
                "later task marked DONE before earlier non-terminal task: "
                f"first={first['id']} later_done={','.join(later_done)}"
            )

    epoch = control.get("completion_evidence_epoch_after")
    epoch_seen = False
    for task in scoped:
        if task.get("id") == epoch:
            epoch_seen = True
            continue
        if not epoch_seen:
            continue
        if task.get("status") == "DONE":
            evidence = task.get("completion_evidence") or []
            acceptance = task.get("acceptance") or []
            verified_by = task.get("verified_by")
            if len(evidence) < len(acceptance):
                errors.append(
                    f"{task['id']}: DONE requires completion_evidence "
                    "for every acceptance criterion"
                )
            if not verified_by:
                errors.append(f"{task['id']}: DONE requires verified_by")

    if epoch and not any(task.get("id") == epoch for task in scoped):
        errors.append(f"completion evidence epoch task missing: {epoch}")

    decision = next_task_decision(tasks, scope=controlled_scope)
    if decision.decision == "INVALID":
        errors.append(
            f"NEXT_TASK state invalid: {decision.reason}; "
            f"unauthorized_active={list(decision.unauthorized_active_tasks)}"
        )

    fnd071 = next((task for task in tasks if task.get("id") == "FND-071"), None)
    if not fnd071:
        errors.append("FND-071 development control gate task missing")

    plt002 = next((task for task in tasks if task.get("id") == "PLT-002"), None)
    if not plt002 or "FND-071" not in (plt002.get("depends_on") or []):
        errors.append("PLT-002 must depend on FND-071")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        sys.exit(1)

    print(
        "OK: Development Control Gate valid; "
        f"decision={decision.decision}; next={decision.selected_task_id}; "
        f"reason={decision.reason}"
    )


if __name__ == "__main__":
    main()
