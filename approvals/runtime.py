from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Approval:
    approval_id: str
    task_id: str
    action: str
    status: str
    requested_by: str
    decided_by: str | None = None
    note: str | None = None


def request_approval(approval_id: str, task_id: str, action: str, requested_by: str) -> Approval:
    return Approval(
        approval_id=approval_id,
        task_id=task_id,
        action=action,
        status="PENDING",
        requested_by=requested_by,
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
        decided_by=decided_by,
        note=note,
    )
