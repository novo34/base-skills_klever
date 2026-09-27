import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from audit.service import AuditService
from audit.store import AuditStore
from authz.runtime import ActorContext
from authz.service import AuthorizationService
from budgets.model_guard import BudgetSnapshot, ModelBudgetGuard
from budgets.registry import BudgetPolicyRegistry
from budgets.service import BudgetExceededError
from command_center.service import CommandCenter
from control.runtime import ControlCommand
from control.service import ControlService
from costs.ledger import CostLedger
from models.gateway import ModelGateway
from models.gateway_contract import (
    ModelProviderAdapter,
    ModelRequest,
    ModelResponse,
    ModelUsage,
    ProviderHealth,
)
from models.provider_registry import ProviderRegistry
from orders.service import WorkOrderService
from orchestrator.project_context import ProjectContextResolver
from projects.persistence import InMemoryProjectStore
from projects.runtime import Project
from projects.service import ProjectService
from reports.service import ReportService


class CountingProvider(ModelProviderAdapter):
    def __init__(self):
        self.calls = 0

    def execute(self, request):
        self.calls += 1
        return ModelResponse(
            request_id=request.request_id,
            provider=request.provider,
            model=request.model,
            content="ok",
            usage=ModelUsage(),
        )

    def health(self):
        return ProviderHealth(ok=True)


def control_with_budget():
    store = InMemoryProjectStore()
    projects = ProjectService(store)
    projects.register(Project(
        project_id="espacore",
        name="Espacore",
        repository="novo34/espacore",
        status="ACTIVE",
        production_branch="main",
        staging_branch="staging",
        staging_url="https://staging.example",
        staging_database_enabled=True,
        allowed_models=("deepseek",),
        default_model="deepseek",
    ))
    budgets = BudgetPolicyRegistry()
    audit_store = AuditStore()
    control = ControlService(
        projects=projects,
        orders=WorkOrderService(ProjectContextResolver(projects)),
        reports=ReportService(CostLedger()),
        budgets=budgets,
        audit=AuditService(audit_store),
        authorization=AuthorizationService(),
        clock=lambda: "2026-09-27T14:00:00+02:00",
    )
    return control, budgets, audit_store


def test_set_budget_control_action_is_authorized_and_audited():
    control, budgets, audit_store = control_with_budget()

    result = control.execute(
        ControlCommand(
            command_id="CMD-BUDGET-1",
            actor="owner",
            action="SET_BUDGET",
            project_id="espacore",
            payload={
                "monthly_limit_chf": 20.0,
                "daily_limit_chf": 10.0,
                "task_limit_chf": 5.0,
                "warning_threshold_pct": 80.0,
                "hard_stop": True,
            },
        ),
        actor_context=ActorContext(
            actor_id="owner",
            role="ADMIN",
        ),
    )

    assert result["budget"].monthly_limit_chf == 20.0
    assert budgets.require("espacore").task_limit_chf == 5.0
    events = audit_store.list(project_id="espacore")
    assert any(event.action == "SET_BUDGET" and event.result == "SUCCESS" for event in events)


def test_new_budget_is_seen_by_next_model_call():
    control, budgets, _ = control_with_budget()
    control.execute(
        ControlCommand(
            command_id="CMD-BUDGET-2",
            actor="owner",
            action="SET_BUDGET",
            project_id="espacore",
            payload={
                "task_limit_chf": 5.0,
                "hard_stop": True,
            },
        ),
        actor_context=ActorContext(
            actor_id="owner",
            role="ADMIN",
        ),
    )

    provider = CountingProvider()
    providers = ProviderRegistry()
    providers.register("deepseek", provider)
    guard = ModelBudgetGuard(
        policy_provider=budgets.get,
        spend_provider=lambda project_id, task_id: BudgetSnapshot(task_spend_chf=4.8),
        estimator=lambda request: 0.5,
    )
    gateway = ModelGateway(providers, budget_guard=guard)

    try:
        gateway.execute(ModelRequest(
            request_id="MR-AFTER-BUDGET",
            project_id="espacore",
            task_id="TASK-1",
            agent_role="developer",
            provider="deepseek",
            model="code",
            prompt="x",
        ))
    except BudgetExceededError:
        pass
    else:
        raise AssertionError("new budget must block the next paid model call")

    assert provider.calls == 0


def test_command_center_budget_still_requires_confirmation():
    center = CommandCenter()
    intent = center.interpret(
        intent_id="INT-B",
        actor="owner",
        text="No gastes más de CHF 20 en Espacore",
    )
    try:
        center.to_control_command(intent)
    except PermissionError as exc:
        assert "command_confirmation_required" in str(exc)
        return
    raise AssertionError("budget command must require confirmation")
