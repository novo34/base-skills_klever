import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from budgets.model_guard import BudgetPolicyMissingError, BudgetSnapshot, ModelBudgetGuard
from budgets.runtime import BudgetPolicy
from budgets.service import BudgetExceededError
from models.gateway import ModelGateway
from models.gateway_contract import (
    ModelProviderAdapter,
    ModelRequest,
    ModelResponse,
    ModelUsage,
    ProviderHealth,
)
from models.provider_registry import ProviderRegistry
from notifications.service import NotificationService


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
            usage=ModelUsage(total_tokens=10, estimated_cost_chf=1.0),
        )

    def health(self):
        return ProviderHealth(ok=True)


def request():
    return ModelRequest(
        request_id="MR-BUDGET",
        project_id="espacore",
        task_id="TASK-B",
        agent_role="developer",
        provider="deepseek",
        model="code",
        prompt="x",
    )


def test_hard_stop_prevents_provider_call():
    provider = CountingProvider()
    registry = ProviderRegistry()
    registry.register("deepseek", provider)

    guard = ModelBudgetGuard(
        policy_provider=lambda project_id: BudgetPolicy(
            project_id=project_id,
            task_limit_chf=5.0,
            hard_stop=True,
        ),
        spend_provider=lambda project_id, task_id: BudgetSnapshot(task_spend_chf=4.8),
        estimator=lambda req: 0.5,
    )

    gateway = ModelGateway(registry, budget_guard=guard)

    try:
        gateway.execute(request())
    except BudgetExceededError:
        pass
    else:
        raise AssertionError("budget hard stop should block model call")

    assert provider.calls == 0


def test_budget_warning_creates_notification_before_call():
    provider = CountingProvider()
    registry = ProviderRegistry()
    registry.register("deepseek", provider)
    notifications = NotificationService()

    guard = ModelBudgetGuard(
        policy_provider=lambda project_id: BudgetPolicy(
            project_id=project_id,
            task_limit_chf=10.0,
            warning_threshold_pct=80.0,
            hard_stop=True,
        ),
        spend_provider=lambda project_id, task_id: BudgetSnapshot(task_spend_chf=8.0),
        estimator=lambda req: 0.5,
        notifications=notifications,
    )

    response = ModelGateway(registry, budget_guard=guard).execute(request())

    assert response.content == "ok"
    assert provider.calls == 1
    items = notifications.list(project_id="espacore")
    assert len(items) == 1
    assert items[0].category == "BUDGET_WARNING"


def test_missing_policy_blocks_model_call():
    provider = CountingProvider()
    registry = ProviderRegistry()
    registry.register("deepseek", provider)

    guard = ModelBudgetGuard(
        policy_provider=lambda project_id: None,
        spend_provider=lambda project_id, task_id: BudgetSnapshot(),
        estimator=lambda req: 999.0,
    )

    try:
        ModelGateway(registry, budget_guard=guard).execute(request())
    except BudgetPolicyMissingError as exc:
        assert "budget_policy_required:espacore" in str(exc)
    else:
        raise AssertionError("missing budget policy must fail closed")
    assert provider.calls == 0
