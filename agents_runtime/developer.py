from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from models.gateway import ModelGateway
from models.gateway_contract import ModelRequest
from workspaces.service import WorkspaceService


@dataclass(frozen=True)
class DeveloperTask:
    task_id: str
    project_id: str
    repository: str
    branch: str
    workspace_id: str
    objective: str
    acceptance_criteria: tuple[str, ...]
    provider: str
    model: str
    fallback_chain: tuple[tuple[str, str], ...] = ()


class DeveloperAgent:
    def __init__(
        self,
        *,
        gateway: ModelGateway,
        workspaces: WorkspaceService,
    ):
        self.gateway = gateway
        self.workspaces = workspaces

    def build_prompt(self, task: DeveloperTask) -> str:
        criteria = "\n".join(f"- {item}" for item in task.acceptance_criteria)
        return (
            f"Task: {task.task_id}\n"
            f"Objective: {task.objective}\n"
            f"Acceptance criteria:\n{criteria}\n"
            "Return an implementation plan and the minimal commands/files needed. "
            "Do not claim completion without tests."
        )

    def plan(self, task: DeveloperTask) -> dict[str, Any]:
        response = self.gateway.execute(
            ModelRequest(
                request_id=f"MODEL-{task.task_id}-PLAN",
                project_id=task.project_id,
                task_id=task.task_id,
                agent_role="developer",
                provider=task.provider,
                model=task.model,
                prompt=self.build_prompt(task),
            ),
            fallback_chain=task.fallback_chain,
        )
        return {
            "task_id": task.task_id,
            "provider": response.provider,
            "model": response.model,
            "content": response.content,
            "usage": response.usage,
        }

    def execute_commands(
        self,
        task: DeveloperTask,
        commands: tuple[str, ...],
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for command in commands:
            result = self.workspaces.execute(task.workspace_id, command)
            results.append({"command": command, "result": result})
        return results

    def collect_diff(self, task: DeveloperTask) -> dict[str, Any]:
        return self.workspaces.collect_diff(task.workspace_id)
