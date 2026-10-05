import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from channels.runtime import ChannelMessage
from channels.service import ChannelIngressService
from intake.runtime import IntakeAttachment


def test_whatsapp_screenshot_enters_multimodal_intake():
    message = ChannelMessage(
        message_id="WA-1",
        channel="WHATSAPP",
        actor="owner",
        project_id="espacore",
        authentication_verified=True,
        identity_verified=True,
        authentication_method="test-verified",
        external_actor_id="external-owner",
        verified_actor="owner",
        text="Haz esta sección parecida a la captura.",
        attachments=(
            IntakeAttachment(
                attachment_id="WA-IMG-1",
                kind="SCREENSHOT",
                role="STYLE_REFERENCE",
                source="channel://whatsapp/WA-IMG-1",
                mime_type="image/png",
            ),
        ),
    )

    intake = ChannelIngressService().to_intake(
        message,
        intake_id="IN-WA-1",
        intake_type="UI_REFERENCE_REDESIGN",
        target_repository="web",
        target_area="home.hero",
    )

    assert intake.attachments[0].role == "STYLE_REFERENCE"
    assert intake.project_id == "espacore"


def test_telegram_image_can_become_structured_work_order():
    message = ChannelMessage(
        message_id="TG-1",
        channel="TELEGRAM",
        actor="owner",
        project_id="espacore",
        authentication_verified=True,
        identity_verified=True,
        authentication_method="test-verified",
        external_actor_id="external-owner",
        verified_actor="owner",
        text="Edita esta imagen.",
        attachments=(
            IntakeAttachment(
                attachment_id="TG-IMG-1",
                kind="IMAGE",
                role="EDIT_TARGET",
                source="channel://telegram/TG-IMG-1",
                mime_type="image/jpeg",
            ),
        ),
    )

    order = ChannelIngressService().to_work_order(
        message,
        intake_id="IN-TG-1",
        order_id="ORD-TG-1",
        title="Edit hero image",
        intake_type="IMAGE_EDIT",
    )

    assert order.work_type == "IMAGE_EDIT"
    assert order.reference_ids == ("TG-IMG-1",)


def test_channel_contract_exposes_no_direct_github_or_agent_execution():
    methods = set(dir(ChannelIngressService))
    assert "merge_pull_request" not in methods
    assert "write_file" not in methods
    assert "execute_agent" not in methods


def test_external_channel_rejects_unverified_identity():
    message = ChannelMessage(
        message_id="WA-BAD",
        channel="WHATSAPP",
        actor="owner",
        project_id="espacore",
        text="status",
        authentication_verified=False,
        identity_verified=False,
    )
    try:
        ChannelIngressService().to_intake(
            message,
            intake_id="IN-WA-BAD",
        )
    except ValueError as exc:
        assert "channel_authentication_required" in str(exc)
        assert "channel_identity_verification_required" in str(exc)
        return
    raise AssertionError("unverified external identity must fail closed")


def test_authenticated_channel_cannot_impersonate_different_actor():
    message = ChannelMessage(
        message_id="WA-IMPERSONATE",
        channel="WHATSAPP",
        actor="admin",
        project_id="espacore",
        text="status",
        authentication_verified=True,
        identity_verified=True,
        authentication_method="signed-webhook",
        external_actor_id="external-owner",
        verified_actor="owner",
    )
    try:
        ChannelIngressService().to_intake(
            message,
            intake_id="IN-WA-IMPERSONATE",
        )
    except ValueError as exc:
        assert "verified_actor_mismatch" in str(exc)
        return
    raise AssertionError("authenticated identity must not impersonate another actor")
