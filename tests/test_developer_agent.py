import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.developer import DeveloperAgent, DeveloperTask
from agents_runtime.developer_flow import DeveloperFlow
from models.gateway import ModelGateway
from models.gateway_contract import ModelProviderAdapter, ModelResponse, ModelUsage
from models.provider_registry import ProviderRegistry
from workspaces.adapter import WorkspaceAdapter
from workspaces.service import WorkspaceService


class FakeModel(ModelProviderAdapter):
    def execute(self, request):
        return ModelResponse(
            request_id=request.request_id,
            provider=request.provider,
            model=request.model,
            content="Implement minimal change and run tests",
            usage=ModelUsage(total_tokens=100, estimated_cost_chf=0.1),
        )

    def health(self):
        return {"ok": True}


class FakeWorkspace(WorkspaceAdapter):
    def __init__(self, exit_code=0):
        self.exit_code = exit_code
        self.calls = []

    def create(self, spec):
        return {"created": True}

    def clone_repository(self, workspace_id, repository, branch):
        return {"cloned": True}

    def install(self, workspace_id):
        return {"installed": True}

    def execute(self, workspace_id, command):
        self.calls.append(command)
        return {"exit_code": self.exit_code}

    def collect_diff(self, workspace_id):
        return {"diff": "changed"}

    def destroy(self, workspace_id):
        return {"destroyed": True}


def build(exit_code=0):
    registry = ProviderRegistry()
    registry.register("deepseek", FakeModel())
    gateway = ModelGateway(registry)

    adapter = FakeWorkspace(exit_code=exit_code)
    service = WorkspaceService(adapter)
    service.provision(
        workspace_id="WS-1",
        task_id="TASK-1",
        repository="novo34/example",
        branch="feat/TASK-1",
        allowed_commands={"pytest", "git status"},
    )

    agent = DeveloperAgent(gateway=gateway, workspaces=service)
    return DeveloperFlow(agent), adapter


def task():
    return DeveloperTask(
        task_id="TASK-1",
        project_id="espacore",
        repository="novo34/example",
        branch="feat/TASK-1",
        workspace_id="WS-1",
        objective="Fix contact form",
        acceptance_criteria=("Tests pass", "Validation works"),
        provider="deepseek",
        model="code-model",
    )


def test_developer_flow_reaches_review_when_commands_pass():
    flow, _ = build(exit_code=0)
    result = flow.run(task(), validation_commands=("pytest",))
    assert result["status"] == "READY_FOR_REVIEW"
    assert result["plan"]["provider"] == "deepseek"
    assert result["diff"]["diff"] == "changed"


def test_developer_flow_fails_when_validation_command_fails():
    flow, _ = build(exit_code=1)
    result = flow.run(task(), validation_commands=("pytest",))
    assert result["status"] == "FAILED"
    assert len(result["failures"]) == 1
