from __future__ import annotations

from authz.runtime import ActorContext
from budgets.model_guard import BudgetSnapshot, ModelBudgetGuard
from budgets.runtime import BudgetPolicy


def explicit_budget_guard():
    return ModelBudgetGuard(
        policy_provider=lambda project_id: BudgetPolicy(
            project_id=project_id,
            monthly_limit_chf=1000000.0,
            daily_limit_chf=1000000.0,
            task_limit_chf=1000000.0,
            hard_stop=True,
        ),
        spend_provider=lambda project_id, task_id: BudgetSnapshot(),
        estimator=lambda request: 0.0,
    )


def admin_actor(actor_id="owner", project_ids=()):
    return ActorContext(
        actor_id=actor_id,
        role="ADMIN",
        project_ids=tuple(project_ids),
    )
