from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Callable


@dataclass
class CircuitState:
    failures: int = 0
    open: bool = False
    half_open: bool = False
    opened_at: float | None = None


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 3,
        *,
        reset_timeout_seconds: float = 60.0,
        clock: Callable[[], float] | None = None,
    ):
        if failure_threshold < 1:
            raise ValueError("failure_threshold_must_be_positive")
        if reset_timeout_seconds <= 0:
            raise ValueError("reset_timeout_must_be_positive")
        self.failure_threshold = failure_threshold
        self.reset_timeout_seconds = float(reset_timeout_seconds)
        self.clock = clock or time.monotonic
        self._states: dict[str, CircuitState] = {}

    def state(self, provider: str) -> CircuitState:
        return self._states.setdefault(provider, CircuitState())

    def allow(self, provider: str) -> bool:
        state = self.state(provider)
        if not state.open:
            return True

        if state.half_open:
            return False

        if state.opened_at is None:
            state.opened_at = self.clock()
            return False

        if self.clock() - state.opened_at >= self.reset_timeout_seconds:
            state.half_open = True
            return True

        return False

    def success(self, provider: str) -> None:
        state = self.state(provider)
        state.failures = 0
        state.open = False
        state.half_open = False
        state.opened_at = None

    def failure(self, provider: str) -> None:
        state = self.state(provider)
        state.failures += 1
        if state.failures >= self.failure_threshold or state.half_open:
            state.open = True
            state.half_open = False
            state.opened_at = self.clock()
