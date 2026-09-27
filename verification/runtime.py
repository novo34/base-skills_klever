from __future__ import annotations

from dataclasses import dataclass, field


class VerificationError(RuntimeError):
    pass


@dataclass(frozen=True)
class VerificationEvidence:
    requirement_ids: tuple[str, ...] = ()
    ci_passed: bool = False
    unit_passed: bool = False
    integration_passed: bool = False
    e2e_passed: bool = False
    diff_reviewed: bool = False
    backend_verified: bool = False
    frontend_verified: bool = False
    database_verified: bool = False
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class VerificationResult:
    status: str
    failures: tuple[str, ...] = ()
    evidence: VerificationEvidence = field(default_factory=VerificationEvidence)


def verify(
    evidence: VerificationEvidence,
    *,
    requires_backend: bool = False,
    requires_frontend: bool = False,
    requires_database: bool = False,
    requires_e2e: bool = True,
) -> VerificationResult:
    failures: list[str] = []

    if not evidence.requirement_ids:
        failures.append("missing_requirement_traceability")
    if not evidence.ci_passed:
        failures.append("ci_failed_or_missing")
    if not evidence.unit_passed:
        failures.append("unit_tests_failed_or_missing")
    if not evidence.integration_passed:
        failures.append("integration_tests_failed_or_missing")
    if requires_e2e and not evidence.e2e_passed:
        failures.append("e2e_failed_or_missing")
    if not evidence.diff_reviewed:
        failures.append("diff_not_reviewed")
    if requires_backend and not evidence.backend_verified:
        failures.append("backend_not_verified")
    if requires_frontend and not evidence.frontend_verified:
        failures.append("frontend_not_verified")
    if requires_database and not evidence.database_verified:
        failures.append("database_not_verified")

    return VerificationResult(
        status="FAILED" if failures else "VERIFIED",
        failures=tuple(failures),
        evidence=evidence,
    )
