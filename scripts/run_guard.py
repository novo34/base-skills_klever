from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Limits:
    max_actions: int
    max_retries: int
    max_cost_usd: float


@dataclass(frozen=True)
class Usage:
    actions: int = 0
    retries: int = 0
    cost_usd: float = 0.0


def check_limits(limits: Limits, usage: Usage) -> tuple[bool, str]:
    if usage.actions >= limits.max_actions:
        return False, "max_actions_reached"
    if usage.retries >= limits.max_retries and limits.max_retries >= 0:
        if usage.retries > 0 or limits.max_retries == 0:
            return False, "max_retries_reached"
    if usage.cost_usd >= limits.max_cost_usd:
        return False, "max_cost_reached"
    return True, "ok"


def can_take_action(limits: Limits, usage: Usage, estimated_cost_usd: float = 0.0) -> tuple[bool, str]:
    ok, reason = check_limits(limits, usage)
    if not ok:
        return ok, reason
    if usage.cost_usd + max(estimated_cost_usd, 0.0) > limits.max_cost_usd:
        return False, "estimated_cost_exceeds_budget"
    return True, "ok"
