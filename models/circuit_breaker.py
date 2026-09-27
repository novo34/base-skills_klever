from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CircuitState:
    failures: int = 0
    open: bool = False


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3):
        if failure_threshold < 1:
            raise ValueError("failure_threshold_must_be_positive")
        self.failure_threshold = failure_threshold
        self._states: dict[str, CircuitState] = {}

    def state(self, provider: str) -> CircuitState:
        return self._states.setdefault(provider, CircuitState())

    def allow(self, provider: str) -> bool:
        return not self.state(provider).open

    def success(self, provider: str) -> None:
        state = self.state(provider)
        state.failures = 0
        state.open = False

    def failure(self, provider: str) -> None:
        state = self.state(provider)
        state.failures += 1
        if state.failures >= self.failure_threshold:
            state.open = True
