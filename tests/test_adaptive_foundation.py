import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.adaptive import (
    AdaptiveContractError,
    BlueprintStep,
    ContextRetrievalPlan,
    ExecutionBlueprint,
    PlanRevision,
    compile_workflow,
    validate_blueprint,
    validate_context_retrieval_plan,
    validate_plan_revision,
)


def sample_blueprint(revision=1):
    return ExecutionBlueprint(
        blueprint_id="BP-1",
        task_id="TASK-1",
        revision=revision,
        objective="Implement safely",
        steps=(
            BlueprintStep(
                step_id="A",
                objective="Inspect",
                exit_criteria=("sources identified",),
            ),
            BlueprintStep(
                step_id="B",
                objective="Implement",
                dependencies=("A",),
                affected_resources=("src/app.py",),
                capabilities=("developer",),
                evidence_required=("unit",),
                exit_criteria=("tests pass",),
            ),
            BlueprintStep(
                step_id="C",
                objective="Verify",
                dependencies=("B",),
                capabilities=("verifier",),
                evidence_required=("independent",),
                exit_criteria=("verified",),
            ),
        ),
        required_capabilities=("developer", "verifier"),
        required_evidence=("unit", "independent"),
        completion_criteria=("verified",),
    )


def test_blueprint_validates_acyclic_dependencies():
    validate_blueprint(sample_blueprint())


def test_blueprint_rejects_cycle():
    blueprint = ExecutionBlueprint(
        blueprint_id="BP-CYCLE",
        task_id="TASK-1",
        revision=1,
        objective="Cycle",
        steps=(
            BlueprintStep("A", "A", dependencies=("B",), exit_criteria=("done",)),
            BlueprintStep("B", "B", dependencies=("A",), exit_criteria=("done",)),
        ),
        completion_criteria=("done",),
    )
    try:
        validate_blueprint(blueprint)
    except AdaptiveContractError as exc:
        assert "blueprint_dependency_cycle" in str(exc)
        return
    raise AssertionError("cycle must fail")


def test_blueprint_rejects_parallel_resource_conflict():
    blueprint = ExecutionBlueprint(
        blueprint_id="BP-PAR",
        task_id="TASK-1",
        revision=1,
        objective="Parallel",
        steps=(
            BlueprintStep("A", "A", affected_resources=("x.py",), exit_criteria=("done",)),
            BlueprintStep("B", "B", affected_resources=("x.py",), exit_criteria=("done",)),
        ),
        parallel_groups=(("A", "B"),),
        completion_criteria=("done",),
    )
    try:
        validate_blueprint(blueprint)
    except AdaptiveContractError as exc:
        assert "parallel_resource_conflict" in str(exc)
        return
    raise AssertionError("shared writable resource must fail")


def test_workflow_compiler_never_under_scopes_r4():
    workflow = compile_workflow(
        task_id="TASK-9",
        intent_depth="L0",
        risk="R4",
        change_radius="LOCAL",
        capabilities=("developer", "verifier"),
        required_evidence=("unit",),
    )
    assert workflow.budget_class == "CRITICAL"
    assert "human_approval" in workflow.gates
    assert "independent_verification" in workflow.gates


def test_workflow_compiler_adds_browser_and_regression_evidence():
    workflow = compile_workflow(
        task_id="TASK-2",
        intent_depth="L1",
        risk="R1",
        change_radius="COMPONENT",
        capabilities=("developer", "verifier"),
        required_evidence=(),
        browser_dependent=True,
        behavior_change=True,
    )
    assert "browser_runtime_evidence" in workflow.evidence_requirements
    assert "regression_evidence" in workflow.evidence_requirements


def test_plan_revision_requires_sequential_revision_and_revalidates_blueprint():
    revision = PlanRevision(
        revision_id="REV-2",
        blueprint_id="BP-1",
        from_revision=1,
        to_revision=2,
        actor="architect",
        reason="New migration dependency",
        evidence=("schema inspection",),
        operations=("INSERT",),
        dependency_impact=("migration before implementation",),
        risk_impact="R1->R2",
        budget_impact="standard",
    )
    validate_plan_revision(
        revision,
        current_revision=1,
        revalidated_blueprint=sample_blueprint(revision=2),
    )


def test_stale_plan_revision_is_rejected():
    revision = PlanRevision(
        revision_id="REV-2",
        blueprint_id="BP-1",
        from_revision=1,
        to_revision=2,
        actor="architect",
        reason="change",
        evidence=(),
        operations=("INSERT",),
        dependency_impact=(),
        risk_impact="none",
        budget_impact="none",
    )
    try:
        validate_plan_revision(
            revision,
            current_revision=2,
            revalidated_blueprint=sample_blueprint(revision=2),
        )
    except AdaptiveContractError as exc:
        assert "stale_plan_revision" in str(exc)
        return
    raise AssertionError("stale revision must fail")


def test_context_retrieval_plan_is_bounded():
    validate_context_retrieval_plan(
        ContextRetrievalPlan(
            task_id="TASK-1",
            budget=12000,
            max_iterations=4,
            required_queries=("contract", "implementation"),
            optional_queries=("history",),
            stop_when=("required context satisfied",),
        )
    )


def test_context_retrieval_rejects_unbounded_iterations():
    try:
        validate_context_retrieval_plan(
            ContextRetrievalPlan(
                task_id="TASK-1",
                budget=1000,
                max_iterations=99,
                required_queries=(),
                optional_queries=(),
                stop_when=("done",),
            )
        )
    except AdaptiveContractError as exc:
        assert "context_iteration_limit_invalid" in str(exc)
        return
    raise AssertionError("unbounded retrieval must fail")
