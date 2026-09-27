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
        staging_revision="rev-1",
        source_pr=1,
        source_commit="commit-1",
        requested_at="2026-09-27T18:00:00Z",
    )
    assert approval.status == "PENDING"

    approval = decide(
        approval,
        decision="APPROVED",
        decided_by="human-admin",
        decided_at="2026-09-27T18:05:00Z",
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
        staging_revision="rev-1",
        source_pr=1,
        source_commit="commit-1",
        requested_at="2026-09-27T18:00:00Z",
    )
    approval = decide(
        approval,
        decision="CHANGES_REQUESTED",
        decided_by="human-admin",
        decided_at="2026-09-27T18:05:00Z",
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
        staging_revision="rev-1",
        source_pr=1,
        source_commit="commit-1",
        requested_at="2026-09-27T18:00:00Z",
    )
    approval = decide(
        approval,
        decision="REJECTED",
        decided_by="human-admin",
        decided_at="2026-09-27T18:05:00Z",
    )

    try:
        decide(
            approval,
            decision="APPROVED",
            decided_by="human-admin",
            decided_at="2026-09-27T18:06:00Z",
        )
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
            requested_at="2026-09-27T18:00:00Z",
        )
    except ValueError as exc:
        assert "merge_approval_snapshot_incomplete" in str(exc)
        return
    raise AssertionError("merge approval without staging evidence must fail")


def test_merge_approval_snapshot_preserves_exact_revision_and_pr():
    approval = request_approval(
        "APR-SNAPSHOT",
        "TASK-SNAPSHOT",
        "MERGE_PULL_REQUEST",
        "integrator",
        requested_at="2026-09-27T18:00:00Z",
        staging_evidence_id="STG-EV-S",
        staging_url="https://staging.example",
        staging_revision="staging-rev-s",
        source_pr=77,
        source_commit="source-commit-s",
    )
    decided = decide(
        approval,
        decision="APPROVED",
        decided_by="owner",
        decided_at="2026-09-27T18:10:00Z",
    )
    assert decided.staging_revision == "staging-rev-s"
    assert decided.source_pr == 77
    assert decided.source_commit == "source-commit-s"
    assert decided.requested_at == "2026-09-27T18:00:00Z"
    assert decided.decided_at == "2026-09-27T18:10:00Z"
