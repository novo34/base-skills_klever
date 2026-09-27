import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.verifier import VerifierAgent, VerifierTask
from models.gateway import ModelGateway
from models.gateway_contract import (
    ModelProviderAdapter,
    ModelResponse,
    ModelUsage,
    ProviderHealth,
)
from models.provider_registry import ProviderRegistry
from tests.security_helpers import explicit_budget_guard
from verification.collectors import (
    CollectorResult,
    VerificationCollectors,
    VerificationContext,
)


class FakeVerifierModel(ModelProviderAdapter):
    def execute(self, request):
        return ModelResponse(
            request_id=request.request_id,
            provider=request.provider,
            model=request.model,
            content="Independent review complete",
            usage=ModelUsage(total_tokens=80, estimated_cost_chf=0.2),
        )

    def health(self):
        return ProviderHealth(ok=True)


class FakeCollectors(VerificationCollectors):
    def __init__(self, overrides=None):
        self.overrides = overrides or {}

    def _result(self, name):
        value = self.overrides.get(name)
        if isinstance(value, Exception):
            raise value
        if value is not None:
            return value
        return CollectorResult(name, "PASS", evidence_ref=f"evidence://{name}")

    def collect_ci(self, context): return self._result("ci")
    def collect_unit(self, context): return self._result("unit")
    def collect_integration(self, context): return self._result("integration")
    def collect_e2e(self, context): return self._result("e2e")
    def collect_diff(self, context): return self._result("diff")
    def collect_backend(self, context): return self._result("backend")
    def collect_frontend(self, context): return self._result("frontend")
    def collect_database(self, context): return self._result("database")


def agent(collectors=None):
    registry = ProviderRegistry()
    registry.register("openai", FakeVerifierModel())
    return VerifierAgent(
        gateway=ModelGateway(registry, budget_guard=explicit_budget_guard()),
        collectors=collectors,
    )


def task():
    return VerifierTask(
        task_id="TASK-V1",
        project_id="espacore",
        requirement_ids=("REQ-API-001",),
        acceptance_criteria=("Form submits", "Backend persists"),
        triggers=("backend", "api"),
        provider="openai",
        model="verifier-model",
    )


def context():
    return VerificationContext(
        task_id="TASK-V1",
        project_id="espacore",
        repository="novo34/example",
        ref="feat/TASK-V1",
        staging_url="https://staging.example",
    )


def test_verifier_inspects_without_editing():
    result = agent().inspect(task(), diff_summary="contact form changes")
    assert result["provider"] == "openai"
    assert "Independent review" in result["findings"]


def test_verifier_returns_verified_from_collector_evidence():
    result = agent(FakeCollectors()).evaluate(
        task(),
        context=context(),
    )
    assert result["result"].status == "VERIFIED"
    assert result["report"]["status"] == "VERIFIED"


def test_verifier_fails_failed_backend_collector():
    result = agent(FakeCollectors({
        "backend": CollectorResult("backend", "FAIL", detail="API mismatch")
    })).evaluate(
        task(),
        context=context(),
    )
    assert result["result"].status == "FAILED"
    assert "backend_not_verified" in result["result"].failures


def test_verifier_blocks_when_collector_cannot_execute():
    result = agent(FakeCollectors({
        "backend": RuntimeError("API unavailable")
    })).evaluate(
        task(),
        context=context(),
    )
    assert result["result"].status == "BLOCKED"
    assert "collector_blocked:backend" in result["result"].failures


def test_verifier_refuses_evaluation_without_collectors():
    try:
        agent().evaluate(task(), context=context())
    except RuntimeError as exc:
        assert "verification_collectors_required" in str(exc)
        return
    raise AssertionError("Verifier must not accept caller booleans instead of collectors")
