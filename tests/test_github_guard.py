import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("github_guard", ROOT / "scripts" / "github_guard.py")
github_guard = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(github_guard)


def test_developer_cannot_write_main():
    ok, reason = github_guard.authorize("WRITE_FILE", "developer", "R1", branch="main")
    assert ok is False
    assert reason == "direct_default_branch_write_forbidden"


def test_verifier_cannot_merge():
    ok, reason = github_guard.authorize("MERGE_PULL_REQUEST", "verifier", "R2", verifier_passed=True)
    assert ok is False
    assert reason == "agent_not_authorized"


def test_integrator_cannot_merge_without_verification():
    ok, reason = github_guard.authorize("MERGE_PULL_REQUEST", "integrator", "R2", verifier_passed=False)
    assert ok is False
    assert reason == "verification_required"


def test_r4_merge_requires_human():
    ok, reason = github_guard.authorize(
        "MERGE_PULL_REQUEST", "integrator", "R4",
        verifier_passed=True, human_approved=False
    )
    assert ok is False
    assert reason == "human_approval_required"


def test_verified_r1_merge_can_be_authorized():
    ok, reason = github_guard.authorize(
        "MERGE_PULL_REQUEST", "integrator", "R1",
        verifier_passed=True, human_approved=False
    )
    assert ok is True
    assert reason == "ok"
