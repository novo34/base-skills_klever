from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse

from intake.runtime import validate_attachment_source


class AttachmentFetchPolicyError(PermissionError):
    pass


@dataclass(frozen=True)
class AttachmentFetchPolicy:
    max_redirects: int = 3
    allow_https_only: bool = True


def _address_is_forbidden(value: str) -> bool:
    ip = ipaddress.ip_address(value)
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_reserved
        or ip.is_multicast
        or ip.is_unspecified
    )


def validate_resolved_external_source(
    source: str,
    *,
    resolve_host: Callable[[str], tuple[str, ...]],
) -> None:
    ok, failure = validate_attachment_source(source)
    if not ok:
        raise AttachmentFetchPolicyError(failure or "attachment_source_invalid")

    parsed = urlparse(source)
    if parsed.scheme.lower() != "https":
        return

    hostname = parsed.hostname
    if not hostname:
        raise AttachmentFetchPolicyError("attachment_source_host_required")

    addresses = resolve_host(hostname)
    if not addresses:
        raise AttachmentFetchPolicyError("attachment_source_dns_resolution_required")

    for address in addresses:
        try:
            if _address_is_forbidden(address):
                raise AttachmentFetchPolicyError(
                    "attachment_source_resolves_to_private_address"
                )
        except ValueError as exc:
            raise AttachmentFetchPolicyError(
                "attachment_source_invalid_resolved_address"
            ) from exc


def validate_redirect_chain(
    urls: tuple[str, ...],
    *,
    resolve_host: Callable[[str], tuple[str, ...]],
    policy: AttachmentFetchPolicy | None = None,
) -> None:
    policy = policy or AttachmentFetchPolicy()
    if not urls:
        raise AttachmentFetchPolicyError("attachment_fetch_url_required")
    if len(urls) - 1 > policy.max_redirects:
        raise AttachmentFetchPolicyError("attachment_redirect_limit_exceeded")

    for url in urls:
        validate_resolved_external_source(
            url,
            resolve_host=resolve_host,
        )
