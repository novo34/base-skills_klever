import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from models.circuit_breaker import CircuitBreaker
from models.gateway import ModelGateway
from models.gateway_contract import (
    ModelProviderAdapter,
    ModelRequest,
    ModelResponse,
    ModelUsage,
)
from models.provider_registry import ProviderRegistry
from models.usage import cost_event_from_response


class FakeProvider(ModelProviderAdapter):
    def __init__(self, *, fail=False, provider="fake"):
        self.fail = fail
        self.provider = provider
        self.calls = []

    def execute(self, request):
        self.calls.append(request)
        if self.fail:
            raise RuntimeError("provider_down")
        return ModelResponse(
            request_id=request.request_id,
            provider=request.provider,
            model=request.model,
            content="ok",
            usage=ModelUsage(
                input_tokens=100,
                output_tokens=50,
                total_tokens=150,
                estimated_cost_chf=0.25,
            ),
            finish_reason="stop",
        )

    def health(self):
        return {"ok": not self.fail}


def request(provider="deepseek", model="model-a"):
    return ModelRequest(
        request_id="MR-1",
        project_id="espacore",
        task_id="TASK-1",
        agent_role="developer",
        provider=provider,
        model=model,
        prompt="Implement task",
    )


def test_gateway_executes_primary_provider():
    registry = ProviderRegistry()
    registry.register("deepseek", FakeProvider(provider="deepseek"))

    response = ModelGateway(registry).execute(request())

    assert response.provider == "deepseek"
    assert response.content == "ok"


def test_gateway_falls_back_to_second_provider():
    registry = ProviderRegistry()
    registry.register("deepseek", FakeProvider(fail=True, provider="deepseek"))
    registry.register("openai", FakeProvider(provider="openai"))

    response = ModelGateway(
        registry,
        circuit_breaker=CircuitBreaker(failure_threshold=1),
    ).execute(
        request(),
        fallback_chain=(("openai", "model-b"),),
    )

    assert response.provider == "openai"
    assert response.model == "model-b"


def test_circuit_opens_after_failure_threshold():
    registry = ProviderRegistry()
    registry.register("deepseek", FakeProvider(fail=True, provider="deepseek"))
    breaker = CircuitBreaker(failure_threshold=1)
    gateway = ModelGateway(registry, circuit_breaker=breaker)

    try:
        gateway.execute(request())
    except Exception:
        pass

    assert breaker.allow("deepseek") is False


def test_model_usage_becomes_cost_event():
    response = ModelResponse(
        request_id="MR-2",
        provider="openai",
        model="premium",
        content="ok",
        usage=ModelUsage(
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
            estimated_cost_chf=0.75,
        ),
    )

    event = cost_event_from_response(
        response,
        event_id="COST-MR-2",
        project_id="espacore",
        task_id="TASK-2",
    )

    assert event.provider == "openai"
    assert event.amount_chf == 0.75
    assert event.units == 150.0
