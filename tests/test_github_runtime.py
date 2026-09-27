import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from github.adapter import GitHubAdapter
from github.runtime import GitHubPolicyError
from github.service import GitHubService


class FakeAdapter(GitHubAdapter):
    def __init__(self):
        self.calls = []

    def get_repository(self, repository):
        self.calls.append(("get_repository", repository))
        return {"repository": repository}

    def create_branch(self, repository, branch, base_branch):
        self.calls.append(("create_branch", repository, branch, base_branch))
        return {"branch": branch}

    def write_file(self, repository, branch, path, content, message):
        self.calls.append(("write_file", repository, branch, path, message))
        return {"path": path}

    def create_pull_request(self, repository, branch, base_branch, title, body):
        self.calls.append(("create_pull_request", repository, branch, base_branch, title))
        return {"number": 1}

    def read_checks(self, repository, ref):
        self.calls.append(("read_checks", repository, ref))
        return {"status": "success"}

    def merge_pull_request(self, repository, pull_request):
        self.calls.append(("merge_pull_request", repository, pull_request))
        return {"merged": True}


def test_service_allows_guarded_branch_and_pr_flow():
    adapter = FakeAdapter()
    service = GitHubService(adapter)

    service.create_branch(
        repository="novo34/example",
        task_id="TASK-1",
        agent="developer",
        risk="R1",
        branch="feat/TASK-1",
    )
    service.write_file(
        repository="novo34/example",
        task_id="TASK-1",
        agent="developer",
        risk="R1",
        branch="feat/TASK-1",
        path="src/example.py",
        content="print('ok')",
        message="feat: task 1",
    )
    service.create_pull_request(
        repository="novo34/example",
        task_id="TASK-1",
        agent="developer",
        risk="R1",
        branch="feat/TASK-1",
        title="TASK-1",
    )

    assert [call[0] for call in adapter.calls] == [
        "create_branch", "write_file", "create_pull_request"
    ]


def test_runtime_blocks_main_write_before_adapter_is_called():
    adapter = FakeAdapter()
    service = GitHubService(adapter)

    try:
        service.write_file(
            repository="novo34/example",
            task_id="TASK-2",
            agent="developer",
            risk="R1",
            branch="main",
            path="src/example.py",
            content="bad",
            message="bad",
        )
    except GitHubPolicyError:
        pass
    else:
        raise AssertionError("main write must be blocked")

    assert adapter.calls == []


def test_r4_merge_requires_human_before_adapter_call():
    adapter = FakeAdapter()
    service = GitHubService(adapter)

    try:
        service.merge_pull_request(
            repository="novo34/example",
            task_id="TASK-3",
            agent="integrator",
            risk="R4",
            pull_request=12,
            verifier_passed=True,
            human_approved=False,
        )
    except GitHubPolicyError:
        pass
    else:
        raise AssertionError("R4 merge must require human approval")

    assert adapter.calls == []
