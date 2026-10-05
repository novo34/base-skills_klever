import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orders.runtime import WorkOrder
from orders.visual_policy import (
    requires_manual_staging_review,
    validate_visual_order,
)


def test_ui_reference_redesign_requires_manual_staging_review():
    order = WorkOrder(
        order_id="ORD-V1",
        project_id="espacore",
        title="Hero redesign",
        description="Use screenshot reference",
        work_type="UI_REFERENCE_REDESIGN",
        target_area="home.hero",
        reference_ids=("CURRENT", "REF"),
        reference_bindings=(
            ("CURRENT", "CURRENT_BASE"),
            ("REF", "STYLE_REFERENCE"),
        ),
    )
    assert requires_manual_staging_review(order) is True
    ok, failures = validate_visual_order(order)
    assert ok is True
    assert failures == []


def test_ui_redesign_without_style_reference_is_rejected():
    order = WorkOrder(
        order_id="ORD-V2",
        project_id="espacore",
        title="Hero redesign",
        description="Use screenshot reference",
        work_type="UI_REFERENCE_REDESIGN",
        target_area="home.hero",
        reference_ids=("CURRENT",),
        reference_bindings=(("CURRENT", "CURRENT_BASE"),),
    )
    ok, failures = validate_visual_order(order)
    assert ok is False
    assert "style_reference_required" in failures


def test_image_edit_requires_edit_target():
    order = WorkOrder(
        order_id="ORD-V3",
        project_id="espacore",
        title="Edit hero",
        description="Edit image",
        work_type="IMAGE_EDIT",
        reference_ids=("REF",),
        reference_bindings=(("REF", "STYLE_REFERENCE"),),
    )
    ok, failures = validate_visual_order(order)
    assert ok is False
    assert "edit_target_required" in failures
