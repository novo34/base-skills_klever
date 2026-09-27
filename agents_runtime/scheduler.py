from __future__ import annotations

from dataclasses import dataclass, replace


class SchedulerError(RuntimeError):
    pass


@dataclass(frozen=True)
class ScheduledAssignment:
    assignment_id: str
    task_id: str
    agent_role: str
    dependency_ids: tuple[str, ...] = ()
    status: str = "PENDING"


ALLOWED_ASSIGNMENT_STATES = {
    "PENDING",
    "RUNNING",
    "COMPLETED",
    "FAILED",
    "BLOCKED",
}


class DependencyScheduler:
    def __init__(self):
        self._items: dict[str, ScheduledAssignment] = {}

    def add(self, item: ScheduledAssignment) -> ScheduledAssignment:
        if not item.assignment_id:
            raise SchedulerError("assignment_id_required")
        if item.assignment_id in self._items:
            raise SchedulerError("assignment_already_exists")
        if item.assignment_id in item.dependency_ids:
            raise SchedulerError("self_dependency_forbidden")
        if item.status not in ALLOWED_ASSIGNMENT_STATES:
            raise SchedulerError("invalid_assignment_status")
        self._items[item.assignment_id] = item
        return item

    def validate_graph(self) -> None:
        for item in self._items.values():
            for dependency in item.dependency_ids:
                if dependency not in self._items:
                    raise SchedulerError(
                        f"unknown_dependency:{item.assignment_id}:{dependency}"
                    )

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str, path: tuple[str, ...]) -> None:
            if node in visited:
                return
            if node in visiting:
                raise SchedulerError(
                    "dependency_cycle:" + "->".join(path + (node,))
                )
            visiting.add(node)
            for dependency in self._items[node].dependency_ids:
                visit(dependency, path + (node,))
            visiting.remove(node)
            visited.add(node)

        for assignment_id in sorted(self._items):
            visit(assignment_id, ())

    def refresh_blocks(self) -> tuple[ScheduledAssignment, ...]:
        self.validate_graph()
        changed: list[ScheduledAssignment] = []

        for assignment_id in sorted(self._items):
            item = self._items[assignment_id]
            if item.status != "PENDING":
                continue

            dependencies = [
                self._items[dependency]
                for dependency in item.dependency_ids
            ]
            if any(dep.status in {"FAILED", "BLOCKED"} for dep in dependencies):
                updated = replace(item, status="BLOCKED")
                self._items[assignment_id] = updated
                changed.append(updated)

        return tuple(changed)

    def runnable(self) -> tuple[ScheduledAssignment, ...]:
        self.validate_graph()
        self.refresh_blocks()

        runnable = []
        for assignment_id in sorted(self._items):
            item = self._items[assignment_id]
            if item.status != "PENDING":
                continue
            dependencies = [
                self._items[dependency]
                for dependency in item.dependency_ids
            ]
            if all(dep.status == "COMPLETED" for dep in dependencies):
                runnable.append(item)

        return tuple(runnable)

    def transition(self, assignment_id: str, status: str) -> ScheduledAssignment:
        if assignment_id not in self._items:
            raise SchedulerError("assignment_not_found")
        if status not in ALLOWED_ASSIGNMENT_STATES:
            raise SchedulerError("invalid_assignment_status")

        current = self._items[assignment_id]
        allowed = {
            "PENDING": {"RUNNING", "BLOCKED"},
            "RUNNING": {"COMPLETED", "FAILED", "BLOCKED"},
            "COMPLETED": set(),
            "FAILED": set(),
            "BLOCKED": set(),
        }
        if status not in allowed[current.status]:
            raise SchedulerError(
                f"invalid_assignment_transition:{current.status}->{status}"
            )

        if status == "RUNNING":
            runnable_ids = {item.assignment_id for item in self.runnable()}
            if assignment_id not in runnable_ids:
                raise SchedulerError("assignment_dependencies_not_satisfied")

        updated = replace(current, status=status)
        self._items[assignment_id] = updated
        if status in {"FAILED", "BLOCKED"}:
            self.refresh_blocks()
        return updated

    def get(self, assignment_id: str) -> ScheduledAssignment:
        if assignment_id not in self._items:
            raise SchedulerError("assignment_not_found")
        return self._items[assignment_id]

    def list(self) -> tuple[ScheduledAssignment, ...]:
        return tuple(self._items[key] for key in sorted(self._items))
