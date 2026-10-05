import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.architect import ArchitectAgent, ArchitectTask
from models.gateway import ModelGateway
from models.gateway_contract import (
    ModelProviderAdapter,
    ModelResponse,
    ModelUsage,
    ProviderHealth,
)
from models.provider_registry import ProviderRegistry
from tests.security_helpers import explicit_budget_guard


class FakeArchitectModel(ModelProviderAdapter):
    def execute(self, request):
        assert request.agent_role == "architect"
        assert "Do not modify code" in request.prompt
        return ModelResponse(
            request_id=request.request_id,
            provider=request.provider,
            model=request.model,
            content="ADR\nWORKPLAN\nRISK_ASSESSMENT",
            usage=ModelUsage(total_tokens=20, estimated_cost_chf=0.01),
        )

    def health(self):
        return ProviderHealth(ok=True)


def test_architect_returns_machine_consumable_output_without_code_action():
    registry = ProviderRegistry()
    registry.register("openai", FakeArchitectModel())
    agent = ArchitectAgent(gateway=ModelGateway(registry, budget_guard=explicit_budget_guard()))

    result = agent.plan(ArchitectTask(
        task_id="TASK-A1",
        project_id="espacore",
        objective="Design contact flow",
        constraints=("No direct main writes",),
        requirement_ids=("REQ-UI-001",),
        provider="openai",
        model="architect-model",
    ))

    assert result.task_id == "TASK-A1"
    assert "ADR" in result.adr
    assert result.provider == "openai"
