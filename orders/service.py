from __future__ import annotations

from orders.runtime import WorkOrder, validate_order
from orchestrator.project_context import ProjectContextResolver


class WorkOrderService:
    def __init__(self, projects: ProjectContextResolver):
        self.projects = projects
        self._orders: dict[str, WorkOrder] = {}

    def create(self, order: WorkOrder) -> dict:
        ok, failures = validate_order(order)
        if not ok:
            raise ValueError(",".join(failures))
        if order.order_id in self._orders:
            raise ValueError("order_already_exists")

        context = self.projects.resolve(order.project_id)

        if (
            context.monthly_budget_chf is not None
            and order.budget_limit_chf is not None
            and order.budget_limit_chf > context.monthly_budget_chf
        ):
            raise ValueError("order_budget_exceeds_project_budget")

        self._orders[order.order_id] = order
        return {
            "order": order,
            "project": context,
        }

    def get(self, order_id: str) -> WorkOrder:
        if order_id not in self._orders:
            raise ValueError("order_not_found")
        return self._orders[order_id]
