import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from approvals.runtime import request_approval
from costs.ledger import CostLedger
from costs.runtime import CostEvent
from orders.runtime import WorkOrder
from projects.runtime import Project
from reports.service import ReportService


def project():
    return Project(
        project_id="espacore",
        name="Espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        status="ACTIVE",
        production_branch="main",
        staging_branch="staging",
        staging_url="https://staging.example",
        staging_database_enabled=True,
        monthly_budget_chf=100.0,
        allowed_models=("deepseek", "openai"),
        default_model="deepseek",
    )


def test_cost_ledger_and_report():
    ledger = CostLedger()
    ledger.record(CostEvent(
        event_id="COST-1",
        project_id="espacore",
        task_id="ORD-1",
        provider="deepseek",
        model="deepseek-code",
        amount_chf=3.25,
    ))
    ledger.record(CostEvent(
        event_id="COST-2",
        project_id="espacore",
        task_id="ORD-1",
        provider="openai",
        model="premium",
        amount_chf=5.75,
    ))

    orders = [
        WorkOrder("ORD-1", "espacore", "A", "A", status="AWAITING_HUMAN"),
        WorkOrder("ORD-2", "espacore", "B", "B", status="DONE"),
    ]
    approvals = [
        request_approval(
            "APR-1",
            "ORD-1",
            "MERGE_PULL_REQUEST",
            "integrator",
            staging_evidence_id="STG-EV-ORD-1",
            staging_url="https://staging.example",
        )
    ]

    report = ReportService(ledger).project_report(
        project=project(),
        orders=orders,
        approvals=approvals,
    )

    assert report["costs"]["total_chf"] == 9.0
    assert report["costs"]["remaining_chf"] == 91.0
    assert report["costs"]["by_provider"]["deepseek"] == 3.25
    assert report["approvals"]["pending"] == 1
    assert report["work"]["completed"] == 1


def test_duplicate_cost_event_rejected():
    ledger = CostLedger()
    event = CostEvent(
        event_id="COST-X",
        project_id="espacore",
        task_id=None,
        provider="openai",
        model="premium",
        amount_chf=1.0,
    )
    ledger.record(event)
    try:
        ledger.record(event)
    except ValueError as exc:
        assert "duplicate_cost_event" in str(exc)
        return
    raise AssertionError("duplicate cost event must fail")
