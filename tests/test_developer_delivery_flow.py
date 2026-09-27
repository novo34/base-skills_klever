import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.delivery_adapter import (
    CommitResult,
    DeveloperDeliveryAdapter,
    PullRequestResult,
)
from agents_runtime.delivery_flow import (
    DeveloperDeliveryFlow,
    DeveloperDeliveryRequest,
)
from agents_runtime.developer import DeveloperAgent, DeveloperTask
from agents_runtime.edit_protocol import EditPlan, FileEdit
from models.gateway import ModelGateway
from models.gateway_contract import (
    ModelProviderAdapter,
    ModelResponse,
    ModelUsage,
    ProviderHealth,
)
from models.provider_registry import ProviderRegistry
from workspaces.adapter import WorkspaceAdapter
from workspaces.service import WorkspaceService


class FakeModel(ModelProviderAdapter):
    def execute(self, request):
        return ModelResponse(
            request_id=request.request_id,
            provider=request.provider,
            model=request.model,
            content="ok",
            usage=ModelUsage(),
        )

    def health(self):
        return ProviderHealth(ok=True)


class FakeWorkspace(WorkspaceAdapter):
    def __init__(self, exit_code=0):
        self.exit_code = exit_code

    def create(self, spec):
        return {"created": True}

    def clone_repository(self, workspace_id, repository, branch):
        return {"cloned": True}

    def install(self, workspace_id):
        return {"installed": True}

    def execute(self, workspace_id, command):
        return {"exit_code": self.exit_code}

    def collect_diff(self, workspace_id):
        return {"diff": "changed"}

    def destroy(self, workspace_id):
        return {"destroyed": True}


class FakeDelivery(DeveloperDeliveryAdapter):
    def __init__(self):
        self.calls = []

    def apply_edit_plan(self, workspace_id, edit_plan):
        self.calls.append("apply")
        return {"applied": len(edit_plan.edits)}

    def commit_and_push(self, workspace_id, *, branch, message):
        self.calls.append("commit")
        return CommitResult(commit_sha="abc123", branch=branch)

    def create_pull_request(
        self,
        *,
        repository,
        task_id,
        branch,
        base_branch,
        title,
        body,
    ):
        self.calls.append("pr")
        return PullRequestResult(pull_request=42, url="https://example/pr/42")


def build(exit_code=0):
    registry = ProviderRegistry()
    registry.register("deepseek", FakeModel())

    workspace = WorkspaceService(FakeWorkspace(exit_code=exit_code))
    workspace.provision(
        workspace_id="WS-1",
        task_id="TASK-1",
        repository="novo34/example",
        branch="feat/TASK-1",
        allowed_commands={"pytest"},
    )

    developer = DeveloperAgent(
        gateway=ModelGateway(registry),
        workspaces=workspace,
    )
    delivery = FakeDelivery()
    return DeveloperDeliveryFlow(developer=developer, delivery=delivery), delivery


def request():
    task = DeveloperTask(
        task_id="TASK-1",
        project_id="espacore",
        repository="novo34/example",
        branch="feat/TASK-1",
        workspace_id="WS-1",
        objective="Change form",
        acceptance_criteria=("Tests pass",),
        provider="deepseek",
        model="code",
    )
    edit_plan = EditPlan(
        task_id="TASK-1",
        workspace_id="WS-1",
        branch="feat/TASK-1",
        edits=(
            FileEdit(
                path="app/contact/page.tsx",
                operation="UPDATE",
                content="changed",
            ),
        ),
    )
    return DeveloperDeliveryRequest(
        task=task,
        edit_plan=edit_plan,
        validation_commands=("pytest",),
        allowed_roots=("app/contact",),
        commit_message="feat: update contact form",
        pull_request_title="Update contact form",
    )


def test_delivery_flow_applies_validates_commits_and_opens_pr():
    flow, delivery = build(exit_code=0)
    result = flow.run(request())

    assert result["status"] == "PR_OPEN"
    assert result["next_role"] == "verifier"
    assert result["commit"].commit_sha == "abc123"
    assert result["pull_request"].pull_request == 42
    assert delivery.calls == ["apply", "commit", "pr"]


def test_validation_failure_prevents_commit_and_pr():
    flow, delivery = build(exit_code=1)
    result = flow.run(request())

    assert result["status"] == "FAILED_VALIDATION"
    assert result["stage"] == "validation"
    assert delivery.calls == ["apply"]


def test_delivery_flow_has_no_merge_or_self_verification_operation():
    methods = set(dir(DeveloperDeliveryAdapter))
    assert "merge_pull_request" not in methods
    assert "verify" not in methods
