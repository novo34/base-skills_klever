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


    def update_status(self, order_id: str, status: str) -> WorkOrder:
        allowed = {
            "DRAFT", "QUEUED", "PLANNED", "RUNNING", "VERIFYING", "STAGING",
            "AWAITING_HUMAN", "CHANGES_REQUESTED", "APPROVED", "REJECTED",
            "DONE", "BLOCKED"
        }
        if status not in allowed:
            raise ValueError("invalid_order_status")

        current = self.get(order_id)
        updated = WorkOrder(**{**current.__dict__, "status": status})
        ok, failures = validate_order(updated)
        if not ok:
            raise ValueError(",".join(failures))
        self._orders[order_id] = updated
        return updated

    def retry(self, order_id: str) -> WorkOrder:
        current = self.get(order_id)
        if current.status not in {"BLOCKED", "CHANGES_REQUESTED", "REJECTED"}:
            raise ValueError("order_not_retryable")
        return self.update_status(order_id, "QUEUED")

    def request_audit(self, order_id: str) -> WorkOrder:
        current = self.get(order_id)
        if current.status in {"DONE"}:
            raise ValueError("completed_order_not_auditable_in_runtime")
        return self.update_status(order_id, "VERIFYING")
