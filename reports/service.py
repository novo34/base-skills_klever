from __future__ import annotations

from collections import Counter

from approvals.runtime import Approval
from costs.ledger import CostLedger
from orders.runtime import WorkOrder
from projects.runtime import Project


class ReportService:
    def __init__(self, costs: CostLedger):
        self.costs = costs

    def project_report(
        self,
        *,
        project: Project,
        orders: list[WorkOrder],
        approvals: list[Approval],
    ) -> dict:
        scoped_orders = [o for o in orders if o.project_id == project.project_id]
        statuses = Counter(o.status for o in scoped_orders)
        order_ids = {o.order_id for o in scoped_orders}
        scoped_approvals = [a for a in approvals if a.task_id in order_ids]

        spent = self.costs.project_total(project.project_id)
        limit = project.monthly_budget_chf
        remaining = None if limit is None else round(limit - spent, 2)

        return {
            "project": {
                "project_id": project.project_id,
                "name": project.name,
                "status": project.status,
                "repository": project.repository,
            },
            "work": {
                "orders_total": len(scoped_orders),
                "by_status": dict(sorted(statuses.items())),
                "completed": statuses.get("DONE", 0),
                "blocked": statuses.get("BLOCKED", 0),
                "awaiting_human": statuses.get("AWAITING_HUMAN", 0),
            },
            "approvals": {
                "pending": sum(1 for a in scoped_approvals if a.status == "PENDING"),
                "changes_requested": sum(
                    1 for a in scoped_approvals if a.status == "CHANGES_REQUESTED"
                ),
                "approved": sum(1 for a in scoped_approvals if a.status == "APPROVED"),
                "rejected": sum(1 for a in scoped_approvals if a.status == "REJECTED"),
            },
            "costs": {
                "total_chf": spent,
                "budget_chf": limit,
                "remaining_chf": remaining,
                "by_provider": self.costs.provider_totals(project_id=project.project_id),
            },
        }
