import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from events.runtime import OperationalEvent
from notifications.event_router import NotificationEventRouter
from notifications.service import NotificationService


def test_operational_event_creates_notification():
    service = NotificationService()
    router = NotificationEventRouter(service)

    created = router.handle(OperationalEvent(
        event_id="EV-1",
        project_id="espacore",
        event_type="STAGING_READY",
        target_type="order",
        target_id="ORD-1",
        title="Staging ready",
        message="Ready for manual review",
        action_url="https://staging.example",
    ))

    assert created is not None
    assert created.category == "STAGING_READY"
    assert created.action_url == "https://staging.example"


def test_duplicate_event_is_deduplicated():
    service = NotificationService()
    router = NotificationEventRouter(service)
    event = OperationalEvent(
        event_id="EV-2",
        project_id="espacore",
        event_type="TASK_BLOCKED",
        target_type="task",
        target_id="TASK-2",
        title="Task blocked",
        message="Dependency missing",
    )

    assert router.handle(event) is not None
    assert router.handle(event) is None
    assert len(service.list(project_id="espacore")) == 1


def test_budget_stop_maps_to_critical_notification():
    service = NotificationService()
    router = NotificationEventRouter(service)

    created = router.handle(OperationalEvent(
        event_id="EV-BUDGET",
        project_id="espacore",
        event_type="BUDGET_STOP",
        target_type="task",
        target_id="TASK-B",
        title="Budget stopped",
        message="Hard stop reached",
    ))

    assert created is not None
    assert created.severity == "CRITICAL"
