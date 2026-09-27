from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ModelRequest:
    request_id: str
    project_id: str
    task_id: str
    agent_role: str
    provider: str
    model: str
    prompt: str
    max_output_tokens: int | None = None
    timeout_seconds: int = 120
    metadata: dict[str, Any] | None = None


@dataclass(frozen=True)
class ModelUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_chf: float = 0.0


@dataclass(frozen=True)
class ModelResponse:
    request_id: str
    provider: str
    model: str
    content: str
    usage: ModelUsage
    finish_reason: str | None = None
    raw_metadata: dict[str, Any] | None = None


class ModelProviderAdapter(ABC):
    @abstractmethod
    def execute(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError

    @abstractmethod
    def health(self) -> dict[str, Any]:
        raise NotImplementedError
