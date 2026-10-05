from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


class EvolutionContractError(ValueError):
    pass


PROTECTED_CONTROLS = {
    "authorization",
    "audit",
    "verification",
    "verifier_independence",
    "human_approval",
    "risk_gate",
    "direct_main_write",
}


@dataclass(frozen=True)
class SkillHealthReport:
    skill_id: str
    activation_count: int
    successful_activations: int
    false_activations: int
    missed_activations: int
    verifier_failure_rate: float
    correction_rate: float
    average_cost: float
    average_latency_ms: float
    overlap_score: float
    freshness: str
    benchmark_status: str
    recommendation: str
    evidence: tuple[str, ...]
    merge_target: str | None = None


@dataclass(frozen=True)
class LearningCandidate:
    candidate_id: str
    kind: str
    scope: str
    statement: str
    confidence: float
    evidence: tuple[str, ...]
    contradictions: tuple[str, ...]
    source_events: tuple[str, ...]
    status: str = "CANDIDATE"


@dataclass(frozen=True)
class ImprovementCandidate:
    candidate_id: str
    problem: str
    evidence: tuple[str, ...]
    improvement_type: str
    proposed_change: str
    expected_benefit: str
    risk: str
    affected_contracts: tuple[str, ...]
    rollback_concept: str
    evaluation_plan: str
    status: str = "CANDIDATE"


@dataclass(frozen=True)
class ScenarioResult:
    scenario_id: str
    quality: float
    safety_passed: bool
    cost: float
    latency_ms: float
    corrections: int
    completed: bool
    critical_regression: bool = False


@dataclass(frozen=True)
class CounterfactualEvalReport:
    corpus_version: str
    baseline_version: str
    candidate_version: str
    regressions: tuple[str, ...]
    wins: tuple[str, ...]
    uncertainty: tuple[str, ...]
    verdict: str


@dataclass(frozen=True)
class SelfImprovementRelease:
    candidate_id: str
    benchmark_report: str
    human_approval: bool
    canary_scope: tuple[str, ...]
    rollback_proof: str
    monitoring_metrics: tuple[str, ...]
    canary_result: str
    promotion_status: str


def classify_skill_health(report: SkillHealthReport) -> str:
    if report.recommendation not in {"KEEP", "IMPROVE", "MERGE", "RETIRE", "DEFER"}:
        raise EvolutionContractError("invalid_skill_health_recommendation")
    if report.recommendation == "MERGE" and not report.merge_target:
        raise EvolutionContractError("skill_merge_target_required")
    if report.activation_count < report.successful_activations + report.false_activations:
        raise EvolutionContractError("skill_health_counts_inconsistent")
    for value in (
        report.verifier_failure_rate,
        report.correction_rate,
        report.overlap_score,
    ):
        if not 0 <= value <= 1:
            raise EvolutionContractError("skill_health_rate_out_of_range")
    if report.average_cost < 0 or report.average_latency_ms < 0:
        raise EvolutionContractError("skill_health_negative_metric")
    if not report.evidence:
        raise EvolutionContractError("skill_health_evidence_required")
    return report.recommendation


def validate_learning_candidate(candidate: LearningCandidate) -> None:
    allowed = {
        "OBSERVATION", "HYPOTHESIS", "PATTERN", "PROJECT_RULE",
        "GLOBAL_RULE", "SKILL_CANDIDATE", "POLICY_CANDIDATE",
    }
    if candidate.kind not in allowed:
        raise EvolutionContractError("invalid_learning_candidate_kind")
    if not 0 <= candidate.confidence <= 1:
        raise EvolutionContractError("learning_confidence_out_of_range")
    if not candidate.evidence or not candidate.source_events:
        raise EvolutionContractError("learning_candidate_provenance_required")
    if candidate.kind in {"GLOBAL_RULE", "SKILL_CANDIDATE", "POLICY_CANDIDATE"}:
        if candidate.status == "APPROVED":
            raise EvolutionContractError(
                "global_learning_requires_external_evaluation_and_approval"
            )


