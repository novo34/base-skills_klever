from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Approval:
    approval_id: str
    task_id: str
    action: str
    status: str
    requested_by: str
    requested_at: str
    staging_evidence_id: str | None = None
    staging_url: str | None = None
    staging_revision: str | None = None
    source_pr: int | None = None
    source_commit: str | None = None
    decided_by: str | None = None
    decided_at: str | None = None
    note: str | None = None


def request_approval(
    approval_id: str,
    task_id: str,
    action: str,
    requested_by: str,
    *,
    requested_at: str,
    staging_evidence_id: str | None = None,
    staging_url: str | None = None,
    staging_revision: str | None = None,
    source_pr: int | None = None,
    source_commit: str | None = None,
) -> Approval:
    if action == "MERGE_PULL_REQUEST":
        required = {
            "staging_evidence_id": staging_evidence_id,
            "staging_url": staging_url,
            "staging_revision": staging_revision,
            "source_pr": source_pr,
            "source_commit": source_commit,
        }
        missing = [name for name, value in required.items() if value in {None, ""}]
        if missing:
            raise ValueError("merge_approval_snapshot_incomplete:" + ",".join(missing))

    return Approval(
        approval_id=approval_id,
        task_id=task_id,
        action=action,
        status="PENDING",
        requested_by=requested_by,
        requested_at=requested_at,
        staging_evidence_id=staging_evidence_id,
        staging_url=staging_url,
        staging_revision=staging_revision,
        source_pr=source_pr,
        source_commit=source_commit,
    )


def decide(
    approval: Approval,
    *,
    decision: str,
    decided_by: str,
    decided_at: str,
    note: str | None = None,
) -> Approval:
    if approval.status != "PENDING":
        raise RuntimeError("approval_already_decided")
    if decision not in {"APPROVED", "REJECTED", "CHANGES_REQUESTED"}:
        raise ValueError("invalid_approval_decision")
    if not decided_at:
        raise ValueError("decided_at_required")

    return Approval(
        approval_id=approval.approval_id,
        task_id=approval.task_id,
        action=approval.action,
        status=decision,
        requested_by=approval.requested_by,
        requested_at=approval.requested_at,
        staging_evidence_id=approval.staging_evidence_id,
        staging_url=approval.staging_url,
        staging_revision=approval.staging_revision,
        source_pr=approval.source_pr,
        source_commit=approval.source_commit,
        decided_by=decided_by,
        decided_at=decided_at,
        note=note,
    )
