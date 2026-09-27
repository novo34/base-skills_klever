from __future__ import annotations

from approvals.runtime import Approval
from orders.runtime import WorkOrder
from projects.runtime import Project


def build_project_view(
    *,
    project: Project,
    orders: list[WorkOrder],
    approvals: list[Approval],
    staging_status: str = "UNKNOWN",
    monthly_cost_chf: float = 0.0,
) -> dict:
    scoped_orders = [order for order in orders if order.project_id == project.project_id]
    scoped_order_ids = {order.order_id for order in scoped_orders}

    return {
        "project_id": project.project_id,
        "name": project.name,
        "status": project.status,
        "repository": project.repository,
        "branches": {
            "production": project.production_branch,
            "staging": project.staging_branch,
        },
        "urls": {
            "production": project.production_url,
            "staging": project.staging_url,
        },
        "staging": {
            "status": staging_status,
            "database_enabled": project.staging_database_enabled,
        },
        "orders": {
            "total": len(scoped_orders),
            "by_status": {
                status: sum(1 for order in scoped_orders if order.status == status)
                for status in sorted({order.status for order in scoped_orders})
            },
        },
        "approvals_pending": sum(
            1
            for approval in approvals
            if approval.task_id in scoped_order_ids and approval.status == "PENDING"
        ),
        "budget": {
            "monthly_limit_chf": project.monthly_budget_chf,
            "month_cost_chf": round(float(monthly_cost_chf), 2),
        },
        "models": {
            "allowed": list(project.allowed_models),
            "default": project.default_model,
        },
    }
