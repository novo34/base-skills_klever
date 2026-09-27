import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from control.runtime import ControlCommand
from control.service import ControlService
from costs.ledger import CostLedger
from orders.service import WorkOrderService
from orchestrator.project_context import ProjectContextResolver
from projects.persistence import InMemoryProjectStore
from projects.runtime import Project, ProjectRepository
from projects.service import ProjectService
from reports.service import ReportService


def services():
    store = InMemoryProjectStore()
    projects = ProjectService(store)
    projects.register(Project(
        project_id="espacore",
        name="Espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        status="ACTIVE",
        production_branch="main",
        staging_branch="staging",
        staging_url="https://staging.example",
        staging_database_enabled=True,
        allowed_models=("deepseek", "openai"),
        default_model="deepseek",
    ))
    orders = WorkOrderService(ProjectContextResolver(projects))
    reports = ReportService(CostLedger())
    return ControlService(projects=projects, orders=orders, reports=reports)


def test_control_layer_can_create_project_scoped_order():
    control = services()
    result = control.execute(ControlCommand(
        command_id="CMD-1",
        actor="owner",
        action="CREATE_ORDER",
        project_id="espacore",
        payload={
            "order_id": "ORD-100",
            "title": "Fix contact form",
            "description": "Repair validation and submission",
        },
    ))

    assert result["order"].order_id == "ORD-100"
    assert result["project"].repository == "novo34/rediseno-web-espacore-gmbh"


def test_control_layer_reads_project_status():
    control = services()
    result = control.execute(ControlCommand(
        command_id="CMD-2",
        actor="owner",
        action="GET_PROJECT_STATUS",
        project_id="espacore",
    ))

    assert result["status"] == "ACTIVE"
    assert result["repository"] == "novo34/rediseno-web-espacore-gmbh"


def test_pause_and_resume_project():
    control = services()
    paused = control.execute(ControlCommand(
        command_id="CMD-3",
        actor="owner",
        action="PAUSE_PROJECT",
        project_id="espacore",
    ))
    assert paused["project"].status == "PAUSED"

    resumed = control.execute(ControlCommand(
        command_id="CMD-4",
        actor="owner",
        action="RESUME_PROJECT",
        project_id="espacore",
    ))
    assert resumed["project"].status == "ACTIVE"


def test_approval_requires_awaiting_human_state():
    control = services()
    control.execute(ControlCommand(
        command_id="CMD-5",
        actor="owner",
        action="CREATE_ORDER",
        project_id="espacore",
        payload={
            "order_id": "ORD-200",
            "title": "Change",
            "description": "Change",
            "status": "RUNNING",
        },
    ))

    try:
        control.execute(ControlCommand(
            command_id="CMD-6",
            actor="owner",
            action="APPROVE_TASK",
            project_id="espacore",
            target_id="ORD-200",
        ))
    except ValueError as exc:
        assert "order_not_awaiting_human" in str(exc)
        return
    raise AssertionError("non-review order must not be approved")


def test_request_changes_and_retry_flow():
    control = services()
    control.execute(ControlCommand(
        command_id="CMD-7",
        actor="owner",
        action="CREATE_ORDER",
        project_id="espacore",
        payload={
            "order_id": "ORD-201",
            "title": "UI change",
            "description": "UI change",
            "status": "AWAITING_HUMAN",
        },
    ))

    changed = control.execute(ControlCommand(
        command_id="CMD-8",
        actor="owner",
        action="REQUEST_CHANGES",
        project_id="espacore",
        target_id="ORD-201",
    ))
    assert changed["order"].status == "CHANGES_REQUESTED"

    retried = control.execute(ControlCommand(
        command_id="CMD-9",
        actor="owner",
        action="RETRY_TASK",
        project_id="espacore",
        target_id="ORD-201",
    ))
    assert retried["order"].status == "QUEUED"


