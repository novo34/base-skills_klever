from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Iterable


class HygieneContractError(ValueError):
    pass


CLASSIFICATIONS = {
    "SAFE_TO_DELETE",
    "LIKELY_DEAD",
    "POSSIBLY_DYNAMIC",
    "GENERATED_REQUIRED",
    "TEST_ARTIFACT",
    "UNKNOWN",
}


TEMP_MARKERS = (
    ".tmp",
    ".temp",
    ".bak",
    ".backup",
    ".old",
    ".orig",
    ".log",
)
TEMP_NAMES = {
    "debug.txt",
    "debug.log",
    "tmp.json",
    "output.json",
    "test123.php",
}


@dataclass(frozen=True)
class HygieneClassification:
    item: str
    classification: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class ReuseDecision:
    proposed_surface: str
    candidates: tuple[str, ...]
    similarity_evidence: tuple[str, ...]
    decision: str
    selected_candidate: str | None
    rationale: str


@dataclass(frozen=True)
class CleanupEvidence:
    added: tuple[str, ...]
    replaced: tuple[str, ...]
    removed: tuple[str, ...]
    retained_for_compatibility: tuple[tuple[str, str], ...]
    temporary_created: tuple[str, ...]
    temporary_removed: tuple[str, ...]
    residual_debt: tuple[str, ...]


@dataclass(frozen=True)
class RepositoryHealth:
    dead_code_candidates: int
    duplicate_blocks: int
    orphan_files: int
    temporary_artifacts: int
    unused_dependencies: int
    stale_todos: int
    generated_drift: int
    cleanup_debt_score: float
    baseline_cleanup_debt_score: float


def classify_candidate(
    item: str,
    *,
    referenced: bool,
    dynamic_or_reflection: bool = False,
    generated_required: bool = False,
    test_artifact: bool = False,
    explicit_safe_delete: bool = False,
) -> HygieneClassification:
    evidence: list[str] = []

    if generated_required:
        return HygieneClassification(
            item, "GENERATED_REQUIRED", ("generated_required",)
        )
    if dynamic_or_reflection:
        return HygieneClassification(
            item, "POSSIBLY_DYNAMIC", ("dynamic_or_reflection",)
        )
    if test_artifact:
        return HygieneClassification(
            item, "TEST_ARTIFACT", ("test_artifact",)
        )
    if explicit_safe_delete:
        return HygieneClassification(
            item, "SAFE_TO_DELETE", ("explicit_safe_delete",)
        )
    if referenced:
        return HygieneClassification(item, "UNKNOWN", ("referenced",))
    return HygieneClassification(item, "LIKELY_DEAD", ("no_static_reference",))


def detect_temporary_artifacts(paths: Iterable[str]) -> tuple[str, ...]:
    found: list[str] = []
    for raw in paths:
        path = raw.replace("\\", "/")
        name = PurePosixPath(path).name.lower()
        lower = path.lower()

        if name in TEMP_NAMES:
            found.append(path)
            continue
        if any(name.endswith(marker) for marker in TEMP_MARKERS):
            found.append(path)
            continue
        if any(
            token in lower
            for token in ("/tmp/", "/temp/", "/debug/", "/scratch/")
        ):
            found.append(path)
            continue
        if any(
            token in name
            for token in ("_copy.", "-copy.", "_backup.", "-backup.")
        ):
            found.append(path)

    return tuple(sorted(set(found)))


def decide_reuse(
    *,
    proposed_surface: str,
    candidates: Iterable[tuple[str, float]],
    searched: bool,
    create_new_rationale: str = "",
    strong_similarity_threshold: float = 0.85,
) -> ReuseDecision:
    if not searched:
        raise HygieneContractError("reuse_search_required")

    ranked = sorted(candidates, key=lambda item: (-item[1], item[0]))
    candidate_names = tuple(item[0] for item in ranked)
    evidence = tuple(f"{name}:{score:.3f}" for name, score in ranked)

    strong = [item for item in ranked if item[1] >= strong_similarity_threshold]
    if strong and not create_new_rationale:
        return ReuseDecision(
            proposed_surface=proposed_surface,
            candidates=candidate_names,
            similarity_evidence=evidence,
            decision="BLOCK_DUPLICATE",
            selected_candidate=strong[0][0],
            rationale="strong_equivalent_candidate_requires_reuse_or_explicit_rationale",
        )

    if strong and create_new_rationale:
        return ReuseDecision(
            proposed_surface=proposed_surface,
            candidates=candidate_names,
            similarity_evidence=evidence,
            decision="CREATE_NEW",
            selected_candidate=None,
            rationale=create_new_rationale,
        )

    if ranked:
        return ReuseDecision(
            proposed_surface=proposed_surface,
            candidates=candidate_names,
            similarity_evidence=evidence,
            decision="EXTEND",
            selected_candidate=ranked[0][0],
            rationale="existing_candidate_preferred_for_review",
        )

    return ReuseDecision(
        proposed_surface=proposed_surface,
        candidates=(),
        similarity_evidence=(),
        decision="CREATE_NEW",
        selected_candidate=None,
        rationale=create_new_rationale or "no_existing_candidate_found",
    )


def validate_cleanup_evidence(evidence: CleanupEvidence) -> None:
    replaced = set(evidence.replaced)
    removed = set(evidence.removed)
    retained = {item for item, reason in evidence.retained_for_compatibility if reason}

    incomplete = replaced - removed - retained
    if incomplete:
        raise HygieneContractError(
            "incomplete_cleanup:" + ",".join(sorted(incomplete))
        )

    missing_temp_cleanup = (
        set(evidence.temporary_created) - set(evidence.temporary_removed)
    )
    if missing_temp_cleanup:
        raise HygieneContractError(
            "temporary_artifacts_not_cleaned:"
            + ",".join(sorted(missing_temp_cleanup))
        )


def validate_health_delta(health: RepositoryHealth) -> None:
    counts = (
        health.dead_code_candidates,
        health.duplicate_blocks,
        health.orphan_files,
        health.temporary_artifacts,
        health.unused_dependencies,
        health.stale_todos,
        health.generated_drift,
    )
    if any(value < 0 for value in counts):
        raise HygieneContractError("repository_health_negative_count")
    if health.cleanup_debt_score < 0 or health.baseline_cleanup_debt_score < 0:
        raise HygieneContractError("repository_health_negative_debt")
    if health.cleanup_debt_score > health.baseline_cleanup_debt_score:
        raise HygieneContractError("cleanup_debt_regression")
