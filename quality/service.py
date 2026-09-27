from __future__ import annotations

from collections import Counter

from quality.runtime import RequirementQuality, quality_status


class QualityService:
    def summarize(self, requirements: list[RequirementQuality]) -> dict:
        statuses = [quality_status(item) for item in requirements]
        counts = Counter(statuses)

        return {
            "total": len(requirements),
            "verified": counts.get("VERIFIED", 0),
            "unverified": counts.get("UNVERIFIED", 0),
            "missing_implementation": counts.get("MISSING_IMPLEMENTATION", 0),
            "failed": counts.get("FAILED", 0),
            "defects_open": counts.get("DEFECTS_OPEN", 0),
            "missing_unit": counts.get("MISSING_UNIT", 0),
            "coverage_pct": (
                round((counts.get("VERIFIED", 0) / len(requirements)) * 100, 2)
                if requirements else 100.0
            ),
            "requirements": [
                {
                    "requirement_id": item.requirement_id,
                    "status": quality_status(item),
                    "implemented": item.implemented,
                    "files": list(item.files),
                    "unit": item.unit_covered,
                    "integration": item.integration_covered,
                    "e2e": item.e2e_covered,
                    "verification": item.verification_status,
                    "defects_open": item.defects_open,
                }
                for item in requirements
            ],
        }
