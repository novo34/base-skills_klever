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
    return not failures, failures
