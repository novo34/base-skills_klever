from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Approval:
    approval_id: str
    task_id: str
    action: str
    status: str
    requested_by: str
    staging_evidence_id: str | None = None
    staging_url: str | None = None
    decided_by: str | None = None
    note: str | None = None


def request_approval(
    approval_id: str,
    task_id: str,
    action: str,
    requested_by: str,
    *,
    staging_evidence_id: str | None = None,
    staging_url: str | None = None,
) -> Approval:
    if action == "MERGE_PULL_REQUEST":
        if not staging_evidence_id:
            raise ValueError("staging_evidence_required_for_merge_approval")
        if not staging_url:
            raise ValueError("staging_url_required_for_merge_approval")

    return Approval(
        approval_id=approval_id,
        task_id=task_id,
        action=action,
        status="PENDING",
        requested_by=requested_by,
        staging_evidence_id=staging_evidence_id,
        staging_url=staging_url,
    )


def decide(
    approval: Approval,
    *,
    decision: str,
    decided_by: str,
    note: str | None = None,
) -> Approval:
    if approval.status != "PENDING":
        raise RuntimeError("approval_already_decided")
    if decision not in {"APPROVED", "REJECTED", "CHANGES_REQUESTED"}:
        raise ValueError("invalid_approval_decision")

    return Approval(
        approval_id=approval.approval_id,
        task_id=approval.task_id,
        action=approval.action,
        status=decision,
        requested_by=approval.requested_by,
        staging_evidence_id=approval.staging_evidence_id,
        staging_url=approval.staging_url,
        decided_by=decided_by,
        note=note,
    )
