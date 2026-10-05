from __future__ import annotations

import argparse
import pathlib
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "backlog" / "jev-master-tasks.yaml"


def validate_release(release_task_id: str) -> list[str]:
    data = yaml.safe_load(BACKLOG.read_text(encoding="utf-8")) or {}
    tasks = data.get("tasks", [])
    by_id = {task["id"]: task for task in tasks}
    errors: list[str] = []

    release = by_id.get(release_task_id)
    if release is None:
        return [f"{release_task_id} release readiness task missing"]

    if release.get("scope") != "FOUNDATION":
        errors.append(f"{release_task_id} is not a FOUNDATION task")

    if release.get("status") != "DONE":
        errors.append(f"{release_task_id} release readiness is not DONE")

    for dependency in release.get("depends_on") or []:
        task = by_id.get(dependency)
        if task is None:
            errors.append(f"{release_task_id} unknown dependency: {dependency}")
        elif task.get("status") != "DONE":
            errors.append(
                f"{release_task_id} dependency not done: {dependency}"
            )

    required_docs = [
        ROOT / "docs" / "FOUNDATION_RELEASE_READINESS.md",
        ROOT / "docs" / "JEV_MASTER_BACKLOG.md",
        ROOT / "docs" / "JEV_EXECUTION_FLOW.md",
        ROOT / "docs" / "REQUIRED_GITHUB_SECURITY_SETTINGS.md",
        ROOT / ".github" / "CODEOWNERS",
    ]
    for required_path in required_docs:
        if not required_path.is_file():
            errors.append(
                f"required release document missing: {required_path.name}"
            )

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate one explicit JEV Foundation release-readiness gate."
    )
    parser.add_argument(
        "--release-task",
        default="FND-032",
        help=(
            "Release-readiness task to validate. During adaptive-foundation "
            "development CI validates the last approved release (FND-032); "
            "FND-070 is validated only when the new Foundation is ready."
        ),
    )
    args = parser.parse_args()

    errors = validate_release(args.release_task)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        sys.exit(1)

    print(
        f"OK: Foundation release gate {args.release_task} is satisfied "
        "with all declared dependencies DONE"
    )


if __name__ == "__main__":
    main()
