from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class StagingDeploymentRequest:
    project_id: str
    task_id: str
    repository_id: str
    repository: str
    source_branch: str
    staging_branch: str
    staging_url: str
    database_ref: str
    environment_kind: str = "PERMANENT_STAGING"
    secret_refs: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StagingStepResult:
    ok: bool
    detail: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class StagingProviderAdapter(ABC):
    @abstractmethod
    def deploy(self, request: StagingDeploymentRequest) -> StagingStepResult:
        raise NotImplementedError

    @abstractmethod
    def verify_database(self, request: StagingDeploymentRequest) -> StagingStepResult:
        raise NotImplementedError

    @abstractmethod
    def apply_migrations(self, request: StagingDeploymentRequest) -> StagingStepResult:
        raise NotImplementedError

    @abstractmethod
    def seed_test_data(self, request: StagingDeploymentRequest) -> StagingStepResult:
        raise NotImplementedError

    @abstractmethod
    def health_check(self, request: StagingDeploymentRequest) -> StagingStepResult:
        raise NotImplementedError

    @abstractmethod
    def run_online_e2e(self, request: StagingDeploymentRequest) -> StagingStepResult:
        raise NotImplementedError
