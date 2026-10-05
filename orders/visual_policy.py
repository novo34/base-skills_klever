from __future__ import annotations

from orders.runtime import WorkOrder


VISUAL_WORK_TYPES = {
    "IMAGE_REPLACEMENT",
    "IMAGE_GENERATION",
    "IMAGE_EDIT",
    "UI_REFERENCE_REDESIGN",
}


def requires_manual_staging_review(order: WorkOrder) -> bool:
    return order.work_type in VISUAL_WORK_TYPES


def validate_visual_order(order: WorkOrder) -> tuple[bool, list[str]]:
    failures: list[str] = []

    if order.work_type in VISUAL_WORK_TYPES:
        if not order.target_area and order.work_type == "UI_REFERENCE_REDESIGN":
            failures.append("visual_target_area_required")
        if not order.reference_bindings:
            failures.append("visual_references_required")

    if order.work_type == "UI_REFERENCE_REDESIGN":
        roles = {role for _, role in order.reference_bindings}
        if "STYLE_REFERENCE" not in roles:
            failures.append("style_reference_required")

    if order.work_type == "IMAGE_EDIT":
        roles = {role for _, role in order.reference_bindings}
        if "EDIT_TARGET" not in roles:
            failures.append("edit_target_required")

    return not failures, failures
