from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


class GovernanceContractError(ValueError):
    pass


@dataclass(frozen=True)
class CapabilityComposition:
    task_id: str
    role: str
    requested_capabilities: tuple[str, ...]
    granted_capabilities: tuple[str, ...]
    denied_capabilities: tuple[str, ...]
    permission_ceiling: tuple[str, ...]
    rationale: tuple[str, ...]


@dataclass(frozen=True)
class HarnessCapabilityResult:
    status: str
    missing_capabilities: tuple[str, ...] = ()
    reason: str | None = None


@dataclass(frozen=True)
class HarnessCapabilityContract:
    harness: str
    version: str
    capabilities: tuple[str, ...]
    limitations: tuple[str, ...]
    supports_browser: bool
    supports_tools: bool
    supports_structured_output: bool


@dataclass(frozen=True)
class ArtifactComment:
    comment_id: str
    selector: str
    text: str
    status: str = "OPEN"


@dataclass(frozen=True)
class ArtifactReview:
    artifact_id: str
    revision: int
    comments: tuple[ArtifactComment, ...]
    decision: str = "PENDING"
    decided_by: str | None = None
    resulting_revision: int | None = None


@dataclass(frozen=True)
class DecisionRecord:
    decision_id: str
    topic: str
    scope: str
    actor: str
    alternatives: tuple[str, ...]
    selected: str
    rationale: str
    evidence: tuple[str, ...]
    affected_artifacts: tuple[str, ...]
    supersedes: tuple[str, ...]
    status: str


@dataclass(frozen=True)
class RequirementNode:
    id: str
    type: str
    label: str


@dataclass(frozen=True)
class RequirementEdge:
    from_id: str
    to_id: str
    relation: str


def compose_capabilities(
    *,
    task_id: str,
    role: str,
    requested_capabilities: Iterable[str],
    available_capabilities: Iterable[str],
    permission_ceiling: Iterable[str],
    capability_permissions: dict[str, set[str]] | None = None,
) -> CapabilityComposition:
    requested = tuple(sorted(set(requested_capabilities)))
    available = set(available_capabilities)
    ceiling = tuple(sorted(set(permission_ceiling)))
    ceiling_set = set(ceiling)
    cap_perms = capability_permissions or {}

    granted: list[str] = []
    denied: list[str] = []
    rationale: list[str] = []

    for capability in requested:
        if capability not in available:
            denied.append(capability)
            rationale.append(f"{capability}:unavailable")
            continue
        required_permissions = cap_perms.get(capability, set())
        if not required_permissions.issubset(ceiling_set):
            denied.append(capability)
            rationale.append(f"{capability}:permission_ceiling")
            continue
        granted.append(capability)

    return CapabilityComposition(
        task_id=task_id,
        role=role,
        requested_capabilities=requested,
        granted_capabilities=tuple(granted),
        denied_capabilities=tuple(denied),
        permission_ceiling=ceiling,
        rationale=tuple(rationale),
    )


def evaluate_harness_for_workflow(
    contract: HarnessCapabilityContract,
    required_capabilities: Iterable[str],
) -> HarnessCapabilityResult:
    missing = tuple(sorted(set(required_capabilities) - set(contract.capabilities)))
    if missing:
        return HarnessCapabilityResult(
            status="BLOCKED",
            missing_capabilities=missing,
            reason="unsupported_harness_capabilities",
        )
    return HarnessCapabilityResult(status="SUPPORTED")


def validate_harness_for_workflow(
    contract: HarnessCapabilityContract,
    required_capabilities: Iterable[str],
) -> None:
    result = evaluate_harness_for_workflow(contract, required_capabilities)
    if result.status != "SUPPORTED":
        raise GovernanceContractError(
            f"{result.reason}:" + ",".join(result.missing_capabilities)
        )


