import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestrator.staging_pipeline import StagingPipeline
from staging.runtime import StagingEnvironment, StagingPolicyError


def env():
    return StagingEnvironment(
        project_id="espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        staging_branch="staging",
        url="https://staging.espacore.test",
        status="READY",
        database_connected=True,
        migration_status="CURRENT",
    )


def verified_execution():
    return {
        "task_id": "TASK-500",
        "state": "VERIFIED",
        "branch": "feat/TASK-500",
    }


def test_verified_task_becomes_ready_for_human_online_test():
    result = StagingPipeline().send_verified_task_to_staging(
        execution=verified_execution(),
        source_pr=50,
        staging_branch="staging",
        staging_commit="abc500",
        environment=env(),
    )

    assert result["promotion"].status == "READY_FOR_HUMAN"
    assert result["approval"].status == "PENDING"
    assert result["staging_url"] == "https://staging.espacore.test"


def test_rejected_human_review_does_not_promote():
    pipeline = StagingPipeline()
    result = pipeline.send_verified_task_to_staging(
        execution=verified_execution(),
        source_pr=50,
        staging_branch="staging",
        staging_commit="abc500",
        environment=env(),
    )
    decided = pipeline.human_decision(
        promotion=result["promotion"],
        approval=result["approval"],
        approved=False,
        decided_by="owner",
        note="UI needs changes",
    )

    assert decided["promotion"].status == "REJECTED"
    assert decided["approval"].status == "REJECTED"

    try:
        pipeline.create_production_promotion(
            promotion=decided["promotion"],
            production_pr=150,
        )
    except StagingPolicyError:
        return
    raise AssertionError("rejected task must not promote")


def test_approved_task_gets_task_specific_production_pr():
    pipeline = StagingPipeline()
    result = pipeline.send_verified_task_to_staging(
        execution=verified_execution(),
        source_pr=50,
        staging_branch="staging",
        staging_commit="abc500",
        environment=env(),
    )
    decided = pipeline.human_decision(
        promotion=result["promotion"],
        approval=result["approval"],
        approved=True,
        decided_by="owner",
    )
    promoted = pipeline.create_production_promotion(
        promotion=decided["promotion"],
        production_pr=150,
    )

    assert promoted.status == "PROMOTED_TO_MAIN"
    assert promoted.source_pr == 50
    assert promoted.production_pr == 150
    assert promoted.task_id == "TASK-500"
