from __future__ import annotations

ROLE_PERMISSIONS = {
    "ADMIN": {
        "CREATE_ORDER",
        "PAUSE_PROJECT",
        "RESUME_PROJECT",
        "APPROVE_TASK",
        "REQUEST_CHANGES",
        "REJECT_TASK",
        "RETRY_TASK",
        "REQUEST_AUDIT",
        "GET_PROJECT_STATUS",
        "GET_DASHBOARD",
        "GET_REPORT",
    },
    "PROJECT_MANAGER": {
        "CREATE_ORDER",
        "PAUSE_PROJECT",
        "RESUME_PROJECT",
        "REQUEST_CHANGES",
        "RETRY_TASK",
        "REQUEST_AUDIT",
        "GET_PROJECT_STATUS",
        "GET_DASHBOARD",
        "GET_REPORT",
    },
    "DEVELOPER": {
        "RETRY_TASK",
        "GET_PROJECT_STATUS",
        "GET_DASHBOARD",
    },
    "AUDITOR": {
        "REQUEST_AUDIT",
        "GET_PROJECT_STATUS",
        "GET_DASHBOARD",
        "GET_REPORT",
    },
    "CLIENT": {
        "GET_PROJECT_STATUS",
        "GET_REPORT",
    },
}


def authorize(role: str, action: str) -> tuple[bool, str]:
    permissions = ROLE_PERMISSIONS.get(role)
    if permissions is None:
        return False, "unknown_role"
    if action not in permissions:
        return False, "action_not_allowed_for_role"
    return True, "ok"