def build_improvement_candidate(
    *,
    candidate_id: str,
    problem: str,
    evidence: Iterable[str],
    improvement_type: str,
    proposed_change: str,
    expected_benefit: str,
    risk: str,
    affected_contracts: Iterable[str],
    rollback_concept: str,
    evaluation_plan: str,
) -> ImprovementCandidate:
    evidence = tuple(evidence)
    if not evidence:
        raise EvolutionContractError("improvement_evidence_required")
    if not rollback_concept:
        raise EvolutionContractError("improvement_rollback_required")
    if not evaluation_plan:
        raise EvolutionContractError("improvement_evaluation_plan_required")
    return ImprovementCandidate(
        candidate_id=candidate_id,
        problem=problem,
        evidence=evidence,
        improvement_type=improvement_type,
        proposed_change=proposed_change,
        expected_benefit=expected_benefit,
        risk=risk,
        affected_contracts=tuple(affected_contracts),
        rollback_concept=rollback_concept,
        evaluation_plan=evaluation_plan,
    )


def compare_counterfactual(
    *,
    corpus_version: str,
    baseline_version: str,
    candidate_version: str,
    baseline_results: Iterable[ScenarioResult],
    candidate_results: Iterable[ScenarioResult],
) -> CounterfactualEvalReport:
    baseline = {item.scenario_id: item for item in baseline_results}
    candidate = {item.scenario_id: item for item in candidate_results}

    if set(baseline) != set(candidate) or not baseline:
        raise EvolutionContractError("counterfactual_scenario_set_mismatch")

    regressions: list[str] = []
    wins: list[str] = []
    uncertainty: list[str] = []

    for scenario_id in sorted(baseline):
        base = baseline[scenario_id]
        cand = candidate[scenario_id]

        if cand.critical_regression or (base.safety_passed and not cand.safety_passed):
            regressions.append(f"{scenario_id}:critical_safety")
            continue
        if cand.quality < base.quality:
            regressions.append(f"{scenario_id}:quality")
        elif cand.quality > base.quality:
            wins.append(f"{scenario_id}:quality")

        if cand.completed and not base.completed:
            wins.append(f"{scenario_id}:completion")
        elif base.completed and not cand.completed:
            regressions.append(f"{scenario_id}:completion")

        if cand.cost < base.cost:
            wins.append(f"{scenario_id}:cost")
        if cand.latency_ms < base.latency_ms:
            wins.append(f"{scenario_id}:latency")
        if cand.corrections < base.corrections:
            wins.append(f"{scenario_id}:corrections")

    critical = any(item.endswith(":critical_safety") for item in regressions)
    if critical or regressions:
        verdict = "FAIL"
    elif wins:
        verdict = "PASS"
    else:
        verdict = "INCONCLUSIVE"
        uncertainty.append("no_material_difference")

    return CounterfactualEvalReport(
        corpus_version=corpus_version,
        baseline_version=baseline_version,
        candidate_version=candidate_version,
        regressions=tuple(regressions),
        wins=tuple(wins),
        uncertainty=tuple(uncertainty),
        verdict=verdict,
    )


def validate_self_improvement_release(
    release: SelfImprovementRelease,
    *,
    benchmark_verdict: str,
    affected_controls: Iterable[str],
) -> None:
    affected = set(affected_controls)
    weakened = affected.intersection(PROTECTED_CONTROLS)
    if weakened:
        raise EvolutionContractError(
            "protected_controls_change_forbidden:" + ",".join(sorted(weakened))
        )
    if benchmark_verdict != "PASS":
        raise EvolutionContractError("self_improvement_benchmark_not_passed")
    if not release.human_approval:
        raise EvolutionContractError("self_improvement_human_approval_required")
    if not release.rollback_proof:
        raise EvolutionContractError("self_improvement_rollback_proof_required")
    if not release.canary_scope:
        raise EvolutionContractError("self_improvement_canary_scope_required")
    if not release.monitoring_metrics:
        raise EvolutionContractError("self_improvement_monitoring_required")
    if release.canary_result == "FAIL":
        if release.promotion_status != "ROLLED_BACK":
            raise EvolutionContractError("failed_canary_must_rollback")
    elif release.canary_result == "PASS":
        if release.promotion_status not in {"READY_TO_PROMOTE", "PROMOTED"}:
            raise EvolutionContractError("passed_canary_not_ready")
    else:
        raise EvolutionContractError("self_improvement_canary_not_run")
