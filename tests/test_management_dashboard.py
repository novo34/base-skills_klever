import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from approvals.runtime import request_approval
from management.dashboard import build_dashboard
from orders.runtime import WorkOrder
from projects.runtime import Project


def project(project_id, status):
    return Project(
        project_id=project_id,
        name=project_id.title(),
        repository=f"novo34/{project_id}",
        status=status,
        production_branch="main",
        staging_branch="staging",
        staging_database_enabled=status == "ACTIVE",
        staging_url="https://staging.example" if status == "ACTIVE" else None,
        allowed_models=("deepseek",),
        default_model="deepseek",
    )


def test_dashboard_summarizes_management_state():
    projects = [
        project("espacore", "ACTIVE"),
        project("nuvurent", "SETUP"),
    ]
    orders = [
        WorkOrder("ORD-1", "espacore", "A", "A", status="RUNNING"),
        WorkOrder("ORD-2", "espacore", "B", "B", status="AWAITING_HUMAN"),
        WorkOrder("ORD-3", "espacore", "C", "C", status="BLOCKED"),
    ]
    approvals = [
        request_approval(
            "APR-1",
            "ORD-2",
            "MERGE_PULL_REQUEST",
            "integrator",
            staging_evidence_id="STG-EV-ORD-2",
            staging_url="https://staging.example",
            staging_revision="rev-1",
            source_pr=2,
            source_commit="commit-ord-2",
            requested_at="2026-09-27T18:00:00Z",
        ),
    ]

    dashboard = build_dashboard(
        projects=projects,
        orders=orders,
        approvals=approvals,
        monthly_cost_chf=12.345,
    )

    assert dashboard["projects"]["total"] == 2
    assert dashboard["projects"]["active"] == 1
    assert dashboard["orders"]["active"] == 2
    assert dashboard["orders"]["blocked"] == 1
    assert dashboard["approvals"]["pending"] == 1
    assert dashboard["costs"]["month_chf"] == 12.35
