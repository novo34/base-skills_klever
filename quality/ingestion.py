from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from quality.runtime import RequirementQuality


@dataclass(frozen=True)
class RequirementTraceRecord:
    requirement_id: str
    source: str
    status: str
    task_id: str
    branch: str
    pull_request: int | None
    files: tuple[str, ...]
    unit_tests: tuple[str, ...]
    integration_tests: tuple[str, ...]
    e2e_tests: tuple[str, ...]
    verification_result: str
    defects_open: int = 0


class QualityTraceIngestor:
    def from_trace_records(
        self,
        records: list[RequirementTraceRecord],
    ) -> list[RequirementQuality]:
        quality: list[RequirementQuality] = []

        for record in records:
            implemented = bool(record.files) and record.status not in {"MISSING", "PLANNED"}
            verification_status = {
                "PASS": "VERIFIED",
                "FAIL": "FAILED",
                "BLOCKED": "BLOCKED",
                "NOT_RUN": "UNVERIFIED",
            }.get(record.verification_result, "UNVERIFIED")

            quality.append(
                RequirementQuality(
                    requirement_id=record.requirement_id,
                    implemented=implemented,
                    files=tuple(sorted(set(record.files))),
                    unit_covered=bool(record.unit_tests),
                    integration_covered=bool(record.integration_tests),
                    e2e_covered=bool(record.e2e_tests),
                    verification_status=verification_status,
                    defects_open=max(0, record.defects_open),
                )
            )

        return quality

    def from_trace_dicts(
        self,
        records: list[dict[str, Any]],
    ) -> list[RequirementQuality]:
        parsed: list[RequirementTraceRecord] = []
        for record in records:
            implementation = record.get("implementation") or {}
            verification = record.get("verification") or {}
            parsed.append(
                RequirementTraceRecord(
                    requirement_id=record["id"],
                    source=record.get("source", ""),
                    status=record.get("status", "MISSING"),
                    task_id=implementation.get("task_id", ""),
                    branch=implementation.get("branch", ""),
                    pull_request=implementation.get("pull_request"),
                    files=tuple(implementation.get("files") or ()),
                    unit_tests=tuple(verification.get("unit_tests") or ()),
                    integration_tests=tuple(verification.get("integration_tests") or ()),
                    e2e_tests=tuple(verification.get("e2e_tests") or ()),
                    verification_result=verification.get("result", "NOT_RUN"),
                    defects_open=int(record.get("defects_open", 0) or 0),
                )
            )
        return self.from_trace_records(parsed)
