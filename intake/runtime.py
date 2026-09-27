from __future__ import annotations

from dataclasses import dataclass


ATTACHMENT_KINDS = {"IMAGE", "SCREENSHOT", "FILE", "LINK"}
ATTACHMENT_ROLES = {
    "CURRENT_BASE",
    "EDIT_TARGET",
    "STYLE_REFERENCE",
    "DESIRED_RESULT",
    "REQUIREMENT_DOCUMENT",
}
INTAKE_TYPES = {
    "GENERAL",
    "IMAGE_REPLACEMENT",
    "IMAGE_GENERATION",
    "IMAGE_EDIT",
    "UI_REFERENCE_REDESIGN",
}


@dataclass(frozen=True)
class IntakeAttachment:
    attachment_id: str
    kind: str
    role: str
    source: str
    mime_type: str | None = None
    filename: str | None = None


@dataclass(frozen=True)
class IntakeMessage:
    intake_id: str
    actor: str
    project_id: str
    text: str
    intake_type: str = "GENERAL"
    target_repository: str | None = None
    target_area: str | None = None
    attachments: tuple[IntakeAttachment, ...] = ()


def validate_intake(message: IntakeMessage) -> tuple[bool, list[str]]:
    failures: list[str] = []

    if not message.intake_id:
        failures.append("intake_id_missing")
    if not message.actor:
        failures.append("actor_missing")
    if not message.project_id:
        failures.append("project_id_missing")
    if not message.text and not message.attachments:
        failures.append("empty_intake")
    if message.intake_type not in INTAKE_TYPES:
        failures.append("invalid_intake_type")

    seen: set[str] = set()
    for item in message.attachments:
        if not item.attachment_id:
            failures.append("attachment_id_missing")
        if item.attachment_id in seen:
            failures.append("duplicate_attachment_id")
        seen.add(item.attachment_id)

        if item.kind not in ATTACHMENT_KINDS:
            failures.append("invalid_attachment_kind")
        if item.role not in ATTACHMENT_ROLES:
            failures.append("invalid_attachment_role")
        if not item.source:
            failures.append("attachment_source_missing")

    return not failures, failures
