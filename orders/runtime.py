from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkOrder:
    order_id: str
    project_id: str
    title: str
    description: str
    status: str = "DRAFT"
    priority: str = "NORMAL"
    requirement_ids: tuple[str, ...] = ()
    created_by: str = "human"
    budget_limit_chf: float | None = None
    target_repository: str | None = None
    work_type: str = "GENERAL"
    reference_ids: tuple[str, ...] = ()
    reference_bindings: tuple[tuple[str, str], ...] = ()
    target_area: str | None = None


ALLOWED_ORDER_STATES = {
    "DRAFT",
    "QUEUED",
    "PLANNED",
    "RUNNING",
    "VERIFYING",
    "STAGING",
    "AWAITING_HUMAN",
    "CHANGES_REQUESTED",
    "APPROVED",
    "REJECTED",
    "DONE",
    "BLOCKED",
}


def validate_order(order: WorkOrder) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if not order.order_id:
        failures.append("order_id_missing")
    if not order.project_id:
        failures.append("project_id_missing")
    if not order.title:
        failures.append("title_missing")
    if not order.description:
        failures.append("description_missing")
    if order.status not in ALLOWED_ORDER_STATES:
        failures.append("invalid_order_status")
    if order.priority not in {"LOW", "NORMAL", "HIGH", "URGENT"}:
        failures.append("invalid_order_priority")
    if order.budget_limit_chf is not None and order.budget_limit_chf < 0:
        failures.append("invalid_order_budget")
    if order.work_type not in {
        "GENERAL",
        "IMAGE_REPLACEMENT",
        "IMAGE_GENERATION",
        "IMAGE_EDIT",
        "UI_REFERENCE_REDESIGN",
    }:
        failures.append("invalid_work_type")
    if len(set(order.reference_ids)) != len(order.reference_ids):
        failures.append("duplicate_reference_id")
    binding_ids = [item[0] for item in order.reference_bindings]
    if len(set(binding_ids)) != len(binding_ids):
        failures.append("duplicate_reference_binding")
    if set(binding_ids) != set(order.reference_ids):
        failures.append("reference_binding_mismatch")
    return not failures, failures
