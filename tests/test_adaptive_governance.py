import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.governance import (
    ArtifactComment,
    ArtifactReview,
    DecisionRecord,
    GovernanceContractError,
    HarnessCapabilityContract,
    RequirementEdge,
    RequirementNode,
    compose_capabilities,
    impacted_nodes,
    review_artifact,
    validate_decision_ledger,
    validate_harness_for_workflow,
    validate_requirement_graph,
)


def test_capability_composition_respects_permission_ceiling():
    result = compose_capabilities(
        task_id="TASK-1",
        role="developer",
        requested_capabilities=("php", "production_merge"),
        available_capabilities=("php", "production_merge"),
        permission_ceiling=("repo_read", "code_write"),
        capability_permissions={
            "php": {"repo_read", "code_write"},
            "production_merge": {"merge"},
        },
    )
    assert result.granted_capabilities == ("php",)
    assert result.denied_capabilities == ("production_merge",)


def test_harness_missing_required_capability_blocks():
    contract = HarnessCapabilityContract(
        harness="cursor",
        version="1",
        capabilities=("text", "code"),
        limitations=(),
        supports_browser=False,
        supports_tools=True,
        supports_structured_output=True,
    )
    try:
        validate_harness_for_workflow(contract, ("code", "browser"))
    except GovernanceContractError as exc:
        assert "unsupported_harness_capabilities:browser" in str(exc)
        return
    raise AssertionError("missing harness capability must block")


def test_artifact_approval_is_bound_to_inspected_revision():
    review = ArtifactReview(
        artifact_id="SPEC",
        revision=3,
        comments=(ArtifactComment("C-1", "section-2", "clarify"),),
    )
    try:
        review_artifact(
            review,
            decision="APPROVE",
            decided_by="human",
            inspected_revision=2,
        )
    except GovernanceContractError as exc:
        assert "artifact_revision_mismatch" in str(exc)
        return
    raise AssertionError("stale artifact approval must fail")


def test_request_changes_requires_new_revision():
    review = ArtifactReview(artifact_id="PLAN", revision=1, comments=())
    updated = review_artifact(
        review,
        decision="REQUEST_CHANGES",
        decided_by="human",
        inspected_revision=1,
        resulting_revision=2,
    )
    assert updated.resulting_revision == 2


def test_decision_ledger_rejects_supersession_cycle():
    records = (
        DecisionRecord(
            "D1", "topic", "project", "human", (), "A", "why", (), (), ("D2",), "APPROVED"
        ),
        DecisionRecord(
            "D2", "topic2", "project", "human", (), "B", "why", (), (), ("D1",), "APPROVED"
        ),
    )
    try:
        validate_decision_ledger(records)
    except GovernanceContractError as exc:
        assert "decision_supersession_cycle" in str(exc)
        return
    raise AssertionError("decision cycle must fail")


def test_requirement_graph_rejects_dangling_edge():
    nodes = (RequirementNode("REQ-1", "SPEC_REQUIREMENT", "Requirement"),)
    edges = (RequirementEdge("REQ-1", "TASK-404", "IMPLEMENTS"),)
    try:
        validate_requirement_graph(nodes, edges)
    except GovernanceContractError as exc:
        assert "requirement_graph_dangling_edge" in str(exc)
        return
    raise AssertionError("dangling trace must fail")


def test_requirement_graph_computes_connected_impact():
    nodes = (
        RequirementNode("GOAL-1", "BUSINESS_GOAL", "Goal"),
        RequirementNode("REQ-1", "SPEC_REQUIREMENT", "Requirement"),
        RequirementNode("TASK-1", "TASK", "Task"),
        RequirementNode("TEST-1", "TEST", "Test"),
    )
    edges = (
        RequirementEdge("GOAL-1", "REQ-1", "REFINES"),
        RequirementEdge("REQ-1", "TASK-1", "IMPLEMENTS"),
        RequirementEdge("TASK-1", "TEST-1", "VERIFIES"),
    )
    validate_requirement_graph(nodes, edges)
    assert impacted_nodes(("REQ-1",), edges) == ("GOAL-1", "REQ-1", "TASK-1", "TEST-1")
