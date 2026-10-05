from __future__ import annotations

from dataclasses import dataclass
import ipaddress
from urllib.parse import urlparse


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

ALLOWED_INTERNAL_SOURCE_SCHEMES = {"upload", "channel"}
ALLOWED_EXTERNAL_SOURCE_SCHEMES = {"https"}


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


def _is_forbidden_host(hostname: str) -> bool:
    host = hostname.strip().lower().rstrip(".")
    if host == "localhost" or host.endswith(".localhost") or host.endswith(".local"):
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_reserved
        or ip.is_multicast
        or ip.is_unspecified
    )


def validate_attachment_source(source: str) -> tuple[bool, str | None]:
    if not source:
        return False, "attachment_source_missing"

    parsed = urlparse(source)
    scheme = parsed.scheme.lower()

    if scheme in ALLOWED_INTERNAL_SOURCE_SCHEMES:
        if not parsed.netloc and not parsed.path:
            return False, "attachment_internal_source_invalid"
        return True, None

    if scheme not in ALLOWED_EXTERNAL_SOURCE_SCHEMES:
        return False, "attachment_source_scheme_forbidden"

    if not parsed.hostname:
        return False, "attachment_source_host_required"
    if parsed.username or parsed.password:
        return False, "attachment_source_userinfo_forbidden"
    if _is_forbidden_host(parsed.hostname):
        return False, "attachment_source_private_host_forbidden"

    return True, None


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

        source_ok, source_failure = validate_attachment_source(item.source)
        if not source_ok and source_failure is not None:
            failures.append(source_failure)

    return not failures, failures
