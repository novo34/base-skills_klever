import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.verifier import VerifierAgent, VerifierTask
from models.gateway import ModelGateway
from models.gateway_contract import ModelProviderAdapter, ModelResponse, ModelUsage
from models.provider_registry import ProviderRegistry


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
        return {"ok": True}


def agent():
    registry = ProviderRegistry()
    registry.register("openai", FakeVerifierModel())
    return VerifierAgent(gateway=ModelGateway(registry))


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


def test_verifier_inspects_without_editing():
    result = agent().inspect(task(), diff_summary="contact form changes")
    assert result["provider"] == "openai"
    assert "Independent review" in result["findings"]


def test_verifier_returns_verified_with_complete_evidence():
    result = agent().evaluate(
        task(),
        ci_status="success",
        unit_exit_code=0,
        integration_exit_code=0,
        e2e_exit_code=0,
        diff_reviewed=True,
        backend_verified=True,
    )
    assert result["result"].status == "VERIFIED"
    assert result["report"]["status"] == "VERIFIED"


def test_verifier_fails_missing_backend_evidence():
    result = agent().evaluate(
        task(),
        ci_status="success",
        unit_exit_code=0,
        integration_exit_code=0,
        e2e_exit_code=0,
        diff_reviewed=True,
        backend_verified=False,
    )
    assert result["result"].status == "FAILED"
    assert "backend_not_verified" in result["result"].failures
