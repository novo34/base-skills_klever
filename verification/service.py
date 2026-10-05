from __future__ import annotations

from verification.policy import requirements_for_triggers
from verification.runtime import VerificationEvidence, VerificationResult, verify


class VerificationService:
    def evaluate(
        self,
        *,
        triggers: set[str],
        evidence: VerificationEvidence,
    ) -> VerificationResult:
        policy = requirements_for_triggers(triggers)
        return verify(evidence, **policy)
