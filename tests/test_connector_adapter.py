import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from github.connector_adapter import ConnectorGitHubAdapter
from github.runtime import GitHubPolicyError
from github.service import GitHubService


def test_connector_receives_only_authorized_operation():
    calls = []

    def executor(operation, payload):
        calls.append((operation, payload))
        return {"ok": True}

    service = GitHubService(ConnectorGitHubAdapter(executor))
    service.create_branch(
        repository="novo34/example",
        task_id="TASK-10",
        agent="developer",
        risk="R1",
        branch="feat/TASK-10",
    )

    assert calls == [(
        "CREATE_BRANCH",
        {
            "repository": "novo34/example",
            "branch": "feat/TASK-10",
            "base_branch": "main",
        },
    )]


def test_connector_never_receives_blocked_main_write():
    calls = []

    def executor(operation, payload):
        calls.append((operation, payload))
        return {"ok": True}

    service = GitHubService(ConnectorGitHubAdapter(executor))

    try:
        service.write_file(
            repository="novo34/example",
            task_id="TASK-11",
            agent="developer",
            risk="R1",
            branch="main",
            path="src/app.py",
            content="x",
            message="bad",
        )
    except GitHubPolicyError:
        pass
    else:
        raise AssertionError("blocked operation reached connector")

    assert calls == []
