from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    actor: str
    actor_type: str
    action: str
    project_id: str
    object_type: str
    object_id: str
    result: str
    timestamp: str
    task_id: str | None = None
    risk: str | None = None
    model: str | None = None
    provider: str | None = None
    cost_chf: float | None = None
    approval_id: str | None = None
    rationale: str | None = None
    metadata: dict | None = None


def validate_audit_event(event: AuditEvent) -> tuple[bool, list[str]]:
    failures: list[str] = []
    required = {
        "event_id": event.event_id,
        "actor": event.actor,
        "actor_type": event.actor_type,
        "action": event.action,
        "project_id": event.project_id,
        "object_type": event.object_type,
        "object_id": event.object_id,
        "result": event.result,
        "timestamp": event.timestamp,
    }
    for name, value in required.items():
        if not value:
            failures.append(f"{name}_missing")

    if event.cost_chf is not None and event.cost_chf < 0:
        failures.append("negative_cost")

    return not failures, failures
