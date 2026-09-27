from __future__ import annotations

from dataclasses import dataclass

from intake.runtime import IntakeAttachment


@dataclass(frozen=True)
class ChannelMessage:
    message_id: str
    channel: str
    actor: str
    project_id: str
    text: str
    attachments: tuple[IntakeAttachment, ...] = ()
    reply_to: str | None = None
    metadata: dict | None = None
    authentication_verified: bool = False
    identity_verified: bool = False
    authentication_method: str | None = None
    external_actor_id: str | None = None
    verified_actor: str | None = None


def validate_channel_message(message: ChannelMessage) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if not message.message_id:
        failures.append("message_id_missing")
    if message.channel not in {"WEB", "TELEGRAM", "WHATSAPP"}:
        failures.append("unsupported_channel")
    if not message.actor:
        failures.append("actor_missing")
    if not message.project_id:
        failures.append("project_id_missing")
    if not message.text and not message.attachments:
        failures.append("empty_channel_message")

    if not message.authentication_verified:
        failures.append("channel_authentication_required")
    if not message.identity_verified:
        failures.append("channel_identity_verification_required")
    if not message.authentication_method:
        failures.append("channel_authentication_method_required")
    if message.channel in {"TELEGRAM", "WHATSAPP"} and not message.external_actor_id:
        failures.append("external_actor_id_required")
    if not message.verified_actor:
        failures.append("verified_actor_required")
    elif message.actor != message.verified_actor:
        failures.append("verified_actor_mismatch")

    return not failures, failures
