from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    notification_id: str
    project_id: str
    category: str
    severity: str
    title: str
    message: str
    target_type: str
    target_id: str
    status: str = "UNREAD"
    action_url: str | None = None
    created_at: str | None = None


ALLOWED_CATEGORIES = {
    "APPROVAL_REQUIRED",
    "STAGING_READY",
    "CRITICAL_FAILURE",
    "BUDGET_WARNING",
    "BUDGET_STOP",
    "VERIFICATION_FAILED",
    "TASK_BLOCKED",
}

ALLOWED_SEVERITIES = {"INFO", "WARNING", "CRITICAL"}


def validate_notification(notification: Notification) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if not notification.notification_id:
        failures.append("notification_id_missing")
    if not notification.project_id:
        failures.append("project_id_missing")
    if notification.category not in ALLOWED_CATEGORIES:
        failures.append("invalid_notification_category")
    if notification.severity not in ALLOWED_SEVERITIES:
        failures.append("invalid_notification_severity")
    if not notification.title:
        failures.append("title_missing")
    if not notification.message:
        failures.append("message_missing")
    if notification.status not in {"UNREAD", "READ", "DISMISSED"}:
        failures.append("invalid_notification_status")
    return not failures, failures
