from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class VerificationContext:
    task_id: str
    project_id: str
    repository: str
    ref: str
    staging_url: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CollectorResult:
    collector: str
    status: str
    detail: str | None = None
    evidence_ref: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.status == "PASS"

    @property
    def blocked(self) -> bool:
        return self.status == "BLOCKED"


class VerificationCollectors(ABC):
    @abstractmethod
    def collect_ci(self, context: VerificationContext) -> CollectorResult:
        raise NotImplementedError

    @abstractmethod
    def collect_unit(self, context: VerificationContext) -> CollectorResult:
        raise NotImplementedError

    @abstractmethod
    def collect_integration(self, context: VerificationContext) -> CollectorResult:
        raise NotImplementedError

    @abstractmethod
    def collect_e2e(self, context: VerificationContext) -> CollectorResult:
        raise NotImplementedError

    @abstractmethod
    def collect_diff(self, context: VerificationContext) -> CollectorResult:
        raise NotImplementedError

    @abstractmethod
    def collect_backend(self, context: VerificationContext) -> CollectorResult:
        raise NotImplementedError

    @abstractmethod
    def collect_frontend(self, context: VerificationContext) -> CollectorResult:
        raise NotImplementedError

    @abstractmethod
    def collect_database(self, context: VerificationContext) -> CollectorResult:
        raise NotImplementedError
