from __future__ import annotations

import pathlib
import re
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "backlog" / "jev-master-tasks.yaml"

data = yaml.safe_load(BACKLOG.read_text(encoding="utf-8")) or {}
tasks = data.get("tasks", [])

errors: list[str] = []
seen: set[str] = set()
valid_statuses = set(data.get("statuses", []))
valid_scopes = set(data.get("scopes", []))
valid_priorities = set(data.get("priorities", []))

for task in tasks:
    task_id = task.get("id")
    if not task_id or not re.match(r"^(FND|PLT)-\d{3}$", task_id):
        errors.append(f"invalid task id: {task_id}")
        continue
    if task_id in seen:
        errors.append(f"duplicate task id: {task_id}")
    seen.add(task_id)

    if task.get("status") not in valid_statuses:
        errors.append(f"{task_id}: invalid status {task.get('status')}")
    if task.get("scope") not in valid_scopes:
        errors.append(f"{task_id}: invalid scope {task.get('scope')}")
    if task.get("priority") not in valid_priorities:
        errors.append(f"{task_id}: invalid priority {task.get('priority')}")
    if not task.get("title"):
        errors.append(f"{task_id}: title missing")
    if not task.get("target_repo"):
        errors.append(f"{task_id}: target_repo missing")
    acceptance = task.get("acceptance") or []
    if not acceptance:
        errors.append(f"{task_id}: acceptance criteria missing")

for task in tasks:
    task_id = task.get("id")
    for dependency in task.get("depends_on") or []:
        if dependency not in seen:
            errors.append(f"{task_id}: unknown dependency {dependency}")
        if dependency == task_id:
            errors.append(f"{task_id}: self dependency forbidden")

graph = {
    task["id"]: list(task.get("depends_on") or [])
    for task in tasks
    if task.get("id") in seen
}
visiting: set[str] = set()
visited: set[str] = set()

def visit(node: str, path: list[str]) -> None:
    if node in visited:
        return
    if node in visiting:
        cycle = " -> ".join(path + [node])
        errors.append(f"dependency cycle: {cycle}")
        return
    visiting.add(node)
    for dep in graph.get(node, []):
        if dep in graph:
            visit(dep, path + [node])
    visiting.remove(node)
    visited.add(node)

for node in graph:
    visit(node, [])

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)

foundation = sum(1 for t in tasks if t.get("scope") == "FOUNDATION")
platform = sum(1 for t in tasks if t.get("scope") == "PLATFORM")
both = sum(1 for t in tasks if t.get("scope") == "BOTH")
print(
    f"OK: validated {len(tasks)} backlog tasks "
    f"(FOUNDATION={foundation}, PLATFORM={platform}, BOTH={both})"
)
