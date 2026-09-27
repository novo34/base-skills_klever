from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ActorContext:
    actor_id: str
    role: str
    project_ids: tuple[str, ...] = ()


def can_access_project(actor: ActorContext, project_id: str) -> bool:
    if actor.role == "ADMIN":
        return True
    return project_id in actor.project_ids
