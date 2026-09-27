import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from github.adapter import GitHubAdapter
from github.service import GitHubService
from orchestrator.execution_pipeline import ExecutionPipeline
from verification.runtime import VerificationEvidence
from workspaces.adapter import WorkspaceAdapter
from workspaces.service import WorkspaceService


class FakeGitHub(GitHubAdapter):
    def __init__(self):
        self.calls = []

    def get_repository(self, repository):
        return {"repository": repository}

    def create_branch(self, repository, branch, base_branch):
        self.calls.append(("CREATE_BRANCH", branch))
        return {"branch": branch}

    def write_file(self, repository, branch, path, content, message):
        self.calls.append(("WRITE_FILE", path))
        return {"path": path}

    def create_pull_request(self, repository, branch, base_branch, title, body):
        self.calls.append(("CREATE_PR", branch, title))
        return {"number": 77, "state": "open"}

    def read_checks(self, repository, ref):
        return {"status": "success"}

    def merge_pull_request(self, repository, pull_request):
        self.calls.append(("MERGE", pull_request))
        return {"merged": True}


class FakeWorkspace(WorkspaceAdapter):
    def __init__(self):
        self.calls = []

    def create(self, spec):
        self.calls.append(("CREATE", spec["workspace_id"]))
        return {"created": True}

    def clone_repository(self, workspace_id, repository, branch):
        self.calls.append(("CLONE", workspace_id, branch))
        return {"cloned": True}

    def install(self, workspace_id):
        self.calls.append(("INSTALL", workspace_id))
        return {"installed": True}

    def execute(self, workspace_id, command):
        self.calls.append(("EXECUTE", command))
        return {"exit_code": 0}

    def collect_diff(self, workspace_id):
        self.calls.append(("DIFF", workspace_id))
        return {"diff": "changed"}

    def destroy(self, workspace_id):
        self.calls.append(("DESTROY", workspace_id))
        return {"destroyed": True}


def build_pipeline():
    gh = FakeGitHub()
    ws = FakeWorkspace()
    return ExecutionPipeline(GitHubService(gh), WorkspaceService(ws)), gh, ws


def full_evidence():
    return VerificationEvidence(
        requirement_ids=("REQ-API-001",),
        ci_passed=True,
        unit_passed=True,
        integration_passed=True,
        e2e_passed=True,
        diff_reviewed=True,
        backend_verified=True,
        frontend_verified=True,
        database_verified=True,
    )


def test_pipeline_reaches_verified_without_merge():
    pipeline, gh, ws = build_pipeline()

    execution = pipeline.start_task(
        task_id="TASK-200",
        repository="novo34/example",
        branch="feat/TASK-200",
        triggers={"backend", "implementation"},
        flags=set(),
        workspace_id="WS-200",
    )
    assert execution["state"] == "RUNNING"

    pipeline.run_command(execution, "pytest")
    prepared = pipeline.prepare_review(
        execution,
        title="TASK-200 implementation",
    )
    execution = prepared["execution"]

    assert execution["state"] == "VERIFYING"
    assert prepared["pull_request"]["number"] == 77
    assert not any(call[0] == "MERGE" for call in gh.calls)

    verified = pipeline.verify(
        execution,
        evidence=full_evidence(),
    )
    execution = verified["execution"]

    assert execution["state"] == "VERIFIED"
    assert execution["verification"]["status"] == "VERIFIED"

    pipeline.teardown(execution)
    assert ws.calls[-1][0] == "DESTROY"


def test_missing_evidence_returns_failed_state():
    pipeline, _, _ = build_pipeline()

    execution = pipeline.start_task(
        task_id="TASK-201",
        repository="novo34/example",
        branch="feat/TASK-201",
        triggers={"frontend", "implementation"},
        flags=set(),
        workspace_id="WS-201",
    )
    prepared = pipeline.prepare_review(execution, title="TASK-201")

    failed = pipeline.verify(
        prepared["execution"],
        evidence=VerificationEvidence(
            requirement_ids=("REQ-UI-001",),
            ci_passed=True,
            unit_passed=True,
            integration_passed=True,
            e2e_passed=False,
            diff_reviewed=True,
            frontend_verified=True,
        ),
    )
    execution = failed["execution"]

    assert execution["state"] == "FAILED"
    assert "e2e_failed_or_missing" in execution["verification"]["failures"]


def test_pipeline_builds_verification_evidence_from_sources():
    pipeline, gh, _ = build_pipeline()
    execution = pipeline.start_task(
        task_id="TASK-202",
        repository="novo34/example",
        branch="feat/TASK-202",
        triggers={"backend", "implementation"},
        flags=set(),
        workspace_id="WS-202",
    )
    prepared = pipeline.prepare_review(execution, title="TASK-202")

    result = pipeline.verify_from_sources(
        prepared["execution"],
        requirement_ids=["REQ-API-202"],
        unit_result={"exit_code": 0},
        integration_result={"exit_code": 0},
        e2e_result={"exit_code": 0},
        diff_reviewed=True,
        backend_verified=True,
    )

    assert result["execution"]["state"] == "VERIFIED"
    assert result["report"]["status"] == "VERIFIED"
    assert result["report"]["checks"]["ci"] is True
