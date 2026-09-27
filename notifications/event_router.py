from __future__ import annotations

from events.runtime import OperationalEvent
from notifications.runtime import Notification
from notifications.service import NotificationService


EVENT_MAP = {
    "STAGING_READY": ("STAGING_READY", "INFO"),
    "APPROVAL_REQUIRED": ("APPROVAL_REQUIRED", "WARNING"),
    "VERIFICATION_FAILED": ("VERIFICATION_FAILED", "WARNING"),
    "TASK_BLOCKED": ("TASK_BLOCKED", "WARNING"),
    "BUDGET_WARNING": ("BUDGET_WARNING", "WARNING"),
    "BUDGET_STOP": ("BUDGET_STOP", "CRITICAL"),
    "CRITICAL_FAILURE": ("CRITICAL_FAILURE", "CRITICAL"),
}


class NotificationEventRouter:
    def __init__(self, notifications: NotificationService):
        self.notifications = notifications

    def handle(self, event: OperationalEvent) -> Notification | None:
        mapped = EVENT_MAP.get(event.event_type)
        if mapped is None:
            return None

        category, severity = mapped
        notification = Notification(
            notification_id=f"N-{event.event_id}",
            project_id=event.project_id,
            category=category,
            severity=severity,
            title=event.title,
            message=event.message,
            target_type=event.target_type,
            target_id=event.target_id,
            action_url=event.action_url,
        )

        try:
            return self.notifications.create(notification)
        except ValueError as exc:
            if "notification_already_exists" in str(exc):
                return None
            raise
