from __future__ import annotations

from typing import Any

from github.adapter import GitHubAdapter
from github.runtime import (
    create_branch_command,
    create_pr_command,
    merge_pr_command,
    write_file_command,
)


class GitHubService:
    def __init__(self, adapter: GitHubAdapter):
        self.adapter = adapter

    def create_branch(self, *, repository: str, task_id: str, agent: str, risk: str,
                      branch: str, base_branch: str = "main") -> dict[str, Any]:
        command = create_branch_command(repository, task_id, agent, risk, branch, base_branch)
        return self.adapter.create_branch(
            command["repository"],
            command["branch"],
            command["payload"]["base_branch"],
        )

    def write_file(self, *, repository: str, task_id: str, agent: str, risk: str,
                   branch: str, path: str, content: str, message: str) -> dict[str, Any]:
        command = write_file_command(repository, task_id, agent, risk, branch, path, content)
        return self.adapter.write_file(
            command["repository"],
            command["branch"],
            command["payload"]["path"],
            command["payload"]["content"],
            message,
        )

    def create_pull_request(self, *, repository: str, task_id: str, agent: str, risk: str,
                            branch: str, base_branch: str = "main", title: str = "",
                            body: str = "") -> dict[str, Any]:
        command = create_pr_command(
            repository, task_id, agent, risk, branch, base_branch, title
        )
        return self.adapter.create_pull_request(
            command["repository"],
            command["branch"],
            command["payload"]["base_branch"],
            command["payload"]["title"],
            body,
        )

    def merge_pull_request(self, *, repository: str, task_id: str, agent: str, risk: str,
                           pull_request: int, verifier_passed: bool,
                           human_approved: bool = False) -> dict[str, Any]:
        command = merge_pr_command(
            repository, task_id, agent, risk, pull_request,
            verifier_passed=verifier_passed,
            human_approved=human_approved,
        )
        return self.adapter.merge_pull_request(
            command["repository"],
            command["payload"]["pull_request"],
        )
