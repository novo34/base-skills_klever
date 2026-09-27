from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 2

    def __post_init__(self):
        if self.max_attempts < 1:
            raise ValueError("max_attempts_must_be_positive")
