from __future__ import annotations

import argparse
import json
import pathlib
import sys
import yaml

try:
    from scripts.development_control import (
        DevelopmentControlError,
        assert_start_allowed,
        next_task_decision,
    )
except ModuleNotFoundError:
    from development_control import (
        DevelopmentControlError,
        assert_start_allowed,
        next_task_decision,
    )

ROOT = pathlib.Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "backlog" / "jev-master-tasks.yaml"


def load_tasks() -> list[dict]:
    data = yaml.safe_load(BACKLOG.read_text(encoding="utf-8")) or {}
    return list(data.get("tasks") or [])


def as_dict(decision) -> dict:
    return {
        "scope": decision.scope,
        "decision": decision.decision,
        "selected_task_id": decision.selected_task_id,
        "first_incomplete_task_id": decision.first_incomplete_task_id,
        "blocking_dependencies": list(decision.blocking_dependencies),
        "unauthorized_active_tasks": list(decision.unauthorized_active_tasks),
        "requires_operator_authorization": decision.requires_operator_authorization,
        "reason": decision.reason,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve/enforce the canonical next JEV backlog task."
    )
    parser.add_argument("--scope", default="PLATFORM")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--expect")
    parser.add_argument("--authorize-task")
    args = parser.parse_args()

    tasks = load_tasks()
    decision = next_task_decision(tasks, scope=args.scope)

    if args.expect and decision.selected_task_id != args.expect:
        print(json.dumps(as_dict(decision), indent=2))
        print(
            f"ERROR: expected NEXT_TASK {args.expect}, "
            f"resolved {decision.selected_task_id}",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.authorize_task:
        try:
            assert_start_allowed(
                tasks,
                requested_task_id=args.authorize_task,
                operator_authorized_task_id=args.authorize_task,
                scope=args.scope,
            )
        except DevelopmentControlError as exc:
            print(json.dumps(as_dict(decision), indent=2))
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(1)

    if args.check and decision.decision == "INVALID":
        print(json.dumps(as_dict(decision), indent=2))
        sys.exit(1)

    print(json.dumps(as_dict(decision), indent=2))


if __name__ == "__main__":
    main()
