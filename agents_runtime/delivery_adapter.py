from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from agents_runtime.edit_protocol import EditPlan


@dataclass(frozen=True)
class CommitResult:
    commit_sha: str
    branch: str
    metadata: dict[str, Any] | None = None


@dataclass(frozen=True)
class PullRequestResult:
    pull_request: int
    url: str | None = None
    metadata: dict[str, Any] | None = None


class DeveloperDeliveryAdapter(ABC):
    @abstractmethod
    def apply_edit_plan(self, workspace_id: str, edit_plan: EditPlan) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def commit_and_push(
        self,
        workspace_id: str,
        *,
        branch: str,
        message: str,
    ) -> CommitResult:
        raise NotImplementedError

    @abstractmethod
    def create_pull_request(
        self,
        *,
        repository: str,
        task_id: str,
        branch: str,
        base_branch: str,
        title: str,
        body: str,
    ) -> PullRequestResult:
        raise NotImplementedError
