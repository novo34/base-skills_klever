import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from command_center.model_interpreter import (
    CommandInterpretationError,
    ModelCommandInterpreter,
)
from models.gateway import ModelGateway
from models.gateway_contract import (
    ModelProviderAdapter,
    ModelResponse,
    ModelUsage,
    ProviderHealth,
)
from models.provider_registry import ProviderRegistry


class FakeModel(ModelProviderAdapter):
    def __init__(self, content):
        self.content = content

    def execute(self, request):
        return ModelResponse(
            request_id=request.request_id,
            provider=request.provider,
            model=request.model,
            content=self.content,
            usage=ModelUsage(),
        )

    def health(self):
        return ProviderHealth(ok=True)


def interpreter(content):
    registry = ProviderRegistry()
    registry.register("openai", FakeModel(content))
    return ModelCommandInterpreter(
        gateway=ModelGateway(registry),
        provider="openai",
        model="command-model",
    )


def test_free_form_command_becomes_structured_intent():
    item = interpreter(
        '{"action":"REQUEST_AUDIT","project_id":"espacore",'
        '"target_id":"TASK-9","confidence":0.96,'
        '"requires_confirmation":false,"payload":{}}'
    ).interpret(
        intent_id="INT-9",
        actor="owner",
        text="Revisa a fondo la tarea 9 de Espacore",
    )

    assert item.action == "REQUEST_AUDIT"
    assert item.project_id == "espacore"
    assert item.target_id == "TASK-9"
    assert item.confidence == 0.96


def test_low_confidence_requires_confirmation():
    item = interpreter(
        '{"action":"REQUEST_AUDIT","project_id":"espacore",'
        '"target_id":"TASK-9","confidence":0.55,'
        '"requires_confirmation":false,"payload":{}}'
    ).interpret(
        intent_id="INT-10",
        actor="owner",
        text="Haz lo de la otra vez",
    )
    assert item.requires_confirmation is True


def test_sensitive_project_pause_always_requires_confirmation():
    item = interpreter(
        '{"action":"PAUSE_PROJECT","project_id":"espacore",'
        '"target_id":null,"confidence":0.99,'
        '"requires_confirmation":false,"payload":{}}'
    ).interpret(
        intent_id="INT-11",
        actor="owner",
        text="Pausa Espacore",
    )
    assert item.requires_confirmation is True


def test_unknown_action_is_rejected_before_control_layer():
    try:
        interpreter(
            '{"action":"DELETE_PRODUCTION","project_id":"espacore",'
            '"target_id":null,"confidence":0.99,'
            '"requires_confirmation":false,"payload":{}}'
        ).interpret(
            intent_id="INT-12",
            actor="owner",
            text="Borra producción",
        )
    except CommandInterpretationError as exc:
        assert "unsupported_structured_action" in str(exc)
        return
    raise AssertionError("unsupported action must fail")


def test_invalid_json_is_rejected():
    try:
        interpreter("not-json").interpret(
            intent_id="INT-13",
            actor="owner",
            text="Algo ambiguo",
        )
    except CommandInterpretationError as exc:
        assert "invalid_structured_intent_json" in str(exc)
        return
    raise AssertionError("invalid JSON must fail")
