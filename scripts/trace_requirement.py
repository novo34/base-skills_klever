from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

REQ_RE = re.compile(r"^REQ-[A-Z0-9]+-[0-9]{3,}$")


def build_record(
    requirement_id: str,
    source: str,
    status: str,
    task_id: str,
    branch: str,
    pull_request: int | None,
    files: list[str],
    unit_tests: list[str],
    integration_tests: list[str],
    e2e_tests: list[str],
    result: str,
) -> dict:
    if not REQ_RE.match(requirement_id):
        raise ValueError("requirement id must match REQ-<DOMAIN>-<NNN>")

    return {
        "id": requirement_id,
        "source": source,
        "status": status,
        "implementation": {
            "task_id": task_id,
            "branch": branch,
            "pull_request": pull_request,
            "files": sorted(set(files)),
        },
        "verification": {
            "unit_tests": sorted(set(unit_tests)),
            "integration_tests": sorted(set(integration_tests)),
            "e2e_tests": sorted(set(e2e_tests)),
            "result": result,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create/update a JEV requirement trace record.")
    parser.add_argument("--id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--status", default="PLANNED")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--pull-request", type=int)
    parser.add_argument("--files", default="")
    parser.add_argument("--unit-tests", default="")
    parser.add_argument("--integration-tests", default="")
    parser.add_argument("--e2e-tests", default="")
    parser.add_argument("--result", default="NOT_RUN")
    args = parser.parse_args()

    split = lambda value: [x.strip() for x in value.split(",") if x.strip()]

    record = build_record(
        args.id,
        args.source,
        args.status,
        args.task_id,
        args.branch,
        args.pull_request,
        split(args.files),
        split(args.unit_tests),
        split(args.integration_tests),
        split(args.e2e_tests),
        args.result,
    )

    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
