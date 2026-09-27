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


def create_task_execution(task_id: str, triggers: set[str], flags: set[str]) -> dict:
    plan = build_plan(task_id, triggers, flags)
    return {
        "task_id": task_id,
        "state": "PLANNED",
        "plan": plan,
        "history": [{"from": None, "to": "PLANNED"}],
    }


def advance(
    execution: dict,
    target: str,
    *,
    verification_passed: bool = False,
    staging_ready: bool = False,
    human_approved: bool = False,
) -> dict:
    current = execution["state"]
    risk = execution["plan"]["risk"]
    new_state = transition(
        current,
        target,
        risk=risk,
        verification_passed=verification_passed,
        staging_ready=staging_ready,
        human_approved=human_approved,
    )
    result = dict(execution)
    result["state"] = new_state
    result["history"] = list(execution.get("history", [])) + [{"from": current, "to": new_state}]
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
