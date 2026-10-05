import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from workspaces.adapter import WorkspaceAdapter
from workspaces.runtime import WorkspacePolicyError
from workspaces.service import WorkspaceService


class FakeWorkspaceAdapter(WorkspaceAdapter):
    def __init__(self):
        self.calls = []

    def create(self, spec):
        self.calls.append(("CREATE", spec))
        return {"created": True}

    def clone_repository(self, workspace_id, repository, branch):
        self.calls.append(("CLONE", workspace_id, repository, branch))
        return {"cloned": True}

    def install(self, workspace_id):
        self.calls.append(("INSTALL", workspace_id))
        return {"installed": True}

    def execute(self, workspace_id, command):
        self.calls.append(("EXECUTE", workspace_id, command))
        return {"exit_code": 0}

    def collect_diff(self, workspace_id):
        self.calls.append(("COLLECT_DIFF", workspace_id))
        return {"diff": ""}

    def destroy(self, workspace_id):
        self.calls.append(("DESTROY", workspace_id))
        return {"destroyed": True}


def test_workspace_rejects_main_branch():
    service = WorkspaceService(FakeWorkspaceAdapter())
    try:
        service.provision(
            workspace_id="WS-1",
            task_id="TASK-1",
            repository="novo34/example",
            branch="main",
        )
    except WorkspacePolicyError:
        return
    raise AssertionError("main branch workspace must be rejected")


def test_workspace_happy_path_and_teardown():
    adapter = FakeWorkspaceAdapter()
    service = WorkspaceService(adapter)

    service.provision(
        workspace_id="WS-2",
        task_id="TASK-2",
        repository="novo34/example",
        branch="feat/TASK-2",
    )
    service.execute("WS-2", "git status")
    service.collect_diff("WS-2")
    service.teardown("WS-2")

    assert service.state("WS-2").status == "DESTROYED"
    assert [call[0] for call in adapter.calls] == [
        "CREATE", "CLONE", "INSTALL", "EXECUTE", "COLLECT_DIFF", "DESTROY"
    ]


def test_disallowed_command_never_reaches_adapter():
    adapter = FakeWorkspaceAdapter()
    service = WorkspaceService(adapter)

    service.provision(
        workspace_id="WS-3",
        task_id="TASK-3",
        repository="novo34/example",
        branch="feat/TASK-3",
    )

    before = len(adapter.calls)
    try:
        service.execute("WS-3", "rm -rf /")
    except PermissionError:
        pass
    else:
        raise AssertionError("dangerous command must be blocked")

    assert len(adapter.calls) == before


def test_teardown_clears_mounted_secrets():
    adapter = FakeWorkspaceAdapter()
    service = WorkspaceService(adapter)
    service.provision(
        workspace_id="WS-4",
        task_id="TASK-4",
        repository="novo34/example",
        branch="feat/TASK-4",
        mounted_secrets={"GITHUB_TOKEN"},
    )
    service.teardown("WS-4")
    assert service.state("WS-4").mounted_secrets == set()
