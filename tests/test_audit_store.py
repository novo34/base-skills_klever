import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from audit.runtime import AuditEvent
from audit.store import AuditStore


def event(event_id="AUD-1"):
    return AuditEvent(
        event_id=event_id,
        actor="owner",
        actor_type="human",
        action="APPROVE_TASK",
        project_id="espacore",
        object_type="order",
        object_id="ORD-1",
        task_id="TASK-1",
        result="SUCCESS",
        timestamp="2026-09-27T10:00:00+02:00",
        approval_id="APR-1",
        rationale="Manual staging review passed",
    )


def test_audit_event_can_be_appended_and_queried():
    store = AuditStore()
    store.append(event())
    result = store.list(project_id="espacore")
    assert len(result) == 1
    assert result[0].action == "APPROVE_TASK"


def test_duplicate_audit_event_is_rejected():
    store = AuditStore()
    store.append(event())
    try:
        store.append(event())
    except ValueError as exc:
        assert "duplicate_audit_event" in str(exc)
        return
    raise AssertionError("duplicate audit event must fail")


def test_audit_events_are_immutable():
    store = AuditStore()
    store.append(event())
    try:
        store.delete("AUD-1")
    except PermissionError as exc:
        assert "audit_events_are_immutable" in str(exc)
        return
    raise AssertionError("audit deletion must fail")
