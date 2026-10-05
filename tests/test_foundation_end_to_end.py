import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "orchestrator"))

from orchestrator.staging_pipeline import StagingPipeline
from orchestrator.task_orchestrator import advance, create_task_execution
from staging.evidence_store import StagingEvidenceStore
from staging.readiness import StagingReadinessEvidence
from staging.runtime import StagingEnvironment


def test_foundation_verified_to_production_done_circuit():
    task = create_task_execution(
        "TASK-E2E-1",
        {"backend", "api", "implementation"},
        set(),
        project_id="espacore",
    )
    task["branch"] = "feat/TASK-E2E-1"

    task = advance(task, "READY")
    task = advance(task, "RUNNING")
    task = advance(task, "VERIFYING")
    task = advance(task, "VERIFIED", verification_passed=True)

    evidence = StagingReadinessEvidence(
        evidence_id="STG-E2E-1",
        project_id="espacore",
        task_id="TASK-E2E-1",
        repository_id="web",
        staging_url="https://staging.example",
        revision="staging-rev-1",
        collected_at="2026-09-27T16:00:00+02:00",
        deployment_active=True,
        web_reachable=True,
        backend_reachable=True,
        database_connected=True,
        migrations_current=True,
        test_data_ready=True,
        online_e2e_passed=True,
    )
    store = StagingEvidenceStore()
    store.append(evidence)

    environment = StagingEnvironment(
        project_id="espacore",
        repository="novo34/espacore",
        staging_branch="staging",
        url="https://staging.example",
        status="READY",
        web_reachable=True,
        backend_reachable=True,
        database_connected=True,
        migration_status="CURRENT",
    )

    staging = StagingPipeline(evidence_store=store)
    review = staging.send_verified_task_to_staging(
        execution=task,
        source_pr=101,
        source_commit="task-commit-1",
        staging_branch="staging",
        staging_commit="staging-rev-1",
        environment=environment,
        staging_evidence_id="STG-E2E-1",
    )

    task = advance(task, "STAGING")
    task = advance(task, "AWAITING_HUMAN", staging_ready=True)

    decision = staging.human_decision(
        promotion=review["promotion"],
        approval=review["approval"],
        decision="APPROVED",
        decided_by="owner",
        decided_at="2026-09-27T18:10:00Z",
    )
    task = advance(task, "APPROVED", human_approved=True)

    promoted = staging.create_production_promotion(
        promotion=decision["promotion"],
        production_pr=201,
        promoted_commit="task-commit-1",
    )

    task = advance(task, "DONE", production_promotion=promoted)

    assert promoted.status == "PROMOTED_TO_MAIN"
    assert promoted.task_id == "TASK-E2E-1"
    assert task["state"] == "DONE"