def test_request_audit_moves_order_to_verifying():
    control = services()
    control.execute(ControlCommand(
        command_id="CMD-10",
        actor="owner",
        action="CREATE_ORDER",
        project_id="espacore",
        payload={
            "order_id": "ORD-202",
            "title": "Audit me",
            "description": "Audit me",
            "status": "RUNNING",
        },
    ))

    result = control.execute(ControlCommand(
        command_id="CMD-11",
        actor="owner",
        action="REQUEST_AUDIT",
        project_id="espacore",
        target_id="ORD-202",
    ))
    assert result["order"].status == "VERIFYING"


def test_control_mutations_are_audited():
    from audit.service import AuditService
    from audit.store import AuditStore

    store = InMemoryProjectStore()
    projects = ProjectService(store)
    projects.register(Project(
        project_id="espacore",
        name="Espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        status="ACTIVE",
        production_branch="main",
        staging_branch="staging",
        staging_url="https://staging.example",
        staging_database_enabled=True,
        allowed_models=("deepseek", "openai"),
        default_model="deepseek",
    ))
    orders = WorkOrderService(ProjectContextResolver(projects))
    reports = ReportService(CostLedger())
    audit_store = AuditStore()
    control = ControlService(
        projects=projects,
        orders=orders,
        reports=reports,
        audit=AuditService(audit_store),
        clock=lambda: "2026-09-27T11:30:00+02:00",
    )

    control.execute(ControlCommand(
        command_id="CMD-AUD-1",
        actor="owner",
        action="PAUSE_PROJECT",
        project_id="espacore",
    ))

    events = audit_store.list(project_id="espacore")
    assert len(events) == 1
    assert events[0].action == "PAUSE_PROJECT"
    assert events[0].result == "SUCCESS"


def test_control_layer_enforces_role_permissions():
    from authz.runtime import ActorContext
    from authz.service import AuthorizationService

    store = InMemoryProjectStore()
    projects = ProjectService(store)
    projects.register(Project(
        project_id="espacore",
        name="Espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        status="ACTIVE",
        production_branch="main",
        staging_branch="staging",
        staging_url="https://staging.example",
        staging_database_enabled=True,
        allowed_models=("deepseek", "openai"),
        default_model="deepseek",
    ))
    orders = WorkOrderService(ProjectContextResolver(projects))
    reports = ReportService(CostLedger())
    control = ControlService(
        projects=projects,
        orders=orders,
        reports=reports,
        authorization=AuthorizationService(),
    )

    try:
        control.execute(
            ControlCommand(
                command_id="CMD-RBAC-1",
                actor="client1",
                action="PAUSE_PROJECT",
                project_id="espacore",
            ),
            actor_context=ActorContext(
                actor_id="client1",
                role="CLIENT",
                project_ids=("espacore",),
            ),
        )
    except PermissionError as exc:
        assert "action_not_allowed_for_role" in str(exc)
        return
    raise AssertionError("client must not pause project")


def test_control_layer_enforces_project_scope():
    from authz.runtime import ActorContext
    from authz.service import AuthorizationService

    store = InMemoryProjectStore()
    projects = ProjectService(store)
    projects.register(Project(
        project_id="espacore",
        name="Espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        status="ACTIVE",
        production_branch="main",
        staging_branch="staging",
        staging_url="https://staging.example",
        staging_database_enabled=True,
        allowed_models=("deepseek", "openai"),
        default_model="deepseek",
    ))
    orders = WorkOrderService(ProjectContextResolver(projects))
    reports = ReportService(CostLedger())
    control = ControlService(
        projects=projects,
        orders=orders,
        reports=reports,
        authorization=AuthorizationService(),
    )

    try:
        control.execute(
            ControlCommand(
                command_id="CMD-RBAC-2",
                actor="pm1",
                action="GET_PROJECT_STATUS",
                project_id="espacore",
            ),
            actor_context=ActorContext(
                actor_id="pm1",
                role="PROJECT_MANAGER",
                project_ids=("nuvurent",),
            ),
        )
    except PermissionError as exc:
        assert "project_access_denied" in str(exc)
        return
    raise AssertionError("project manager must not access unassigned project")


