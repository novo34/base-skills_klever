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
    append_decision_record,
    compose_capabilities,
    documentation_impact_from_graph,
    evaluate_harness_for_workflow,
    impacted_nodes,
    requirement_quality_snapshot,
    review_artifact,
    scoped_decisions,
    validate_decision_ledger,
    validate_harness_for_workflow,
    validate_requirement_graph,
    validate_requirement_trace_completeness,
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


def full_requirement_graph():
    nodes = (
        RequirementNode("GOAL-1", "BUSINESS_GOAL", "Goal"),
        RequirementNode("CAP-1", "PRD_CAPABILITY", "Capability"),
        RequirementNode("REQ-1", "SPEC_REQUIREMENT", "Requirement"),
        RequirementNode("ADR-1", "ADR", "Decision"),
        RequirementNode("PHASE-1", "ROADMAP_PHASE", "Phase"),
        RequirementNode("TASK-1", "TASK", "Task"),
        RequirementNode("CODE-1", "CODE", "Code"),
        RequirementNode("TEST-1", "TEST", "Test"),
        RequirementNode("EVID-1", "EVIDENCE", "Evidence"),
        RequirementNode("REL-1", "RELEASE", "Release"),
    )
    edges = (
        RequirementEdge("GOAL-1", "CAP-1", "REFINES"),
        RequirementEdge("CAP-1", "REQ-1", "REFINES"),
        RequirementEdge("REQ-1", "ADR-1", "DECIDES"),
        RequirementEdge("REQ-1", "PHASE-1", "PLANS"),
        RequirementEdge("REQ-1", "TASK-1", "IMPLEMENTS"),
        RequirementEdge("TASK-1", "CODE-1", "IMPLEMENTS"),
        RequirementEdge("CODE-1", "TEST-1", "VERIFIES"),
        RequirementEdge("TEST-1", "EVID-1", "EVIDENCES"),
        RequirementEdge("EVID-1", "REL-1", "RELEASES"),
    )
    return nodes, edges


def test_requirement_trace_completeness_accepts_end_to_end_chain():
    nodes, edges = full_requirement_graph()
    validate_requirement_trace_completeness(nodes, edges, require_release=True)


def test_requirement_trace_completeness_detects_missing_test_evidence():
    nodes, edges = full_requirement_graph()
    broken = tuple(
        edge for edge in edges
        if not (edge.from_id == "CODE-1" and edge.to_id == "TEST-1")
    )
    try:
        validate_requirement_trace_completeness(nodes, broken, require_release=True)
    except GovernanceContractError as exc:
        assert "requirement_trace_missing_downstream" in str(exc)
        return
    raise AssertionError("missing trace link must fail")


def test_documentation_impact_derives_canonical_surfaces():
    nodes, edges = full_requirement_graph()
    impact = documentation_impact_from_graph(("REQ-1",), nodes, edges)
    assert "PRD" in impact
    assert "SPEC" in impact
    assert "ROADMAP" in impact
    assert "BACKLOG" in impact
    assert "TESTS" in impact


def test_quality_snapshot_consumes_requirement_graph():
    nodes, edges = full_requirement_graph()
    snapshot = requirement_quality_snapshot("REQ-1", nodes, edges)
    assert snapshot["has_task"] is True
    assert snapshot["has_code"] is True
    assert snapshot["has_test"] is True
    assert snapshot["has_evidence"] is True
    assert snapshot["has_release"] is True


def test_harness_evaluation_returns_typed_blocking_result():
    contract = HarnessCapabilityContract(
        harness="cursor",
        version="1",
        capabilities=("text", "code"),
        limitations=(),
        supports_browser=False,
        supports_tools=False,
        supports_structured_output=False,
    )
    result = evaluate_harness_for_workflow(contract, ("code", "browser"))
    assert result.status == "BLOCKED"
    assert result.missing_capabilities == ("browser",)
    assert result.reason == "unsupported_harness_capabilities"


def test_decision_ledger_is_append_only_by_id():
    original = DecisionRecord(
        "D1", "auth", "project-a", "human", ("A", "B"), "A", "why", ("E1",), ("SPEC",), (), "APPROVED"
    )
    try:
        append_decision_record((original,), original)
    except GovernanceContractError as exc:
        assert "decision_record_immutable_duplicate_id" in str(exc)
        return
    raise AssertionError("decision history must be append-only")


def test_decision_retrieval_is_scoped():
    records = (
        DecisionRecord("D1", "auth", "project-a", "human", (), "A", "why", (), (), (), "APPROVED"),
        DecisionRecord("D2", "ui", "project-b", "human", (), "B", "why", (), (), (), "APPROVED"),
    )
    selected = scoped_decisions(records, scope="project-a")
    assert tuple(record.decision_id for record in selected) == ("D1",)
