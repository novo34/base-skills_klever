from __future__ import annotations

from verification.runtime import VerificationEvidence


class EvidenceBuilder:
    def from_sources(
        self,
        *,
        requirement_ids: list[str],
        ci_status: str,
        unit_exit_code: int | None,
        integration_exit_code: int | None,
        e2e_exit_code: int | None,
        diff_reviewed: bool,
        backend_verified: bool = False,
        frontend_verified: bool = False,
        database_verified: bool = False,
        notes: list[str] | None = None,
    ) -> VerificationEvidence:
        return VerificationEvidence(
            requirement_ids=tuple(requirement_ids),
            ci_passed=ci_status == "success",
            unit_passed=unit_exit_code == 0,
            integration_passed=integration_exit_code == 0,
            e2e_passed=e2e_exit_code == 0,
            diff_reviewed=diff_reviewed,
            backend_verified=backend_verified,
            frontend_verified=frontend_verified,
            database_verified=database_verified,
            notes=tuple(notes or []),
        )