def test_denied_control_action_is_audited_as_blocked():
    from audit.service import AuditService
    from audit.store import AuditStore
    from authz.runtime import ActorContext
    from authz.service import AuthorizationService

    store = InMemoryProjectStore()
    projects = ProjectService(store)
    projects.register(Project(
        project_id="espacore",
        name="Espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        status="ACTIVE",
        production_branch="main",
        staging_branch="staging",
        staging_url="https://staging.example",
        staging_database_enabled=True,
        allowed_models=("deepseek",),
        default_model="deepseek",
    ))
    orders = WorkOrderService(ProjectContextResolver(projects))
    audit_store = AuditStore()
    control = ControlService(
        projects=projects,
        orders=orders,
        reports=ReportService(CostLedger()),
        audit=AuditService(audit_store),
        authorization=AuthorizationService(),
        clock=lambda: "2026-09-27T12:00:00+02:00",
    )

    try:
        control.execute(
            ControlCommand(
                command_id="CMD-DENIED",
                actor="client1",
                action="PAUSE_PROJECT",
                project_id="espacore",
            ),
            actor_context=ActorContext(
                actor_id="client1",
                role="CLIENT",
                project_ids=("espacore",),
            ),
        )
    except PermissionError:
        pass
    else:
        raise AssertionError("client action should be denied")

    events = audit_store.list(project_id="espacore")
    assert len(events) == 1
    assert events[0].result == "BLOCKED"
    assert "action_not_allowed_for_role" in (events[0].rationale or "")


def test_failed_domain_action_is_audited_as_failed():
    from audit.service import AuditService
    from audit.store import AuditStore

    store = InMemoryProjectStore()
    projects = ProjectService(store)
    projects.register(Project(
        project_id="espacore",
        name="Espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        status="ACTIVE",
        production_branch="main",
        staging_branch="staging",
        staging_url="https://staging.example",
        staging_database_enabled=True,
        allowed_models=("deepseek",),
        default_model="deepseek",
    ))
    orders = WorkOrderService(ProjectContextResolver(projects))
    orders.create(__import__("orders.runtime", fromlist=["WorkOrder"]).WorkOrder(
        order_id="ORD-FAIL",
        project_id="espacore",
        title="x",
        description="x",
        status="RUNNING",
    ))
    audit_store = AuditStore()
    control = ControlService(
        projects=projects,
        orders=orders,
        reports=ReportService(CostLedger()),
        audit=AuditService(audit_store),
        clock=lambda: "2026-09-27T12:00:00+02:00",
    )

    try:
        control.execute(ControlCommand(
            command_id="CMD-FAIL",
            actor="owner",
            action="APPROVE_TASK",
            project_id="espacore",
            target_id="ORD-FAIL",
        ))
    except ValueError:
        pass
    else:
        raise AssertionError("invalid approval state should fail")

    events = audit_store.list(project_id="espacore")
    assert len(events) == 1
    assert events[0].result == "FAILED"
    assert "order_not_awaiting_human" in (events[0].rationale or "")


def test_control_layer_passes_target_repository_for_multi_repo_order():
    store = InMemoryProjectStore()
    projects = ProjectService(store)
    projects.register(Project(
        project_id="multi",
        name="Multi",
        repository="novo34/multi-web",
        status="ACTIVE",
        production_branch="main",
        staging_branch="staging",
        staging_url="https://staging.multi.example",
        staging_database_enabled=True,
        allowed_models=("deepseek",),
        default_model="deepseek",
        repositories=(
            ProjectRepository(
                repository_id="web",
                full_name="novo34/multi-web",
                role="frontend",
                primary=True,
            ),
            ProjectRepository(
                repository_id="api",
                full_name="novo34/multi-api",
                role="backend",
                primary=False,
            ),
        ),
    ))
    control = ControlService(
        projects=projects,
        orders=WorkOrderService(ProjectContextResolver(projects)),
        reports=ReportService(CostLedger()),
    )

    result = control.execute(ControlCommand(
        command_id="CMD-MULTI",
        actor="owner",
        action="CREATE_ORDER",
        project_id="multi",
        payload={
            "order_id": "ORD-MULTI",
            "title": "Change API",
            "description": "Change API",
            "target_repository": "api",
        },
    ))

    assert result["order"].target_repository == "api"
    assert result["repository"].full_name == "novo34/multi-api"
