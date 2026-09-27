import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.handoff import AgentHandoff
from agents_runtime.integrator import IntegratorAgent
from agents_runtime.multiagent import AgentAssignment, MultiAgentCoordinator


def developer_handoff():
    return AgentHandoff(
        handoff_id="HO-DEV",
        task_id="TASK-1",
        from_agent="developer",
        to_agent="integrator",
        status="COMPLETED",
        summary="Implementation complete",
        artifacts=("PR-1",),
    )


def verifier_handoff():
    return AgentHandoff(
        handoff_id="HO-VER",
        task_id="TASK-1",
        from_agent="verifier",
        to_agent="integrator",
        status="COMPLETED",
        summary="Verification complete",
        artifacts=("VER-1",),
    )


def test_integrator_requires_human_approval_after_verification():
    result = IntegratorAgent().evaluate(
        developer_handoff=developer_handoff(),
        verifier_handoff=verifier_handoff(),
        verification_status="VERIFIED",
        human_approved=False,
    )
    assert result.status == "AWAITING_HUMAN"


def test_integrator_allows_merge_only_after_all_gates():
    result = IntegratorAgent().evaluate(
        developer_handoff=developer_handoff(),
        verifier_handoff=verifier_handoff(),
        verification_status="VERIFIED",
        human_approved=True,
    )
    assert result.status == "READY_TO_MERGE"


def test_multiagent_blocks_resource_lock_conflict():
    coordinator = MultiAgentCoordinator()
    coordinator.assign(AgentAssignment(
        task_id="TASK-10",
        agent_role="frontend",
        resource_locks=("app/contact/page.tsx",),
        status="RUNNING",
    ))

    try:
        coordinator.assign(AgentAssignment(
            task_id="TASK-10",
            agent_role="ux",
            resource_locks=("app/contact/page.tsx",),
            status="PENDING",
        ))
    except ValueError as exc:
        assert "resource_lock_conflict" in str(exc)
        return

    raise AssertionError("parallel agents must not share writable lock")
