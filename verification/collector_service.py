from __future__ import annotations

from dataclasses import dataclass

from verification.collectors import (
    CollectorResult,
    VerificationCollectors,
    VerificationContext,
)
from verification.policy import requirements_for_triggers
from verification.runtime import VerificationEvidence


@dataclass(frozen=True)
class CollectedEvidenceBundle:
    evidence: VerificationEvidence
    results: tuple[CollectorResult, ...]
    blocked: bool
    blocked_collectors: tuple[str, ...]


class CollectorService:
    def __init__(self, collectors: VerificationCollectors):
        self.collectors = collectors

    def _safe_collect(self, name: str, fn, context: VerificationContext) -> CollectorResult:
        try:
            result = fn(context)
        except Exception as exc:
            return CollectorResult(
                collector=name,
                status="BLOCKED",
                detail=f"{type(exc).__name__}: {exc}",
            )

        if result.status not in {"PASS", "FAIL", "BLOCKED"}:
            return CollectorResult(
                collector=name,
                status="BLOCKED",
                detail="invalid_collector_status",
            )
        return result

    def collect(
        self,
        *,
        context: VerificationContext,
        triggers: set[str],
        requirement_ids: tuple[str, ...],
    ) -> CollectedEvidenceBundle:
        requirements = requirements_for_triggers(triggers)

        raw: list[CollectorResult] = [
            self._safe_collect("ci", self.collectors.collect_ci, context),
            self._safe_collect("unit", self.collectors.collect_unit, context),
            self._safe_collect("integration", self.collectors.collect_integration, context),
            self._safe_collect("diff", self.collectors.collect_diff, context),
        ]

        e2e = (
            self._safe_collect("e2e", self.collectors.collect_e2e, context)
            if requirements["requires_e2e"]
            else CollectorResult("e2e", "PASS", detail="not_applicable")
        )
        backend = (
            self._safe_collect("backend", self.collectors.collect_backend, context)
            if requirements["requires_backend"]
            else CollectorResult("backend", "PASS", detail="not_applicable")
        )
        frontend = (
            self._safe_collect("frontend", self.collectors.collect_frontend, context)
            if requirements["requires_frontend"]
            else CollectorResult("frontend", "PASS", detail="not_applicable")
        )
        database = (
            self._safe_collect("database", self.collectors.collect_database, context)
            if requirements["requires_database"]
            else CollectorResult("database", "PASS", detail="not_applicable")
        )
        raw.extend([e2e, backend, frontend, database])

        by_name = {result.collector: result for result in raw}
        blocked = tuple(
            result.collector for result in raw if result.blocked
        )

        evidence = VerificationEvidence(
            requirement_ids=requirement_ids,
            ci_passed=by_name["ci"].passed,
            unit_passed=by_name["unit"].passed,
            integration_passed=by_name["integration"].passed,
            e2e_passed=by_name["e2e"].passed,
            diff_reviewed=by_name["diff"].passed,
            backend_verified=by_name["backend"].passed,
            frontend_verified=by_name["frontend"].passed,
            database_verified=by_name["database"].passed,
            notes=tuple(
                f"{result.collector}:{result.status}:{result.detail or ''}"
                for result in raw
            ),
        )

        return CollectedEvidenceBundle(
            evidence=evidence,
            results=tuple(raw),
            blocked=bool(blocked),
            blocked_collectors=blocked,
        )
