from __future__ import annotations

from typing import Any

from github.service import GitHubService
from orchestrator.task_orchestrator import advance, create_task_execution
from workspaces.service import WorkspaceService


class ExecutionPipeline:
    def __init__(self, github: GitHubService, workspaces: WorkspaceService):
        self.github = github
        self.workspaces = workspaces

    def start_task(
        self,
        *,
        task_id: str,
        repository: str,
        branch: str,
        triggers: set[str],
        flags: set[str],
        workspace_id: str,
        developer_agent: str = "developer",
    ) -> dict[str, Any]:
        execution = create_task_execution(task_id, triggers, flags)
        risk = execution["plan"]["risk"]

        execution = advance(execution, "READY")

        self.github.create_branch(
            repository=repository,
            task_id=task_id,
            agent=developer_agent,
            risk=risk,
            branch=branch,
        )

        self.workspaces.provision(
            workspace_id=workspace_id,
            task_id=task_id,
            repository=repository,
            branch=branch,
        )

        execution = advance(execution, "RUNNING")
        execution["repository"] = repository
        execution["branch"] = branch
        execution["workspace_id"] = workspace_id
        return execution

    def run_command(self, execution: dict[str, Any], command: str) -> dict[str, Any]:
        result = self.workspaces.execute(execution["workspace_id"], command)
        return {
            "execution": execution,
            "command": command,
            "result": result,
        }

    def prepare_review(
        self,
        execution: dict[str, Any],
        *,
        title: str,
        body: str = "",
        developer_agent: str = "developer",
    ) -> dict[str, Any]:
        if execution["state"] != "RUNNING":
            raise RuntimeError("task_not_running")

        diff = self.workspaces.collect_diff(execution["workspace_id"])
        execution = advance(execution, "VERIFYING")

        pr = self.github.create_pull_request(
            repository=execution["repository"],
            task_id=execution["task_id"],
            agent=developer_agent,
            risk=execution["plan"]["risk"],
            branch=execution["branch"],
            title=title,
            body=body,
        )

        return {
            "execution": execution,
            "diff": diff,
            "pull_request": pr,
        }

    def complete_verification(
        self,
        execution: dict[str, Any],
        *,
        verification_passed: bool,
    ) -> dict[str, Any]:
        if not verification_passed:
            return advance(execution, "FAILED")

        return advance(
            execution,
            "VERIFIED",
            verification_passed=True,
        )

    def teardown(self, execution: dict[str, Any]) -> dict[str, Any]:
        return self.workspaces.teardown(execution["workspace_id"])
