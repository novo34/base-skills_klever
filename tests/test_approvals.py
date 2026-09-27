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
        staging_evidence_id="STG-EV-1",
        staging_url="https://staging.example",
    )
    assert approval.status == "PENDING"

    approval = decide(
        approval,
        decision="APPROVED",
        decided_by="human-admin",
    )
    assert approval.status == "APPROVED"
    assert approval.decided_by == "human-admin"


def test_human_can_request_changes():
    approval = request_approval(
        "APR-2",
        "TASK-2",
        "MERGE_PULL_REQUEST",
        "integrator",
        staging_evidence_id="STG-EV-2",
        staging_url="https://staging.example",
    )
    approval = decide(
        approval,
        decision="CHANGES_REQUESTED",
        decided_by="human-admin",
        note="Adjust mobile layout",
    )
    assert approval.status == "CHANGES_REQUESTED"


def test_approval_cannot_be_decided_twice():
    approval = request_approval(
        "APR-3",
        "TASK-3",
        "MERGE_PULL_REQUEST",
        "integrator",
        staging_evidence_id="STG-EV-3",
        staging_url="https://staging.example",
    )
    approval = decide(approval, decision="REJECTED", decided_by="human-admin")

    try:
        decide(approval, decision="APPROVED", decided_by="human-admin")
    except RuntimeError:
        return
    raise AssertionError("decided approval must be immutable")


def test_merge_approval_requires_staging_evidence():
    try:
        request_approval(
            "APR-NO-EVIDENCE",
            "TASK-X",
            "MERGE_PULL_REQUEST",
            "integrator",
        )
    except ValueError as exc:
        assert "staging_evidence_required_for_merge_approval" in str(exc)
        return
    raise AssertionError("merge approval without staging evidence must fail")
