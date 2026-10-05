from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class WorkspacePolicyError(PermissionError):
    pass


@dataclass
class Workspace:
    workspace_id: str
    task_id: str
    repository: str
    branch: str
    isolation: str = "container"
    network_policy: str = "restricted"
    status: str = "CREATING"
    allowed_commands: set[str] = field(default_factory=set)
    mounted_secrets: set[str] = field(default_factory=set)


DEFAULT_ALLOWED = {
    "git status",
    "git diff",
    "git log",
    "pnpm install",
    "pnpm lint",
    "pnpm test",
    "pnpm build",
    "pytest",
}


def create_workspace(
    workspace_id: str,
    task_id: str,
    repository: str,
    branch: str,
    *,
    isolation: str = "container",
    network_policy: str = "restricted",
    allowed_commands: set[str] | None = None,
    mounted_secrets: set[str] | None = None,
) -> Workspace:
    if branch in {"main", "master"}:
        raise WorkspacePolicyError("workspace_branch_must_not_be_default_branch")
    if isolation not in {"container", "vm"}:
        raise WorkspacePolicyError("unsupported_isolation")
    if network_policy not in {"restricted", "standard", "offline"}:
        raise WorkspacePolicyError("unsupported_network_policy")

    return Workspace(
        workspace_id=workspace_id,
        task_id=task_id,
        repository=repository,
        branch=branch,
        isolation=isolation,
        network_policy=network_policy,
        status="READY",
        allowed_commands=set(allowed_commands or DEFAULT_ALLOWED),
        mounted_secrets=set(mounted_secrets or set()),
    )


def authorize_command(workspace: Workspace, command: str) -> tuple[bool, str]:
    if workspace.status not in {"READY", "RUNNING"}:
        return False, "workspace_not_runnable"
    if command not in workspace.allowed_commands:
        return False, "command_not_allowed"
    return True, "ok"


def start(workspace: Workspace) -> Workspace:
    if workspace.status != "READY":
        raise WorkspacePolicyError("workspace_not_ready")
    workspace.status = "RUNNING"
    return workspace


def destroy(workspace: Workspace) -> Workspace:
    if workspace.status == "DESTROYED":
        return workspace
    workspace.status = "DESTROYED"
    workspace.mounted_secrets.clear()
    return workspace
