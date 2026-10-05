from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from scripts.github_guard import authorize


class GitHubPolicyError(PermissionError):
    pass


@dataclass(frozen=True)
class GitHubCommand:
    operation: str
    repository: str
    task_id: str
    actor_agent: str
    risk: str
    branch: str | None = None
    payload: dict[str, Any] | None = None


def prepare_command(
    command: GitHubCommand,
    *,
    verifier_passed: bool = False,
    human_approved: bool = False,
) -> dict[str, Any]:
    ok, reason = authorize(
        command.operation,
        command.actor_agent,
        command.risk,
        branch=command.branch,
        verifier_passed=verifier_passed,
        human_approved=human_approved,
    )
    if not ok:
        raise GitHubPolicyError(reason)

    return {
        "operation": command.operation,
        "repository": command.repository,
        "task_id": command.task_id,
        "actor_agent": command.actor_agent,
        "risk": command.risk,
        "branch": command.branch,
        "payload": command.payload or {},
        "authorized": True,
        "policy_reason": "ok",
    }


def create_branch_command(repository: str, task_id: str, actor_agent: str, risk: str,
                          branch: str, base_branch: str = "main") -> dict[str, Any]:
    return prepare_command(GitHubCommand(
        operation="CREATE_BRANCH",
        repository=repository,
        task_id=task_id,
        actor_agent=actor_agent,
        risk=risk,
        branch=branch,
        payload={"base_branch": base_branch},
    ))


def write_file_command(repository: str, task_id: str, actor_agent: str, risk: str,
                       branch: str, path: str, content: str) -> dict[str, Any]:
    return prepare_command(GitHubCommand(
        operation="WRITE_FILE",
        repository=repository,
        task_id=task_id,
        actor_agent=actor_agent,
        risk=risk,
        branch=branch,
        payload={"path": path, "content": content},
    ))


def create_pr_command(repository: str, task_id: str, actor_agent: str, risk: str,
                      branch: str, base_branch: str = "main", title: str = "") -> dict[str, Any]:
    return prepare_command(GitHubCommand(
        operation="CREATE_PULL_REQUEST",
        repository=repository,
        task_id=task_id,
        actor_agent=actor_agent,
        risk=risk,
        branch=branch,
        payload={"base_branch": base_branch, "title": title},
    ))


def merge_pr_command(repository: str, task_id: str, actor_agent: str, risk: str,
                     pull_request: int, *, verifier_passed: bool,
                     human_approved: bool = False) -> dict[str, Any]:
    return prepare_command(
        GitHubCommand(
            operation="MERGE_PULL_REQUEST",
            repository=repository,
            task_id=task_id,
            actor_agent=actor_agent,
            risk=risk,
            payload={"pull_request": pull_request},
        ),
        verifier_passed=verifier_passed,
        human_approved=human_approved,
    )
