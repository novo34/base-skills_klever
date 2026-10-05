from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationalEvent:
    event_id: str
    project_id: str
    event_type: str
    target_type: str
    target_id: str
    title: str
    message: str
    action_url: str | None = None
    metadata: dict | None = None