def review_artifact(
    review: ArtifactReview,
    *,
    decision: str,
    decided_by: str,
    inspected_revision: int,
    resulting_revision: int | None = None,
) -> ArtifactReview:
    allowed = {"APPROVE", "REQUEST_CHANGES", "REJECT"}
    if decision not in allowed:
        raise GovernanceContractError("invalid_artifact_review_decision")
    if inspected_revision != review.revision:
        raise GovernanceContractError("artifact_revision_mismatch")
    if not decided_by:
        raise GovernanceContractError("artifact_reviewer_required")
    if decision == "REQUEST_CHANGES":
        if resulting_revision is None or resulting_revision <= review.revision:
            raise GovernanceContractError("new_artifact_revision_required")
    elif resulting_revision is not None and resulting_revision != review.revision:
        raise GovernanceContractError("unexpected_artifact_revision")

    return ArtifactReview(
        artifact_id=review.artifact_id,
        revision=review.revision,
        comments=review.comments,
        decision=decision,
        decided_by=decided_by,
        resulting_revision=resulting_revision,
    )


def validate_decision_ledger(records: Iterable[DecisionRecord]) -> None:
    records = tuple(records)
    by_id = {record.decision_id: record for record in records}
    if len(by_id) != len(records):
        raise GovernanceContractError("duplicate_decision_id")

    for record in records:
        if not record.decision_id or not record.topic or not record.actor:
            raise GovernanceContractError("decision_identity_required")
        if record.status not in {
            "PROPOSED", "APPROVED", "REJECTED", "LOCKED", "SUPERSEDED"
        }:
            raise GovernanceContractError("invalid_decision_status")
        for predecessor in record.supersedes:
            if predecessor not in by_id:
                raise GovernanceContractError(
                    f"unknown_superseded_decision:{record.decision_id}:{predecessor}"
                )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(decision_id: str, path: tuple[str, ...]) -> None:
        if decision_id in visited:
            return
        if decision_id in visiting:
            raise GovernanceContractError(
                "decision_supersession_cycle:" + "->".join(path + (decision_id,))
            )
        visiting.add(decision_id)
        for predecessor in by_id[decision_id].supersedes:
            visit(predecessor, path + (decision_id,))
        visiting.remove(decision_id)
        visited.add(decision_id)

    for decision_id in sorted(by_id):
        visit(decision_id, ())


REQUIREMENT_NODE_TYPES = {
    "BUSINESS_GOAL", "PRD_CAPABILITY", "SPEC_REQUIREMENT", "ADR",
    "ROADMAP_PHASE", "TASK", "CODE", "TEST", "EVIDENCE", "RELEASE",
}
REQUIREMENT_RELATIONS = {
    "IMPLEMENTS", "REFINES", "DECIDES", "PLANS",
    "VERIFIES", "EVIDENCES", "RELEASES", "DEPENDS_ON",
}


def validate_requirement_graph(
    nodes: Iterable[RequirementNode],
    edges: Iterable[RequirementEdge],
) -> None:
    nodes = tuple(nodes)
    edges = tuple(edges)
    by_id = {node.id: node for node in nodes}
    if len(by_id) != len(nodes):
        raise GovernanceContractError("duplicate_requirement_graph_node")
    for node in nodes:
        if node.type not in REQUIREMENT_NODE_TYPES:
            raise GovernanceContractError(f"invalid_requirement_node_type:{node.type}")
    for edge in edges:
        if edge.from_id not in by_id or edge.to_id not in by_id:
            raise GovernanceContractError("requirement_graph_dangling_edge")
        if edge.relation not in REQUIREMENT_RELATIONS:
            raise GovernanceContractError(
                f"invalid_requirement_relation:{edge.relation}"
            )


def impacted_nodes(
    changed_node_ids: Iterable[str],
    edges: Iterable[RequirementEdge],
) -> tuple[str, ...]:
    changed = set(changed_node_ids)
    reverse: dict[str, set[str]] = {}
    forward: dict[str, set[str]] = {}
    for edge in edges:
        forward.setdefault(edge.from_id, set()).add(edge.to_id)
        reverse.setdefault(edge.to_id, set()).add(edge.from_id)

    impacted = set(changed)
    frontier = list(changed)
    while frontier:
        current = frontier.pop()
        for neighbor in forward.get(current, set()) | reverse.get(current, set()):
            if neighbor not in impacted:
                impacted.add(neighbor)
                frontier.append(neighbor)
    return tuple(sorted(impacted))


