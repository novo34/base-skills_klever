from __future__ import annotations

from collections import Counter
from typing import Iterable

from approvals.runtime import Approval
from orders.runtime import WorkOrder
from projects.runtime import Project


def build_dashboard(
    *,
    projects: Iterable[Project],
    orders: Iterable[WorkOrder],
    approvals: Iterable[Approval],
    monthly_cost_chf: float = 0.0,
) -> dict:
    project_list = list(projects)
    order_list = list(orders)
    approval_list = list(approvals)

    project_counts = Counter(project.status for project in project_list)
    order_counts = Counter(order.status for order in order_list)

    active_orders = {
        "RUNNING",
        "VERIFYING",
        "STAGING",
        "AWAITING_HUMAN",
        "CHANGES_REQUESTED",
    }

    return {
        "projects": {
            "total": len(project_list),
            "active": project_counts.get("ACTIVE", 0),
            "setup": project_counts.get("SETUP", 0),
            "paused": project_counts.get("PAUSED", 0),
        },
        "orders": {
            "total": len(order_list),
            "active": sum(1 for order in order_list if order.status in active_orders),
            "blocked": order_counts.get("BLOCKED", 0),
            "awaiting_human": order_counts.get("AWAITING_HUMAN", 0),
            "changes_requested": order_counts.get("CHANGES_REQUESTED", 0),
            "done": order_counts.get("DONE", 0),
        },
        "approvals": {
            "pending": sum(1 for approval in approval_list if approval.status == "PENDING"),
            "approved": sum(1 for approval in approval_list if approval.status == "APPROVED"),
            "rejected": sum(1 for approval in approval_list if approval.status == "REJECTED"),
            "changes_requested": sum(
                1 for approval in approval_list if approval.status == "CHANGES_REQUESTED"
            ),
        },
        "costs": {
            "month_chf": round(float(monthly_cost_chf), 2),
        },
    }
