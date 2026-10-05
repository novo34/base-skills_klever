from __future__ import annotations

from budgets.runtime import BudgetPolicy, validate_policy


class BudgetExceededError(RuntimeError):
    pass


class BudgetService:
    def evaluate(
        self,
        *,
        policy: BudgetPolicy,
        month_spend_chf: float,
        day_spend_chf: float,
        task_spend_chf: float,
        estimated_next_cost_chf: float = 0.0,
    ) -> dict:
        ok, failures = validate_policy(policy)
        if not ok:
            raise ValueError(",".join(failures))

        projected_month = month_spend_chf + estimated_next_cost_chf
        projected_day = day_spend_chf + estimated_next_cost_chf
        projected_task = task_spend_chf + estimated_next_cost_chf

        limits = {
            "monthly": (projected_month, policy.monthly_limit_chf),
            "daily": (projected_day, policy.daily_limit_chf),
            "task": (projected_task, policy.task_limit_chf),
        }

        exceeded = [
            name for name, (spend, limit) in limits.items()
            if limit is not None and spend > limit
        ]

        warnings = []
        for name, (spend, limit) in limits.items():
            if limit is None or limit == 0:
                continue
            pct = (spend / limit) * 100
            if pct >= policy.warning_threshold_pct:
                warnings.append(name)

        allowed = not exceeded or not policy.hard_stop

        return {
            "allowed": allowed,
            "exceeded": exceeded,
            "warnings": warnings,
            "projected": {
                "monthly_chf": round(projected_month, 2),
                "daily_chf": round(projected_day, 2),
                "task_chf": round(projected_task, 2),
            },
        }

    def require_budget(
        self,
        *,
        policy: BudgetPolicy,
        month_spend_chf: float,
        day_spend_chf: float,
        task_spend_chf: float,
        estimated_next_cost_chf: float = 0.0,
    ) -> dict:
        result = self.evaluate(
            policy=policy,
            month_spend_chf=month_spend_chf,
            day_spend_chf=day_spend_chf,
            task_spend_chf=task_spend_chf,
            estimated_next_cost_chf=estimated_next_cost_chf,
        )
        if not result["allowed"]:
            raise BudgetExceededError(
                "budget_hard_stop:" + ",".join(result["exceeded"])
            )
        return result
