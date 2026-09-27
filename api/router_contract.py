from __future__ import annotations

ROUTES = {
    "GET /api/dashboard": "GET_DASHBOARD",
    "GET /api/projects/{project_id}": "GET_PROJECT_STATUS",
    "GET /api/projects/{project_id}/report": "GET_REPORT",
    "POST /api/projects/{project_id}/orders": "CREATE_ORDER",
    "POST /api/projects/{project_id}/pause": "PAUSE_PROJECT",
    "POST /api/projects/{project_id}/resume": "RESUME_PROJECT",
    "POST /api/projects/{project_id}/budget": "SET_BUDGET",
    "POST /api/projects/{project_id}/orders/{order_id}/retry": "RETRY_TASK",
    "POST /api/projects/{project_id}/orders/{order_id}/audit": "REQUEST_AUDIT",
    "POST /api/projects/{project_id}/orders/{order_id}/approve": "APPROVE_TASK",
    "POST /api/projects/{project_id}/orders/{order_id}/request-changes": "REQUEST_CHANGES",
    "POST /api/projects/{project_id}/orders/{order_id}/reject": "REJECT_TASK",
}


def resolve_route(method: str, route_template: str) -> str:
    key = f"{method.upper()} {route_template}"
    if key not in ROUTES:
        raise KeyError("api_route_not_registered")
    return ROUTES[key]
