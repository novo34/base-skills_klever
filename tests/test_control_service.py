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
