from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


RISK_ORDER = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4}
DEPTH_ORDER = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4}
RADIUS_ORDER = {
    "LOCAL": 0,
    "COMPONENT": 1,
    "CROSS_LAYER": 2,
    "ARCHITECTURAL": 3,
    "PRODUCT": 4,
}
BUDGET_CLASS = {0: "LIGHT", 1: "STANDARD", 2: "STANDARD", 3: "DEEP", 4: "CRITICAL"}


class AdaptiveContractError(ValueError):
    pass


@dataclass(frozen=True)
class BlueprintStep:
    step_id: str
    objective: str
    dependencies: tuple[str, ...] = ()
    affected_resources: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()
    evidence_required: tuple[str, ...] = ()
    exit_criteria: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExecutionBlueprint:
    blueprint_id: str
    task_id: str
    revision: int
    objective: str
    steps: tuple[BlueprintStep, ...]
    source_requirements: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    parallel_groups: tuple[tuple[str, ...], ...] = ()
    required_capabilities: tuple[str, ...] = ()
    required_evidence: tuple[str, ...] = ()
    rollback_strategy: str = "restore_previous_known_good_state"
    completion_criteria: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExecutionStepHandoff:
    handoff_id: str
    task_id: str
    blueprint_id: str
    blueprint_revision: int
    step_id: str
    agent_role: str
    context_pack_ref: str
    objective: str
    inputs: tuple[str, ...] = ()
    expected_outputs: tuple[str, ...] = ()
    evidence_required: tuple[str, ...] = ()
    exit_criteria: tuple[str, ...] = ()
    authorized_resources: tuple[str, ...] = ()


@dataclass(frozen=True)
class AdaptiveWorkflow:
    workflow_id: str
    task_id: str
    intent_depth: str
    risk: str
    change_radius: str
    capabilities: tuple[str, ...]
    steps: tuple[str, ...]
    gates: tuple[str, ...]
    evidence_requirements: tuple[str, ...]
    budget_class: str


@dataclass(frozen=True)
class PlanRevision:
    revision_id: str
    blueprint_id: str
    from_revision: int
    to_revision: int
    actor: str
    reason: str
    evidence: tuple[str, ...]
    operations: tuple[str, ...]
    dependency_impact: tuple[str, ...]
    risk_impact: str
    budget_impact: str


@dataclass(frozen=True)
class ContextRetrievalPlan:
    task_id: str
    budget: int
    max_iterations: int
    required_queries: tuple[str, ...]
    optional_queries: tuple[str, ...]
    stop_when: tuple[str, ...]


def _validate_unique(values: Iterable[str], error: str) -> None:
    values = tuple(values)
    if len(values) != len(set(values)):
        raise AdaptiveContractError(error)


def validate_blueprint(blueprint: ExecutionBlueprint) -> None:
    if not blueprint.blueprint_id or not blueprint.task_id or not blueprint.objective:
        raise AdaptiveContractError("blueprint_identity_required")
    if blueprint.revision < 1:
        raise AdaptiveContractError("blueprint_revision_invalid")
    if not blueprint.steps:
        raise AdaptiveContractError("blueprint_steps_required")
    if not blueprint.completion_criteria:
        raise AdaptiveContractError("blueprint_completion_criteria_required")

    ids = tuple(step.step_id for step in blueprint.steps)
    _validate_unique(ids, "duplicate_blueprint_step_id")
    known = set(ids)

    for step in blueprint.steps:
        if not step.step_id or not step.objective:
            raise AdaptiveContractError("blueprint_step_identity_required")
        if not step.exit_criteria:
            raise AdaptiveContractError(f"step_exit_criteria_required:{step.step_id}")
        if step.step_id in step.dependencies:
            raise AdaptiveContractError(f"self_dependency_forbidden:{step.step_id}")
        for dependency in step.dependencies:
            if dependency not in known:
                raise AdaptiveContractError(
                    f"unknown_blueprint_dependency:{step.step_id}:{dependency}"
                )

    visiting: set[str] = set()
    visited: set[str] = set()
    by_id = {step.step_id: step for step in blueprint.steps}

    def visit(step_id: str, path: tuple[str, ...]) -> None:
        if step_id in visited:
            return
        if step_id in visiting:
            raise AdaptiveContractError(
                "blueprint_dependency_cycle:" + "->".join(path + (step_id,))
            )
        visiting.add(step_id)
        for dependency in by_id[step_id].dependencies:
            visit(dependency, path + (step_id,))
        visiting.remove(step_id)
        visited.add(step_id)

    for step_id in sorted(known):
        visit(step_id, ())

    seen_parallel: set[str] = set()
    for group in blueprint.parallel_groups:
        if len(group) < 2:
            raise AdaptiveContractError("parallel_group_too_small")
        _validate_unique(group, "parallel_group_duplicate_step")
        for step_id in group:
            if step_id not in known:
                raise AdaptiveContractError(f"parallel_group_unknown_step:{step_id}")
            if step_id in seen_parallel:
                raise AdaptiveContractError(f"step_in_multiple_parallel_groups:{step_id}")
            seen_parallel.add(step_id)

        group_set = set(group)
        for step_id in group:
            if group_set.intersection(by_id[step_id].dependencies):
                raise AdaptiveContractError(
                    f"parallel_dependency_conflict:{step_id}"
                )

        locks: dict[str, str] = {}
        for step_id in group:
            for resource in by_id[step_id].affected_resources:
                prior = locks.get(resource)
                if prior is not None:
                    raise AdaptiveContractError(
                        f"parallel_resource_conflict:{prior}:{step_id}:{resource}"
                    )
                locks[resource] = step_id


