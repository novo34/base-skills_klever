from __future__ import annotations

from authz.policy import authorize
from authz.runtime import ActorContext, can_access_project


class AuthorizationService:
    def require(self, actor: ActorContext, *, action: str, project_id: str) -> None:
        ok, reason = authorize(actor.role, action)
        if not ok:
            raise PermissionError(reason)
        if not can_access_project(actor, project_id):
            raise PermissionError("project_access_denied")
