from __future__ import annotations

from audit.runtime import AuditEvent, validate_audit_event


class AuditStore:
    def __init__(self):
        self._events: list[AuditEvent] = []
        self._ids: set[str] = set()

    def append(self, event: AuditEvent) -> AuditEvent:
        ok, failures = validate_audit_event(event)
        if not ok:
            raise ValueError(",".join(failures))
        if event.event_id in self._ids:
            raise ValueError("duplicate_audit_event")

        self._events.append(event)
        self._ids.add(event.event_id)
        return event

    def list(
        self,
        *,
        project_id: str | None = None,
        task_id: str | None = None,
        action: str | None = None,
    ) -> list[AuditEvent]:
        events = list(self._events)
        if project_id is not None:
            events = [e for e in events if e.project_id == project_id]
        if task_id is not None:
            events = [e for e in events if e.task_id == task_id]
        if action is not None:
            events = [e for e in events if e.action == action]
        return events

    def replace(self, event_id: str, event: AuditEvent) -> None:
        raise PermissionError("audit_events_are_immutable")

    def delete(self, event_id: str) -> None:
        raise PermissionError("audit_events_are_immutable")
