from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentAssignment:
    task_id: str
    agent_role: str
    dependency_ids: tuple[str, ...] = ()
    resource_locks: tuple[str, ...] = ()
    status: str = "PENDING"


class MultiAgentCoordinator:
    def __init__(self):
        self._assignments: dict[tuple[str, str], AgentAssignment] = {}

    def assign(self, assignment: AgentAssignment) -> AgentAssignment:
        key = (assignment.task_id, assignment.agent_role)
        if key in self._assignments:
            raise ValueError("assignment_already_exists")

        active_locks = {
            lock
            for current in self._assignments.values()
            if current.status in {"PENDING", "RUNNING"}
            for lock in current.resource_locks
        }
        conflict = active_locks.intersection(assignment.resource_locks)
        if conflict:
            raise ValueError("resource_lock_conflict:" + ",".join(sorted(conflict)))

        self._assignments[key] = assignment
        return assignment

    def list_task(self, task_id: str) -> list[AgentAssignment]:
        return [
            item for item in self._assignments.values()
            if item.task_id == task_id
        ]
