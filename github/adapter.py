from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class GitHubAdapter(ABC):
    @abstractmethod
    def get_repository(self, repository: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def create_branch(self, repository: str, branch: str, base_branch: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def write_file(self, repository: str, branch: str, path: str, content: str,
                   message: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def create_pull_request(self, repository: str, branch: str, base_branch: str,
                            title: str, body: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def read_checks(self, repository: str, ref: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def merge_pull_request(self, repository: str, pull_request: int) -> dict[str, Any]:
        raise NotImplementedError
