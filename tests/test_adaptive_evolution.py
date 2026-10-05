import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.evolution import (
    CounterfactualEvalReport,
    EvolutionContractError,
    ImprovementCandidate,
    LearningCandidate,
    ScenarioResult,
    SelfImprovementRelease,
    SkillHealthReport,
    build_improvement_candidate,
    classify_skill_health,
    compare_counterfactual,
    validate_learning_candidate,
    validate_self_improvement_release,
)


def test_skill_health_requires_evidence_and_consistent_counts():
    report = SkillHealthReport(
        skill_id="25-source-grounded-development",
        activation_count=10,
        successful_activations=8,
        false_activations=1,
        missed_activations=0,
        verifier_failure_rate=0.1,
        correction_rate=0.1,
        average_cost=0.2,
        average_latency_ms=1200,
        overlap_score=0.2,
        freshness="2026-10-05",
        benchmark_status="PASS",
        recommendation="KEEP",
        evidence=("E1",),
    )
    assert classify_skill_health(report) == "KEEP"


def test_skill_health_merge_requires_target():
    report = SkillHealthReport(
        skill_id="x",
        activation_count=1,
        successful_activations=1,
        false_activations=0,
        missed_activations=0,
        verifier_failure_rate=0.0,
        correction_rate=0.0,
        average_cost=0.0,
        average_latency_ms=1,
        overlap_score=0.9,
        freshness="2026-10-05",
        benchmark_status="PASS",
        recommendation="MERGE",
        evidence=("E1",),
    )
    try:
        classify_skill_health(report)
    except EvolutionContractError as exc:
        assert "skill_merge_target_required" in str(exc)
        return
    raise AssertionError("MERGE must name a target")


def test_global_learning_cannot_self_approve():
    candidate = LearningCandidate(
        candidate_id="LC-1",
        kind="GLOBAL_RULE",
        scope="global",
        statement="Always do X",
        confidence=0.9,
        evidence=("E1",),
        contradictions=(),
        source_events=("EV-1",),
        status="APPROVED",
    )
    try:
        validate_learning_candidate(candidate)
    except EvolutionContractError as exc:
        assert "global_learning_requires_external_evaluation_and_approval" in str(exc)
        return
    raise AssertionError("global learning must not self-approve")


def test_improvement_candidate_requires_evidence_and_rollback():
    candidate = build_improvement_candidate(
        candidate_id="IC-1",
        problem="False activations",
        evidence=("metric:0.3",),
        improvement_type="SKILL",
        proposed_change="Tighten triggers",
        expected_benefit="Lower false positives",
        risk="R1",
        affected_contracts=("skills-manifest.yaml",),
        rollback_concept="restore previous manifest",
        evaluation_plan="replay corpus",
    )
    assert isinstance(candidate, ImprovementCandidate)
    assert candidate.status == "CANDIDATE"


def test_counterfactual_fails_on_quality_regression():
    baseline = (
        ScenarioResult("S1", 0.9, True, 1.0, 1000, 1, True),
    )
    candidate = (
        ScenarioResult("S1", 0.8, True, 0.5, 700, 0, True),
    )
    report = compare_counterfactual(
        corpus_version="v1",
        baseline_version="base",
        candidate_version="cand",
        baseline_results=baseline,
        candidate_results=candidate,
    )
    assert isinstance(report, CounterfactualEvalReport)
    assert report.verdict == "FAIL"
    assert "S1:quality" in report.regressions


def test_counterfactual_safety_regression_has_veto():
    baseline = (
        ScenarioResult("S1", 0.8, True, 1.0, 1000, 1, True),
    )
    candidate = (
        ScenarioResult("S1", 1.0, False, 0.1, 100, 0, True),
    )
    report = compare_counterfactual(
        corpus_version="v1",
        baseline_version="base",
        candidate_version="cand",
        baseline_results=baseline,
        candidate_results=candidate,
    )
    assert report.verdict == "FAIL"
    assert "S1:critical_safety" in report.regressions


def test_self_improvement_requires_human_approval_and_rollback_proof():
    release = SelfImprovementRelease(
        candidate_id="IC-1",
        benchmark_report="EVAL-1",
        human_approval=False,
        canary_scope=("project-a",),
        rollback_proof="restore baseline",
        monitoring_metrics=("quality",),
        canary_result="PASS",
        promotion_status="READY_TO_PROMOTE",
    )
    try:
        validate_self_improvement_release(
            release,
            benchmark_verdict="PASS",
            affected_controls=(),
        )
    except EvolutionContractError as exc:
        assert "self_improvement_human_approval_required" in str(exc)
        return
    raise AssertionError("human approval must be required")


def test_self_improvement_cannot_weaken_protected_controls():
    release = SelfImprovementRelease(
        candidate_id="IC-1",
        benchmark_report="EVAL-1",
        human_approval=True,
        canary_scope=("project-a",),
        rollback_proof="restore baseline",
        monitoring_metrics=("quality",),
        canary_result="PASS",
        promotion_status="READY_TO_PROMOTE",
    )
    try:
        validate_self_improvement_release(
            release,
            benchmark_verdict="PASS",
            affected_controls=("human_approval",),
        )
    except EvolutionContractError as exc:
        assert "protected_controls_change_forbidden" in str(exc)
        return
    raise AssertionError("protected controls must be immutable from self-improvement")


def test_failed_canary_must_rollback():
    release = SelfImprovementRelease(
        candidate_id="IC-1",
        benchmark_report="EVAL-1",
        human_approval=True,
        canary_scope=("project-a",),
        rollback_proof="restore baseline",
        monitoring_metrics=("quality",),
        canary_result="FAIL",
        promotion_status="READY_TO_PROMOTE",
    )
    try:
        validate_self_improvement_release(
            release,
            benchmark_verdict="PASS",
            affected_controls=(),
        )
    except EvolutionContractError as exc:
        assert "failed_canary_must_rollback" in str(exc)
        return
    raise AssertionError("failed canary must force rollback")