def validate_requirement_trace_completeness(
    nodes: Iterable[RequirementNode],
    edges: Iterable[RequirementEdge],
    *,
    require_release: bool = False,
) -> None:
    nodes = tuple(nodes)
    edges = tuple(edges)
    validate_requirement_graph(nodes, edges)
    by_id = {node.id: node for node in nodes}
    forward: dict[str, set[str]] = {}
    reverse: dict[str, set[str]] = {}
    for edge in edges:
        forward.setdefault(edge.from_id, set()).add(edge.to_id)
        reverse.setdefault(edge.to_id, set()).add(edge.from_id)

    def reachable(start: str, graph: dict[str, set[str]]) -> set[str]:
        seen: set[str] = set()
        stack = [start]
        while stack:
            current = stack.pop()
            for nxt in graph.get(current, set()):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    required_downstream = {"TASK", "CODE", "TEST", "EVIDENCE"}
    if require_release:
        required_downstream.add("RELEASE")

    for node in nodes:
        if node.type != "SPEC_REQUIREMENT":
            continue
        upstream_types = {by_id[item].type for item in reachable(node.id, reverse)}
        downstream_types = {by_id[item].type for item in reachable(node.id, forward)}

        if "PRD_CAPABILITY" not in upstream_types:
            raise GovernanceContractError(
                f"requirement_trace_missing_prd_capability:{node.id}"
            )
        if "BUSINESS_GOAL" not in upstream_types:
            raise GovernanceContractError(
                f"requirement_trace_missing_business_goal:{node.id}"
            )

        missing = required_downstream - downstream_types
        if missing:
            raise GovernanceContractError(
                f"requirement_trace_missing_downstream:{node.id}:"
                + ",".join(sorted(missing))
            )


def documentation_impact_from_graph(
    changed_node_ids: Iterable[str],
    nodes: Iterable[RequirementNode],
    edges: Iterable[RequirementEdge],
) -> tuple[str, ...]:
    nodes = tuple(nodes)
    by_id = {node.id: node for node in nodes}
    impacted = impacted_nodes(changed_node_ids, edges)

    artifact_for_type = {
        "BUSINESS_GOAL": "PRD",
        "PRD_CAPABILITY": "PRD",
        "SPEC_REQUIREMENT": "SPEC",
        "ADR": "ADR",
        "ROADMAP_PHASE": "ROADMAP",
        "TASK": "BACKLOG",
        "CODE": "IMPLEMENTATION",
        "TEST": "TESTS",
        "EVIDENCE": "EVIDENCE",
        "RELEASE": "RELEASE",
    }
    artifacts = {
        artifact_for_type[by_id[node_id].type]
        for node_id in impacted
        if node_id in by_id
    }
    return tuple(sorted(artifacts))


def requirement_quality_snapshot(
    requirement_id: str,
    nodes: Iterable[RequirementNode],
    edges: Iterable[RequirementEdge],
) -> dict:
    nodes = tuple(nodes)
    by_id = {node.id: node for node in nodes}
    if requirement_id not in by_id:
        raise GovernanceContractError("requirement_not_found")
    if by_id[requirement_id].type != "SPEC_REQUIREMENT":
        raise GovernanceContractError("quality_snapshot_requires_spec_requirement")

    connected = impacted_nodes((requirement_id,), edges)
    connected_types = {
        by_id[node_id].type for node_id in connected if node_id in by_id
    }
    return {
        "requirement_id": requirement_id,
        "has_task": "TASK" in connected_types,
        "has_code": "CODE" in connected_types,
        "has_test": "TEST" in connected_types,
        "has_evidence": "EVIDENCE" in connected_types,
        "has_release": "RELEASE" in connected_types,
    }


def append_decision_record(
    existing: Iterable[DecisionRecord],
    new_record: DecisionRecord,
) -> tuple[DecisionRecord, ...]:
    existing = tuple(existing)
    if any(record.decision_id == new_record.decision_id for record in existing):
        raise GovernanceContractError("decision_record_immutable_duplicate_id")
    combined = existing + (new_record,)
    validate_decision_ledger(combined)
    return combined


def scoped_decisions(
    records: Iterable[DecisionRecord],
    *,
    scope: str,
    topics: Iterable[str] = (),
) -> tuple[DecisionRecord, ...]:
    topic_set = set(topics)
    return tuple(
        record
        for record in records
        if record.scope == scope and (not topic_set or record.topic in topic_set)
    )
