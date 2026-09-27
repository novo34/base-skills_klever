from __future__ import annotations

from verification.runtime import VerificationResult


def build_report(task_id: str, result: VerificationResult) -> dict:
    evidence = result.evidence
    return {
        "task_id": task_id,
        "status": result.status,
        "failures": list(result.failures),
        "checks": {
            "requirements": bool(evidence.requirement_ids),
            "ci": evidence.ci_passed,
            "unit": evidence.unit_passed,
            "integration": evidence.integration_passed,
            "e2e": evidence.e2e_passed,
            "diff_review": evidence.diff_reviewed,
            "backend": evidence.backend_verified,
            "frontend": evidence.frontend_verified,
            "database": evidence.database_verified,
        },
        "requirement_ids": list(evidence.requirement_ids),
        "notes": list(evidence.notes),
    }
