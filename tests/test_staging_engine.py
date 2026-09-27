import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from staging.runtime import StagingEnvironment, StagingPolicyError
from staging.service import StagingService


def ready_env():
    return StagingEnvironment(
        project_id="espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        staging_branch="staging",
        url="https://staging.example.test",
        status="READY",
        web_reachable=True,
        backend_reachable=True,
        database_connected=True,
        migration_status="CURRENT",
    )


def test_staging_requires_separate_database():
    env = StagingEnvironment(
        project_id="nuvurent",
        repository="novo34/nuvurent",
        staging_branch="staging",
        url="https://staging.example.test",
        status="READY",
        web_reachable=True,
        backend_reachable=True,
        database_connected=False,
        migration_status="CURRENT",
    )
    result = StagingService().validate_project_staging(env)
    assert result["ready"] is False
    assert "staging_database_not_connected" in result["failures"]


def test_task_can_be_validated_in_permanent_staging():
    service = StagingService()
    promotion = service.create_promotion(
        task_id="TASK-301",
        task_branch="feat/TASK-301",
        staging_branch="staging",
        source_pr=41,
    )
    promotion = service.deployed_to_staging(
        promotion,
        staging_commit="abc123",
    )
    promotion = service.ready_for_human(
        promotion,
        env=ready_env(),
    )
    assert promotion.status == "READY_FOR_HUMAN"


def test_approval_is_task_specific():
    service = StagingService()
    promotion = service.create_promotion(
        task_id="TASK-302",
        task_branch="feat/TASK-302",
        staging_branch="staging",
        source_pr=42,
    )
    promotion = service.deployed_to_staging(promotion, staging_commit="def456")
    promotion = service.ready_for_human(promotion, env=ready_env())
    promotion = service.decide(
        promotion,
        approved=True,
        approval_id="APR-302",
    )
    promotion = service.promoted_to_main(
        promotion,
        production_pr=99,
    )

    assert promotion.task_id == "TASK-302"
    assert promotion.source_pr == 42
    assert promotion.production_pr == 99
    assert promotion.status == "PROMOTED_TO_MAIN"


def test_unapproved_task_cannot_be_promoted_to_main():
    service = StagingService()
    promotion = service.create_promotion(
        task_id="TASK-303",
        task_branch="feat/TASK-303",
        staging_branch="staging",
        source_pr=43,
    )
    try:
        service.promoted_to_main(promotion, production_pr=100)
    except StagingPolicyError:
        return
    raise AssertionError("unapproved task must not reach main")


def test_staging_not_ready_if_web_or_backend_is_unreachable():
    service = StagingService()
    bad = StagingEnvironment(
        project_id="espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        staging_branch="staging",
        url="https://staging.example.test",
        status="READY",
        web_reachable=False,
        backend_reachable=True,
        database_connected=True,
        migration_status="CURRENT",
    )
    result = service.validate_project_staging(bad)
    assert result["ready"] is False
    assert "staging_web_not_reachable" in result["failures"]


def test_pending_migrations_block_human_review():
    service = StagingService()
    bad = StagingEnvironment(
        project_id="espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        staging_branch="staging",
        url="https://staging.example.test",
        status="READY",
        web_reachable=True,
        backend_reachable=True,
        database_connected=True,
        migration_status="PENDING",
    )
    result = service.validate_project_staging(bad)
    assert result["ready"] is False
    assert "staging_migrations_not_current" in result["failures"]
