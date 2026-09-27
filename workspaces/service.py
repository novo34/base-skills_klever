from __future__ import annotations

from typing import Any

from workspaces.adapter import WorkspaceAdapter
from workspaces.runtime import Workspace, authorize_command, create_workspace, destroy, start


class WorkspaceService:
    def __init__(self, adapter: WorkspaceAdapter):
        self.adapter = adapter
        self._states: dict[str, Workspace] = {}

    def provision(
        self,
        *,
        workspace_id: str,
        task_id: str,
        repository: str,
        branch: str,
        isolation: str = "container",
        network_policy: str = "restricted",
        allowed_commands: set[str] | None = None,
        mounted_secrets: set[str] | None = None,
    ) -> dict[str, Any]:
        ws = create_workspace(
            workspace_id,
            task_id,
            repository,
            branch,
            isolation=isolation,
            network_policy=network_policy,
            allowed_commands=allowed_commands,
            mounted_secrets=mounted_secrets,
        )
        self._states[workspace_id] = ws

        result = self.adapter.create({
            "workspace_id": ws.workspace_id,
            "task_id": ws.task_id,
            "repository": ws.repository,
            "branch": ws.branch,
            "isolation": ws.isolation,
            "network_policy": ws.network_policy,
            "mounted_secrets": sorted(ws.mounted_secrets),
        })
        self.adapter.clone_repository(ws.workspace_id, ws.repository, ws.branch)
        self.adapter.install(ws.workspace_id)
        start(ws)
        return result

    def execute(self, workspace_id: str, command: str) -> dict[str, Any]:
        ws = self._states[workspace_id]
        ok, reason = authorize_command(ws, command)
        if not ok:
            raise PermissionError(reason)
        return self.adapter.execute(workspace_id, command)

    def collect_diff(self, workspace_id: str) -> dict[str, Any]:
        ws = self._states[workspace_id]
        if ws.status not in {"RUNNING", "READY"}:
            raise PermissionError("workspace_not_available")
        return self.adapter.collect_diff(workspace_id)

    def teardown(self, workspace_id: str) -> dict[str, Any]:
        ws = self._states[workspace_id]
        result = self.adapter.destroy(workspace_id)
        destroy(ws)
        return result

    def state(self, workspace_id: str) -> Workspace:
        return self._states[workspace_id]
