import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.verifier import VerifierAgent
from scripts.github_guard import authorize


def test_verifier_runtime_exposes_no_delivery_write_methods():
    methods = set(dir(VerifierAgent))
    assert "apply_edit_plan" not in methods
    assert "commit_and_push" not in methods
    assert "create_pull_request" not in methods
    assert "merge_pull_request" not in methods


def test_verifier_github_write_is_denied():
    ok, _ = authorize(
        "WRITE_FILE",
        "verifier",
        "R2",
        branch="feat/TASK-1",
    )
    assert ok is False


def test_verifier_merge_is_denied_even_with_gates():
    ok, _ = authorize(
        "MERGE_PULL_REQUEST",
        "verifier",
        "R4",
        verifier_passed=True,
        human_approved=True,
    )
    assert ok is False
