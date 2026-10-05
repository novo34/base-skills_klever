from __future__ import annotations

from typing import Any, Callable

from github.adapter import GitHubAdapter


class ConnectorGitHubAdapter(GitHubAdapter):
    """
    Adapter for a GitHub connector/App transport.

    The injected executor is responsible only for performing an already-authorized
    operation. Policy decisions remain in JEV's GitHubService/runtime.
    """

    def __init__(self, executor: Callable[[str, dict[str, Any]], dict[str, Any]]):
        self.executor = executor

    def get_repository(self, repository: str) -> dict[str, Any]:
        return self.executor("GET_REPOSITORY", {"repository": repository})

    def create_branch(self, repository: str, branch: str, base_branch: str) -> dict[str, Any]:
        return self.executor("CREATE_BRANCH", {
            "repository": repository,
            "branch": branch,
            "base_branch": base_branch,
        })

    def write_file(self, repository: str, branch: str, path: str, content: str,
                   message: str) -> dict[str, Any]:
        return self.executor("WRITE_FILE", {
            "repository": repository,
            "branch": branch,
            "path": path,
            "content": content,
            "message": message,
        })

    def create_pull_request(self, repository: str, branch: str, base_branch: str,
                            title: str, body: str) -> dict[str, Any]:
        return self.executor("CREATE_PULL_REQUEST", {
            "repository": repository,
            "branch": branch,
            "base_branch": base_branch,
            "title": title,
            "body": body,
        })

    def read_checks(self, repository: str, ref: str) -> dict[str, Any]:
        return self.executor("READ_CHECKS", {
            "repository": repository,
            "ref": ref,
        })

    def merge_pull_request(self, repository: str, pull_request: int) -> dict[str, Any]:
        return self.executor("MERGE_PULL_REQUEST", {
            "repository": repository,
            "pull_request": pull_request,
        })
