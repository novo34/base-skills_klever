import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from intake.fetch_policy import (
    AttachmentFetchPolicy,
    AttachmentFetchPolicyError,
    validate_redirect_chain,
    validate_resolved_external_source,
)


def test_public_https_source_with_public_dns_is_allowed():
    validate_resolved_external_source(
        "https://example.com/image.png",
        resolve_host=lambda host: ("93.184.216.34",),
    )


def test_public_hostname_resolving_private_is_blocked():
    try:
        validate_resolved_external_source(
            "https://example.com/image.png",
            resolve_host=lambda host: ("169.254.169.254",),
        )
    except AttachmentFetchPolicyError as exc:
        assert "attachment_source_resolves_to_private_address" in str(exc)
        return
    raise AssertionError("private DNS resolution must be blocked")


def test_redirect_to_private_destination_is_blocked():
    try:
        validate_redirect_chain(
            (
                "https://example.com/file",
                "https://internal.example/file",
            ),
            resolve_host=lambda host: (
                ("93.184.216.34",)
                if host == "example.com"
                else ("10.0.0.10",)
            ),
        )
    except AttachmentFetchPolicyError as exc:
        assert "attachment_source_resolves_to_private_address" in str(exc)
        return
    raise AssertionError("redirect to private address must be blocked")


def test_redirect_limit_is_enforced():
    try:
        validate_redirect_chain(
            (
                "https://a.example/x",
                "https://b.example/x",
                "https://c.example/x",
            ),
            resolve_host=lambda host: ("93.184.216.34",),
            policy=AttachmentFetchPolicy(max_redirects=1),
        )
    except AttachmentFetchPolicyError as exc:
        assert "attachment_redirect_limit_exceeded" in str(exc)
        return
    raise AssertionError("redirect limit must be enforced")
