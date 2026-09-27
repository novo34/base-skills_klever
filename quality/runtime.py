from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RequirementQuality:
    requirement_id: str
    implemented: bool
    files: tuple[str, ...] = ()
    unit_covered: bool = False
    integration_covered: bool = False
    e2e_covered: bool = False
    verification_status: str = "UNVERIFIED"
    defects_open: int = 0


def quality_status(item: RequirementQuality) -> str:
    if not item.implemented:
        return "MISSING_IMPLEMENTATION"
    if item.defects_open > 0:
        return "DEFECTS_OPEN"
    if item.verification_status == "FAILED":
        return "FAILED"
    if item.verification_status != "VERIFIED":
        return "UNVERIFIED"
    if not item.unit_covered:
        return "MISSING_UNIT"
    return "VERIFIED"
