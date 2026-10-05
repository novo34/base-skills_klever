from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BudgetPolicy:
    project_id: str
    monthly_limit_chf: float | None = None
    daily_limit_chf: float | None = None
    task_limit_chf: float | None = None
    warning_threshold_pct: float = 80.0
    hard_stop: bool = True


def validate_policy(policy: BudgetPolicy) -> tuple[bool, list[str]]:
    failures: list[str] = []

    for name, value in {
        "monthly_limit_chf": policy.monthly_limit_chf,
        "daily_limit_chf": policy.daily_limit_chf,
        "task_limit_chf": policy.task_limit_chf,
    }.items():
        if value is not None and value < 0:
            failures.append(f"{name}_must_be_non_negative")

    if not 0 <= policy.warning_threshold_pct <= 100:
        failures.append("warning_threshold_pct_out_of_range")

    return not failures, failures
