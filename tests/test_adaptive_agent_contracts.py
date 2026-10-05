import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.handoff import AgentHandoff
from agents_runtime.integrator import IntegratorAgent
from agents_runtime.verifier import AdaptiveVerificationEvidence, VerifierAgent
from scripts.classify_risk import classify
from scripts.plan_task import resolve_skills


def developer_handoff():
    return AgentHandoff(
        handoff_id="DEV",
        task_id="TASK-1",
        from_agent="developer",
        to_agent="integrator",
        status="COMPLETED",
        summary="done",
    )


def verifier_handoff():
    return AgentHandoff(
        handoff_id="VER",
        task_id="TASK-1",
        from_agent="verifier",
        to_agent="integrator",
        status="COMPLETED",
        summary="verified",
    )


def test_integrator_blocks_unapproved_blueprint_revision():
    result = IntegratorAgent().evaluate_adaptive(
        developer_handoff=developer_handoff(),
        verifier_handoff=verifier_handoff(),
        verification_status="VERIFIED",
        human_approved=True,
        approved_blueprint_revision=2,
        delivered_blueprint_revision=3,
        approved_promotion_scope=("PR-1",),
        requested_promotion_scope=("PR-1",),
    )
    assert result.status == "BLOCKED"
    assert result.reason == "blueprint_revision_mismatch"


def test_integrator_blocks_scope_larger_than_approval():
    result = IntegratorAgent().evaluate_adaptive(
        developer_handoff=developer_handoff(),
        verifier_handoff=verifier_handoff(),
        verification_status="VERIFIED",
        human_approved=True,
        approved_blueprint_revision=2,
        delivered_blueprint_revision=2,
        approved_promotion_scope=("PR-1",),
        requested_promotion_scope=("PR-1", "PR-2"),
    )
    assert result.status == "BLOCKED"
    assert result.reason == "promotion_scope_not_approved"


def test_verifier_requires_all_adaptive_evidence():
    ok, failures = VerifierAgent.validate_adaptive_evidence(
        AdaptiveVerificationEvidence(
            hygiene_status="VERIFIED",
            adversarial_status="FAILED",
            runtime_status="VERIFIED",
            trace_status="VERIFIED",
        )
    )
    assert ok is False
    assert "adversarial_status:FAILED" in failures


def test_self_improvement_is_always_r4():
    assert classify({"self_improvement"}) == "R4"


def test_uncertain_deletion_is_at_least_r3():
    assert classify({"uncertain_code_deletion"}) == "R3"


def test_plan_mutation_is_at_least_r2():
    assert classify({"plan_mutation"}) == "R2"


def test_resolver_selects_adaptive_capabilities():
    selected = {
        item["id"]
        for item in resolve_skills(
            {"implementation", "planning", "verification", "cleanup"}
        )
    }
    assert "22-intent-discovery-and-refinement" in selected
    assert "24-planning-task-breakdown" in selected
    assert "47-adaptive-workflow-compilation" in selected
    assert "91-repository-hygiene-and-dead-code" in selected
    assert "92-duplication-and-reuse-guard" in selected
