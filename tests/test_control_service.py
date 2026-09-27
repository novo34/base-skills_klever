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
from projects.runtime import Project
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
