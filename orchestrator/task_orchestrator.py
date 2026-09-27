from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "orchestrator"))

from plan_task import build_plan
from state_machine import transition, TransitionError
from events.runtime import OperationalEvent
from staging.runtime import Promotion


def create_task_execution(
    task_id: str,
    triggers: set[str],
    flags: set[str],
    *,
    project_id: str | None = None,
) -> dict:
    plan = build_plan(task_id, triggers, flags)
    result = {
        "task_id": task_id,
        "state": "PLANNED",
        "plan": plan,
        "history": [{"from": None, "to": "PLANNED"}],
    }
    if project_id is not None:
        result["project_id"] = project_id
    return result


def advance(
    execution: dict,
    target: str,
    *,
    verification_passed: bool = False,
    staging_ready: bool = False,
    human_approved: bool = False,
    production_promotion: Promotion | None = None,
    event_router=None,
) -> dict:
    current = execution["state"]
    risk = execution["plan"]["risk"]
    production_promoted = False
    if production_promotion is not None:
        if production_promotion.task_id != execution["task_id"]:
            raise TransitionError("production promotion task mismatch")
        production_promoted = production_promotion.status == "PROMOTED_TO_MAIN"

    new_state = transition(
        current,
        target,
        risk=risk,
        verification_passed=verification_passed,
        staging_ready=staging_ready,
        human_approved=human_approved,
        production_promoted=production_promoted,
    )
    result = dict(execution)
    result["state"] = new_state
    result["history"] = list(execution.get("history", [])) + [{"from": current, "to": new_state}]

    if new_state == "BLOCKED" and event_router is not None and execution.get("project_id"):
        event_router.handle(OperationalEvent(
            event_id=f'{execution["task_id"]}-BLOCKED-{len(result["history"])}',
            project_id=execution["project_id"],
            event_type="TASK_BLOCKED",
            target_type="task",
            target_id=execution["task_id"],
            title="Task blocked",
            message="The task entered a blocked state and needs attention.",
        ))

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a JEV task execution envelope.")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--triggers", default="")
    parser.add_argument("--flags", default="")
    args = parser.parse_args()

    split = lambda value: {x.strip() for x in value.split(",") if x.strip()}
    execution = create_task_execution(args.task_id, split(args.triggers), split(args.flags))
    print(json.dumps(execution, indent=2))


if __name__ == "__main__":
    main()
