from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from budgets.runtime import BudgetPolicy
from budgets.service import BudgetService
from models.gateway_contract import ModelRequest
from notifications.runtime import Notification
from notifications.service import NotificationService


@dataclass(frozen=True)
class BudgetSnapshot:
    month_spend_chf: float = 0.0
    day_spend_chf: float = 0.0
    task_spend_chf: float = 0.0


class ModelBudgetGuard:
    def __init__(
        self,
        *,
        policy_provider: Callable[[str], BudgetPolicy | None],
        spend_provider: Callable[[str, str], BudgetSnapshot],
        estimator: Callable[[ModelRequest], float],
        notifications: NotificationService | None = None,
        service: BudgetService | None = None,
    ):
        self.policy_provider = policy_provider
        self.spend_provider = spend_provider
        self.estimator = estimator
        self.notifications = notifications
        self.service = service or BudgetService()

    def before_call(self, request: ModelRequest) -> dict:
        policy = self.policy_provider(request.project_id)
        if policy is None:
            return {
                "allowed": True,
                "exceeded": [],
                "warnings": [],
                "projected": {},
            }

        snapshot = self.spend_provider(request.project_id, request.task_id)
        estimated = max(0.0, float(self.estimator(request)))
        result = self.service.require_budget(
            policy=policy,
            month_spend_chf=snapshot.month_spend_chf,
            day_spend_chf=snapshot.day_spend_chf,
            task_spend_chf=snapshot.task_spend_chf,
            estimated_next_cost_chf=estimated,
        )

        if result["warnings"] and self.notifications is not None:
            notification = Notification(
                notification_id=f"N-BUDGET-{request.project_id}-{request.task_id}",
                project_id=request.project_id,
                category="BUDGET_WARNING",
                severity="WARNING",
                title="Budget threshold reached",
                message="Budget warning before model execution",
                target_type="task",
                target_id=request.task_id,
            )
            try:
                self.notifications.create(notification)
            except ValueError as exc:
                if "notification_already_exists" not in str(exc):
                    raise

        return result


class NoLimitModelBudgetGuard:
    def before_call(self, request: ModelRequest) -> dict:
        return {
            "allowed": True,
            "exceeded": [],
            "warnings": [],
            "projected": {},
        }
