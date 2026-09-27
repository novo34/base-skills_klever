from __future__ import annotations

from audit.runtime import AuditEvent
from audit.store import AuditStore


class AuditService:
    def __init__(self, store: AuditStore):
        self.store = store

    def record(
        self,
        *,
        event_id: str,
        actor: str,
        actor_type: str,
        action: str,
        project_id: str,
        object_type: str,
        object_id: str,
        result: str,
        timestamp: str,
        task_id: str | None = None,
        approval_id: str | None = None,
        rationale: str | None = None,
        metadata: dict | None = None,
    ) -> AuditEvent:
        return self.store.append(AuditEvent(
            event_id=event_id,
            actor=actor,
            actor_type=actor_type,
            action=action,
            project_id=project_id,
            object_type=object_type,
            object_id=object_id,
            task_id=task_id,
            result=result,
            timestamp=timestamp,
            approval_id=approval_id,
            rationale=rationale,
            metadata=metadata,
        ))
