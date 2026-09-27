from __future__ import annotations

from typing import Any, Callable

from workspaces.adapter import WorkspaceAdapter


class DockerWorkspaceAdapter(WorkspaceAdapter):
    """
    Thin transport around a Docker executor.

    The executor performs already-authorized workspace operations. JEV policy
    lives in WorkspaceService/runtime, not in this adapter.
    """

    def __init__(self, executor: Callable[[str, dict[str, Any]], dict[str, Any]]):
        self.executor = executor

    def create(self, spec: dict[str, Any]) -> dict[str, Any]:
        return self.executor("CREATE", spec)

    def clone_repository(self, workspace_id: str, repository: str, branch: str) -> dict[str, Any]:
        return self.executor("CLONE", {
            "workspace_id": workspace_id,
            "repository": repository,
            "branch": branch,
        })

    def install(self, workspace_id: str) -> dict[str, Any]:
        return self.executor("INSTALL", {"workspace_id": workspace_id})

    def execute(self, workspace_id: str, command: str) -> dict[str, Any]:
        return self.executor("EXECUTE", {
            "workspace_id": workspace_id,
            "command": command,
        })

    def collect_diff(self, workspace_id: str) -> dict[str, Any]:
        return self.executor("COLLECT_DIFF", {"workspace_id": workspace_id})

    def destroy(self, workspace_id: str) -> dict[str, Any]:
        return self.executor("DESTROY", {"workspace_id": workspace_id})
