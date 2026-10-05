import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from intake.runtime import IntakeAttachment, IntakeMessage
from intake.service import MultimodalIntakeService


def test_ui_reference_intake_preserves_attachment_roles():
    message = IntakeMessage(
        intake_id="IN-1",
        actor="owner",
        project_id="espacore",
        text="Haz esta sección parecida a la referencia.",
        intake_type="UI_REFERENCE_REDESIGN",
        target_repository="web",
        target_area="home.hero",
        attachments=(
            IntakeAttachment(
                attachment_id="ATT-CURRENT",
                kind="SCREENSHOT",
                role="CURRENT_BASE",
                source="upload://current.png",
                mime_type="image/png",
            ),
            IntakeAttachment(
                attachment_id="ATT-REF",
                kind="SCREENSHOT",
                role="STYLE_REFERENCE",
                source="upload://reference.png",
                mime_type="image/png",
            ),
        ),
    )

    order = MultimodalIntakeService().to_work_order(
        message,
        order_id="ORD-1",
        title="Redesign hero",
    )

    assert order.work_type == "UI_REFERENCE_REDESIGN"
    assert order.target_area == "home.hero"
    assert order.reference_ids == ("ATT-CURRENT", "ATT-REF")
    assert order.reference_bindings == (
        ("ATT-CURRENT", "CURRENT_BASE"),
        ("ATT-REF", "STYLE_REFERENCE"),
    )
    assert order.target_repository == "web"


def test_image_edit_can_distinguish_base_and_desired_result():
    message = IntakeMessage(
        intake_id="IN-2",
        actor="owner",
        project_id="espacore",
        text="Edita la imagen original con este resultado como referencia.",
        intake_type="IMAGE_EDIT",
        attachments=(
            IntakeAttachment(
                "BASE",
                "IMAGE",
                "EDIT_TARGET",
                "upload://base.jpg",
            ),
            IntakeAttachment(
                "TARGET",
                "IMAGE",
                "DESIRED_RESULT",
                "upload://target.jpg",
            ),
        ),
    )

    assert MultimodalIntakeService().requires_manual_staging_review(message) is True


def test_visual_intake_requires_no_guessing_about_attachment_role():
    message = IntakeMessage(
        intake_id="IN-3",
        actor="owner",
        project_id="espacore",
        text="Cambia esta imagen",
        intake_type="IMAGE_REPLACEMENT",
        attachments=(
            IntakeAttachment(
                attachment_id="A",
                kind="IMAGE",
                role="UNKNOWN",
                source="upload://x.png",
            ),
        ),
    )

    try:
        MultimodalIntakeService().to_work_order(
            message,
            order_id="ORD-3",
            title="Replace image",
        )
    except ValueError as exc:
        assert "invalid_attachment_role" in str(exc)
        return
    raise AssertionError("ambiguous attachment role must fail")


def test_attachment_source_rejects_file_scheme():
    message = IntakeMessage(
        intake_id="IN-SOURCE-1",
        actor="owner",
        project_id="espacore",
        text="Review attachment",
        attachments=(
            IntakeAttachment(
                attachment_id="ATT-1",
                kind="FILE",
                role="REQUIREMENT_DOCUMENT",
                source="file:///tmp/example.txt",
            ),
        ),
    )
    try:
        MultimodalIntakeService().to_work_order(
            message,
            order_id="ORD-SOURCE-1",
            title="Unsafe source",
        )
    except ValueError as exc:
        assert "attachment_source_scheme_forbidden" in str(exc)
        return
    raise AssertionError("file attachment source must be rejected")


def test_attachment_source_rejects_loopback_host():
    message = IntakeMessage(
        intake_id="IN-SOURCE-2",
        actor="owner",
        project_id="espacore",
        text="Review attachment",
        attachments=(
            IntakeAttachment(
                attachment_id="ATT-2",
                kind="LINK",
                role="REQUIREMENT_DOCUMENT",
                source="https://127.0.0.1/internal",
            ),
        ),
    )
    try:
        MultimodalIntakeService().to_work_order(
            message,
            order_id="ORD-SOURCE-2",
            title="Unsafe host",
        )
    except ValueError as exc:
        assert "attachment_source_private_host_forbidden" in str(exc)
        return
    raise AssertionError("loopback attachment source must be rejected")
