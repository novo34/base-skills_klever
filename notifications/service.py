from __future__ import annotations

from notifications.runtime import Notification, validate_notification


class NotificationService:
    def __init__(self):
        self._items: dict[str, Notification] = {}

    def create(self, notification: Notification) -> Notification:
        ok, failures = validate_notification(notification)
        if not ok:
            raise ValueError(",".join(failures))
        if notification.notification_id in self._items:
            raise ValueError("notification_already_exists")
        self._items[notification.notification_id] = notification
        return notification

    def list(
        self,
        *,
        project_id: str | None = None,
        status: str | None = None,
        severity: str | None = None,
    ) -> list[Notification]:
        items = list(self._items.values())
        if project_id is not None:
            items = [n for n in items if n.project_id == project_id]
        if status is not None:
            items = [n for n in items if n.status == status]
        if severity is not None:
            items = [n for n in items if n.severity == severity]
        return items

    def mark_read(self, notification_id: str) -> Notification:
        current = self._items[notification_id]
        updated = Notification(**{**current.__dict__, "status": "READ"})
        self._items[notification_id] = updated
        return updated

    def dismiss(self, notification_id: str) -> Notification:
        current = self._items[notification_id]
        updated = Notification(**{**current.__dict__, "status": "DISMISSED"})
        self._items[notification_id] = updated
        return updated
