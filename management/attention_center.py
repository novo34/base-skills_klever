from __future__ import annotations

from notifications.runtime import Notification


def build_attention_center(notifications: list[Notification]) -> dict:
    active = [
        n for n in notifications
        if n.status == "UNREAD"
    ]

    critical = [n for n in active if n.severity == "CRITICAL"]
    warning = [n for n in active if n.severity == "WARNING"]
    info = [n for n in active if n.severity == "INFO"]

    ordered = critical + warning + info

    return {
        "total": len(ordered),
        "critical": len(critical),
        "warning": len(warning),
        "info": len(info),
        "items": [
            {
                "notification_id": n.notification_id,
                "project_id": n.project_id,
                "category": n.category,
                "severity": n.severity,
                "title": n.title,
                "message": n.message,
                "target_type": n.target_type,
                "target_id": n.target_id,
                "action_url": n.action_url,
            }
            for n in ordered
        ],
    }
