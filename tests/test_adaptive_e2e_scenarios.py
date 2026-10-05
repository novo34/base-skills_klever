import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.adaptive import (
    BlueprintStep,
    ExecutionBlueprint,
    PlanRevision,
    compile_workflow,
    validate_plan_revision,
)
from agents_runtime.evolution import (
    ScenarioResult,
    SelfImprovementRelease,
    compare_counterfactual,
    validate_self_improvement_release,
)
from agents_runtime.governance import (
    RequirementEdge,
    RequirementNode,
    validate_requirement_trace_completeness,
)
from agents_runtime.hygiene import (
    CleanupEvidence,
    HygieneContractError,
    classify_candidate,
    validate_cleanup_evidence,
)
from audit.runtime import AuditEvent, validate_audit_event


def assert_audit(action: str, result: str = "SUCCESS"):
    event = AuditEvent(
        event_id=f"AUD-{action}",
        actor="jev",
        actor_type="SYSTEM",
        action=action,
        project_id="project-a",
        object_type="task",
        object_id="TASK-1",
        task_id="TASK-1",
        result=result,
        timestamp="2026-10-05T10:00:00Z",
        rationale="adaptive e2e scenario",
    )
    ok, failures = validate_audit_event(event)
    assert ok, failures


def test_e2e_trivial_visual_change_is_light_but_requires_browser_evidence():
    workflow = compile_workflow(
        task_id="TASK-UI",
        intent_depth="L0",
        risk="R0",
        change_radius="LOCAL",
        capabilities=("developer", "verifier"),
        required_evidence=(),
        browser_dependent=True,
    )
    assert workflow.budget_class == "LIGHT"
    assert "browser_runtime_evidence" in workflow.evidence_requirements
    assert "no_direct_main_write" in workflow.gates
    assert_audit("compile_visual_workflow")


def test_e2e_business_logic_defect_requires_regression_and_verification():
    workflow = compile_workflow(
        task_id="TASK-BUG",
        intent_depth="L1",
        risk="R1",
        change_radius="COMPONENT",
        capabilities=("developer", "verifier"),
        required_evidence=(),
        behavior_change=True,
    )
    assert "regression_evidence" in workflow.evidence_requirements
    assert "independent_verification" in workflow.gates
    assert_audit("compile_bugfix_workflow")


def test_e2e_architectural_change_is_deep_and_traced():
    workflow = compile_workflow(
        task_id="TASK-ARCH",
        intent_depth="L3",
        risk="R3",
        change_radius="ARCHITECTURAL",
        capabilities=("architect", "developer", "verifier"),
        required_evidence=("adr",),
        architectural_change=True,
    )
    assert workflow.budget_class == "DEEP"
    assert "architecture_evidence" in workflow.evidence_requirements

    nodes = (
        RequirementNode("GOAL-1", "BUSINESS_GOAL", "Goal"),
        RequirementNode("CAP-1", "PRD_CAPABILITY", "Capability"),
        RequirementNode("REQ-1", "SPEC_REQUIREMENT", "Requirement"),
        RequirementNode("TASK-ARCH", "TASK", "Task"),
        RequirementNode("CODE-1", "CODE", "Code"),
        RequirementNode("TEST-1", "TEST", "Test"),
        RequirementNode("EVID-1", "EVIDENCE", "Evidence"),
    )
    edges = (
        RequirementEdge("GOAL-1", "CAP-1", "REFINES"),
        RequirementEdge("CAP-1", "REQ-1", "REFINES"),
        RequirementEdge("REQ-1", "TASK-ARCH", "IMPLEMENTS"),
        RequirementEdge("TASK-ARCH", "CODE-1", "IMPLEMENTS"),
        RequirementEdge("CODE-1", "TEST-1", "VERIFIES"),
        RequirementEdge("TEST-1", "EVID-1", "EVIDENCES"),
    )
    validate_requirement_trace_completeness(nodes, edges)
    assert_audit("architectural_trace_verified")


def test_e2e_plan_mutation_requires_new_valid_revision():
    original = ExecutionBlueprint(
        blueprint_id="BP-1",
        task_id="TASK-PLAN",
        revision=1,
        objective="Initial",
        steps=(BlueprintStep("A", "Inspect", exit_criteria=("done",)),),
        completion_criteria=("done",),
    )
    revised = ExecutionBlueprint(
        blueprint_id="BP-1",
        task_id="TASK-PLAN",
        revision=2,
        objective="Initial",
        steps=(
            BlueprintStep("A", "Inspect", exit_criteria=("done",)),
            BlueprintStep("B", "Migrate", dependencies=("A",), exit_criteria=("done",)),
        ),
        completion_criteria=("done",),
    )
    revision = PlanRevision(
        revision_id="REV-2",
        blueprint_id="BP-1",
        from_revision=1,
        to_revision=2,
        actor="architect",
        reason="migration discovered",
        evidence=("schema inspection",),
        operations=("INSERT",),
        dependency_impact=("B after A",),
        risk_impact="R1->R2",
        budget_impact="standard",
    )
    assert original.revision == 1
    validate_plan_revision(
        revision,
        current_revision=1,
        revalidated_blueprint=revised,
    )
    assert_audit("plan_revised")


def test_e2e_repository_cleanup_blocks_uncertain_dynamic_deletion():
    classification = classify_candidate(
        "src/plugin_loader.php",
        referenced=False,
        dynamic_or_reflection=True,
    )
    assert classification.classification == "POSSIBLY_DYNAMIC"

    try:
        validate_cleanup_evidence(
            CleanupEvidence(
                added=(),
                replaced=("legacy.php",),
                removed=(),
                retained_for_compatibility=(),
                temporary_created=(),
                temporary_removed=(),
                residual_debt=(),
            )
        )
    except HygieneContractError:
        assert_audit("cleanup_blocked", result="BLOCKED")
        return
    raise AssertionError("incomplete cleanup must block")


def test_e2e_supervised_self_improvement_requires_benchmark_human_and_canary():
    baseline = (
        ScenarioResult("S1", 0.80, True, 1.0, 1000, 1, True),
    )
    candidate = (
        ScenarioResult("S1", 0.90, True, 0.8, 900, 0, True),
    )
    report = compare_counterfactual(
        corpus_version="v1",
        baseline_version="base",
        candidate_version="candidate",
        baseline_results=baseline,
        candidate_results=candidate,
    )
    assert report.verdict == "PASS"

    release = SelfImprovementRelease(
        candidate_id="IC-1",
        benchmark_report="EVAL-1",
        human_approval=True,
        canary_scope=("project-a",),
        rollback_proof="restore baseline commit",
        monitoring_metrics=("quality", "safety", "cost"),
        canary_result="PASS",
        promotion_status="READY_TO_PROMOTE",
    )
    validate_self_improvement_release(
        release,
        benchmark_verdict=report.verdict,
        affected_controls=(),
    )
    assert_audit("self_improvement_ready_to_promote")
