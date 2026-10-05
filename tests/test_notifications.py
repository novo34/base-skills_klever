import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from management.attention_center import build_attention_center
from notifications.runtime import Notification
from notifications.service import NotificationService


def test_attention_center_prioritizes_critical_items():
    service = NotificationService()
    service.create(Notification(
        notification_id="N-1",
        project_id="espacore",
        category="STAGING_READY",
        severity="INFO",
        title="Staging ready",
        message="Ready for manual review",
        target_type="order",
        target_id="ORD-1",
    ))
    service.create(Notification(
        notification_id="N-2",
        project_id="espacore",
        category="CRITICAL_FAILURE",
        severity="CRITICAL",
        title="Critical failure",
        message="Production gate failed",
        target_type="task",
        target_id="TASK-2",
    ))

    center = build_attention_center(service.list(status="UNREAD"))
    assert center["total"] == 2
    assert center["critical"] == 1
    assert center["items"][0]["notification_id"] == "N-2"


def test_read_notification_leaves_attention_center():
    service = NotificationService()
    service.create(Notification(
        notification_id="N-3",
        project_id="espacore",
        category="APPROVAL_REQUIRED",
        severity="WARNING",
        title="Approval required",
        message="Manual approval required",
        target_type="order",
        target_id="ORD-3",
    ))
    service.mark_read("N-3")
    center = build_attention_center(service.list(status="UNREAD"))
    assert center["total"] == 0
