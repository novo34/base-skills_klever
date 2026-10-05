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
    ProviderHealth,
)
from models.errors import ProviderAuthError, ProviderTimeoutError
from models.retry import RetryPolicy
from models.provider_registry import ProviderRegistry
from models.usage import cost_event_from_response
from tests.security_helpers import explicit_budget_guard


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
        return ProviderHealth(ok=not self.fail)


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

    response = ModelGateway(registry, budget_guard=explicit_budget_guard()).execute(request())

    assert response.provider == "deepseek"
    assert response.content == "ok"


def test_gateway_falls_back_to_second_provider():
    registry = ProviderRegistry()
    registry.register("deepseek", FakeProvider(fail=True, provider="deepseek"))
    registry.register("openai", FakeProvider(provider="openai"))

    response = ModelGateway(
        registry,
        budget_guard=explicit_budget_guard(),
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
    gateway = ModelGateway(
        registry,
        budget_guard=explicit_budget_guard(),
        circuit_breaker=breaker,
    )

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



class RetryProvider(ModelProviderAdapter):
    def __init__(self, failures_before_success=0, error_type=ProviderTimeoutError):
        self.failures_before_success = failures_before_success
        self.error_type = error_type
        self.calls = 0

    def execute(self, request):
        self.calls += 1
        if self.calls <= self.failures_before_success:
            raise self.error_type("temporary")
        return ModelResponse(
            request_id=request.request_id,
            provider=request.provider,
            model=request.model,
            content="ok-after-retry",
            usage=ModelUsage(total_tokens=10, estimated_cost_chf=0.01),
        )

    def health(self):
        return ProviderHealth(ok=True)


def test_retryable_provider_error_is_retried():
    registry = ProviderRegistry()
    provider = RetryProvider(failures_before_success=1)
    registry.register("deepseek", provider)

    response = ModelGateway(
        registry,
        budget_guard=explicit_budget_guard(),
        retry_policy=RetryPolicy(max_attempts=2),
    ).execute(request())

    assert response.content == "ok-after-retry"
    assert provider.calls == 2


def test_non_retryable_auth_error_is_not_retried_and_falls_back():
    registry = ProviderRegistry()
    primary = RetryProvider(
        failures_before_success=99,
        error_type=ProviderAuthError,
    )
    secondary = RetryProvider(failures_before_success=0)
    registry.register("deepseek", primary)
    registry.register("openai", secondary)

    response = ModelGateway(
        registry,
        budget_guard=explicit_budget_guard(),
        retry_policy=RetryPolicy(max_attempts=3),
    ).execute(
        request(),
        fallback_chain=(("openai", "model-b"),),
    )

    assert primary.calls == 1
    assert response.provider == "openai"


def test_request_rejects_invalid_timeout():
    try:
        ModelRequest(
            request_id="MR-BAD",
            project_id="espacore",
            task_id="TASK-1",
            agent_role="developer",
            provider="deepseek",
            model="model-a",
            prompt="x",
            timeout_seconds=0,
        )
    except ValueError as exc:
        assert "timeout_seconds_must_be_positive" in str(exc)
        return
    raise AssertionError("invalid timeout must fail")


def test_gateway_refuses_missing_budget_guard():
    registry = ProviderRegistry()
    registry.register("deepseek", FakeProvider(provider="deepseek"))
    try:
        ModelGateway(registry, budget_guard=None)
    except ValueError as exc:
        assert "budget_guard_required" in str(exc)
        return
    raise AssertionError("ModelGateway must fail closed without budget guard")


def test_circuit_breaker_recovers_through_half_open_probe():
    now = [100.0]
    breaker = CircuitBreaker(
        failure_threshold=1,
        reset_timeout_seconds=30.0,
        clock=lambda: now[0],
    )

    breaker.failure("deepseek")
    assert breaker.allow("deepseek") is False

    now[0] = 131.0
    assert breaker.allow("deepseek") is True
    assert breaker.allow("deepseek") is False

    breaker.success("deepseek")
    assert breaker.allow("deepseek") is True
