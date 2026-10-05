import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from authz.runtime import ActorContext
from authz.service import AuthorizationService


def test_admin_can_access_any_project():
    AuthorizationService().require(
        ActorContext(actor_id="u1", role="ADMIN"),
        action="APPROVE_TASK",
        project_id="espacore",
    )


def test_client_cannot_approve_task():
    try:
        AuthorizationService().require(
            ActorContext(actor_id="client1", role="CLIENT", project_ids=("espacore",)),
            action="APPROVE_TASK",
            project_id="espacore",
        )
    except PermissionError as exc:
        assert "action_not_allowed_for_role" in str(exc)
        return
    raise AssertionError("client must not approve task")


def test_project_manager_cannot_access_unassigned_project():
    try:
        AuthorizationService().require(
            ActorContext(actor_id="pm1", role="PROJECT_MANAGER", project_ids=("espacore",)),
            action="GET_PROJECT_STATUS",
            project_id="nuvurent",
        )
    except PermissionError as exc:
        assert "project_access_denied" in str(exc)
        return
    raise AssertionError("project access must be scoped")
