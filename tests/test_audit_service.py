import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from audit.service import AuditService
from audit.store import AuditStore


def test_audit_service_records_control_event():
    store = AuditStore()
    service = AuditService(store)
    service.record(
        event_id="AUD-CMD-1",
        actor="owner",
        actor_type="human",
        action="PAUSE_PROJECT",
        project_id="espacore",
        object_type="project",
        object_id="espacore",
        result="SUCCESS",
        timestamp="2026-09-27T11:00:00+02:00",
    )

    events = store.list(project_id="espacore")
    assert len(events) == 1
    assert events[0].action == "PAUSE_PROJECT"