def build_step_handoff(
    *,
    blueprint: ExecutionBlueprint,
    step_id: str,
    handoff_id: str,
    agent_role: str,
    context_pack_ref: str,
    authorized_resources: Iterable[str] = (),
) -> ExecutionStepHandoff:
    validate_blueprint(blueprint)
    step = next((item for item in blueprint.steps if item.step_id == step_id), None)
    if step is None:
        raise AdaptiveContractError("blueprint_step_not_found")
    if not handoff_id or not agent_role or not context_pack_ref:
        raise AdaptiveContractError("step_handoff_identity_required")

    authorized = tuple(sorted(set(authorized_resources)))
    unauthorized = set(step.affected_resources) - set(authorized)
    if unauthorized:
        raise AdaptiveContractError(
            "step_handoff_missing_authorized_resource:" + ",".join(sorted(unauthorized))
        )

    return ExecutionStepHandoff(
        handoff_id=handoff_id,
        task_id=blueprint.task_id,
        blueprint_id=blueprint.blueprint_id,
        blueprint_revision=blueprint.revision,
        step_id=step.step_id,
        agent_role=agent_role,
        context_pack_ref=context_pack_ref,
        objective=step.objective,
        inputs=(),
        expected_outputs=(),
        evidence_required=step.evidence_required,
        exit_criteria=step.exit_criteria,
        authorized_resources=authorized,
    )


def compile_workflow(
    *,
    task_id: str,
    intent_depth: str,
    risk: str,
    change_radius: str,
    capabilities: Iterable[str],
    required_evidence: Iterable[str],
    browser_dependent: bool = False,
    behavior_change: bool = False,
    architectural_change: bool = False,
) -> AdaptiveWorkflow:
    if intent_depth not in DEPTH_ORDER:
        raise AdaptiveContractError("invalid_intent_depth")
    if risk not in RISK_ORDER:
        raise AdaptiveContractError("invalid_risk")
    if change_radius not in RADIUS_ORDER:
        raise AdaptiveContractError("invalid_change_radius")

    level = max(
        DEPTH_ORDER[intent_depth],
        RISK_ORDER[risk],
        RADIUS_ORDER[change_radius],
    )
    evidence = set(required_evidence)
    steps = ["ground_sources", "execute_blueprint", "verify"]
    gates = ["no_direct_main_write"]

    if behavior_change:
        evidence.add("regression_evidence")
    if browser_dependent:
        evidence.add("browser_runtime_evidence")
    if architectural_change or level >= 3:
        evidence.add("architecture_evidence")
        steps.insert(1, "architecture_review")
    if risk != "R0":
        gates.append("independent_verification")
    if risk == "R4":
        gates.append("human_approval")
    if level >= 2:
        steps.insert(1, "acceptance_contract_review")

    unique_capabilities = tuple(sorted(set(capabilities)))
    if not unique_capabilities:
        raise AdaptiveContractError("workflow_capability_required")

    return AdaptiveWorkflow(
        workflow_id=f"WF-{task_id}",
        task_id=task_id,
        intent_depth=intent_depth,
        risk=risk,
        change_radius=change_radius,
        capabilities=unique_capabilities,
        steps=tuple(steps),
        gates=tuple(gates),
        evidence_requirements=tuple(sorted(evidence)),
        budget_class=BUDGET_CLASS[level],
    )


def validate_plan_revision(
    revision: PlanRevision,
    *,
    current_revision: int,
    revalidated_blueprint: ExecutionBlueprint,
) -> None:
    if revision.from_revision != current_revision:
        raise AdaptiveContractError("stale_plan_revision")
    if revision.to_revision != current_revision + 1:
        raise AdaptiveContractError("non_sequential_plan_revision")
    if not revision.actor or not revision.reason:
        raise AdaptiveContractError("plan_revision_actor_reason_required")
    if not revision.operations:
        raise AdaptiveContractError("plan_revision_operation_required")
    allowed = {"INSERT", "SPLIT", "REORDER", "BLOCK", "REPLACE", "REMOVE"}
    if any(operation not in allowed for operation in revision.operations):
        raise AdaptiveContractError("invalid_plan_revision_operation")
    validate_blueprint(revalidated_blueprint)
    if revalidated_blueprint.revision != revision.to_revision:
        raise AdaptiveContractError("revalidated_blueprint_revision_mismatch")


def validate_context_ready(
    *,
    missing_required: Iterable[str],
    budget_used: int,
    budget: int,
    iterations: int,
    max_iterations: int,
) -> None:
    missing = tuple(missing_required)
    if budget < 1 or budget_used < 0:
        raise AdaptiveContractError("context_budget_invalid")
    if budget_used > budget:
        raise AdaptiveContractError("context_budget_exceeded")
    if iterations < 0 or iterations > max_iterations:
        raise AdaptiveContractError("context_iteration_limit_exceeded")
    if missing:
        raise AdaptiveContractError(
            "context_required_missing:" + ",".join(sorted(set(missing)))
        )


def validate_context_retrieval_plan(plan: ContextRetrievalPlan) -> None:
    if not plan.task_id:
        raise AdaptiveContractError("context_task_required")
    if plan.budget < 1:
        raise AdaptiveContractError("context_budget_invalid")
    if not 1 <= plan.max_iterations <= 8:
        raise AdaptiveContractError("context_iteration_limit_invalid")
    if not plan.stop_when:
        raise AdaptiveContractError("context_stop_condition_required")
    _validate_unique(plan.required_queries, "duplicate_required_context_query")
    _validate_unique(plan.optional_queries, "duplicate_optional_context_query")
