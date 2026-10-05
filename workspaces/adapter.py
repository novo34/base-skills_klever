from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class WorkspaceAdapter(ABC):
    @abstractmethod
    def create(self, spec: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def clone_repository(self, workspace_id: str, repository: str, branch: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def install(self, workspace_id: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def execute(self, workspace_id: str, command: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def collect_diff(self, workspace_id: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def destroy(self, workspace_id: str) -> dict[str, Any]:
        raise NotImplementedError
