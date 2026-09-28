from __future__ import annotations

import pathlib
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "backlog" / "jev-master-tasks.yaml"

data = yaml.safe_load(BACKLOG.read_text(encoding="utf-8")) or {}
tasks = data.get("tasks", [])
by_id = {task["id"]: task for task in tasks}

errors: list[str] = []

foundation_tasks = [
    task for task in tasks
    if str(task.get("id", "")).startswith("FND-")
    and task.get("id") != "FND-032"
]

not_done = [
    task["id"]
    for task in foundation_tasks
    if task.get("status") != "DONE"
]
if not_done:
    errors.append(
        "foundation tasks not done: " + ", ".join(sorted(not_done))
    )

p0_not_done = [
    task["id"]
    for task in tasks
    if str(task.get("id", "")).startswith("FND-")
    and task.get("priority") == "P0"
    and task.get("id") != "FND-032"
    and task.get("status") != "DONE"
]
if p0_not_done:
    errors.append(
        "foundation P0 release blockers remain: "
        + ", ".join(sorted(p0_not_done))
    )

release = by_id.get("FND-032")
if release is None:
    errors.append("FND-032 release readiness task missing")
else:
    for dependency in release.get("depends_on") or []:
        task = by_id.get(dependency)
        if task is None:
            errors.append(f"FND-032 unknown dependency: {dependency}")
        elif task.get("status") != "DONE":
            errors.append(
                f"FND-032 dependency not done: {dependency}"
            )

required_docs = [
    ROOT / "docs" / "FOUNDATION_RELEASE_READINESS.md",
    ROOT / "docs" / "JEV_MASTER_BACKLOG.md",
    ROOT / "docs" / "JEV_EXECUTION_FLOW.md",
    ROOT / "docs" / "REQUIRED_GITHUB_SECURITY_SETTINGS.md",
    ROOT / ".github" / "CODEOWNERS",
]
for path in required_docs:
    if not path.is_file():
        errors.append(f"required release document missing: {path.name}")

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)

print(
    f"OK: foundation release prerequisites satisfied "
    f"({len(foundation_tasks)} completed FOUNDATION tasks)"
)
