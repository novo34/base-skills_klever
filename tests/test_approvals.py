import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from approvals.runtime import decide, request_approval


def test_approval_lifecycle():
    approval = request_approval(
        "APR-1",
        "TASK-1",
        "MERGE_PULL_REQUEST",
        "integrator",
    )
    assert approval.status == "PENDING"

    approval = decide(
        approval,
        approved=True,
        decided_by="human-admin",
    )
    assert approval.status == "APPROVED"
    assert approval.decided_by == "human-admin"


def test_approval_cannot_be_decided_twice():
    approval = request_approval("APR-2", "TASK-2", "MERGE_PULL_REQUEST", "integrator")
    approval = decide(approval, approved=False, decided_by="human-admin")

    try:
        decide(approval, approved=True, decided_by="human-admin")
    except RuntimeError:
        return
    raise AssertionError("decided approval must be immutable")
