import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from staging.adapter import StagingStepResult
from staging.evidence_store import StagingEvidenceStore
from staging.readiness import (
    StagingReadinessRequirements,
    evaluate_readiness,
)
from staging.readiness_builder import build_readiness_evidence


def provider_result(**overrides):
    steps = {
        "deploy": StagingStepResult(ok=True),
        "database": StagingStepResult(ok=True),
        "migrations": StagingStepResult(ok=True),
        "seed": StagingStepResult(ok=True),
        "health": StagingStepResult(
            ok=True,
            metadata={
                "web_reachable": True,
                "backend_reachable": True,
            },
        ),
        "e2e": StagingStepResult(ok=True),
    }
    steps.update(overrides)
    return {"ready": True, "steps": steps}


def evidence(result=None):
    return build_readiness_evidence(
        evidence_id="STG-EV-1",
        project_id="espacore",
        task_id="TASK-1",
        repository_id="web",
        staging_url="https://staging.example",
        revision="abc123",
        collected_at="2026-09-27T12:00:00+02:00",
        provider_result=result or provider_result(),
    )


def test_complete_staging_evidence_is_ready_for_human():
    result = evaluate_readiness(evidence())
    assert result.ready is True
    assert result.failures == ()


def test_missing_backend_health_blocks_readiness():
    bad = provider_result(
        health=StagingStepResult(
            ok=True,
            metadata={
                "web_reachable": True,
                "backend_reachable": False,
            },
        )
    )
    result = evaluate_readiness(evidence(bad))
    assert result.ready is False
    assert "backend_not_reachable" in result.failures


def test_requirements_can_exempt_non_applicable_backend():
    bad = provider_result(
        health=StagingStepResult(
            ok=True,
            metadata={
                "web_reachable": True,
                "backend_reachable": False,
            },
        )
    )
    result = evaluate_readiness(
        evidence(bad),
        StagingReadinessRequirements(require_backend=False),
    )
    assert result.ready is True


def test_staging_evidence_is_append_only_and_traceable_by_task():
    store = StagingEvidenceStore()
    item = store.append(evidence())
    assert store.get(item.evidence_id) == item
    assert store.latest_for_task("TASK-1") == item

    try:
        store.delete(item.evidence_id)
    except PermissionError as exc:
        assert "staging_evidence_is_immutable" in str(exc)
        return
    raise AssertionError("staging evidence must be immutable")
