import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from notifications.event_router import NotificationEventRouter
from notifications.service import NotificationService
from orchestrator.staging_pipeline import StagingPipeline
from staging.evidence_store import StagingEvidenceStore
from staging.readiness import StagingReadinessEvidence
from staging.runtime import StagingEnvironment, StagingPolicyError


def env():
    return StagingEnvironment(
        project_id="espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        staging_branch="staging",
        url="https://staging.espacore.test",
        status="READY",
        web_reachable=True,
        backend_reachable=True,
        database_connected=True,
        migration_status="CURRENT",
    )


def verified_execution():
    return {
        "task_id": "TASK-500",
        "project_id": "espacore",
        "state": "VERIFIED",
        "branch": "feat/TASK-500",
    }


def evidence(evidence_id="STG-EV-500", revision="abc500"):
    return StagingReadinessEvidence(
        evidence_id=evidence_id,
        project_id="espacore",
        task_id="TASK-500",
        repository_id="web",
        staging_url="https://staging.espacore.test",
        revision=revision,
        collected_at="2026-09-27T12:00:00+02:00",
        deployment_active=True,
        web_reachable=True,
        backend_reachable=True,
        database_connected=True,
        migrations_current=True,
        test_data_ready=True,
        online_e2e_passed=True,
    )


def pipeline_with_evidence(*, revision="abc500", notifications=None):
    store = StagingEvidenceStore()
    store.append(evidence(revision=revision))
    router = (
        NotificationEventRouter(notifications)
        if notifications is not None
        else None
    )
    return StagingPipeline(
        evidence_store=store,
        event_router=router,
    )


def send(pipeline):
    return pipeline.send_verified_task_to_staging(
        execution=verified_execution(),
        source_pr=50,
        source_commit="task500",
        staging_branch="staging",
        staging_commit="abc500",
        environment=env(),
        staging_evidence_id="STG-EV-500",
    )


def test_verified_task_becomes_ready_for_human_online_test():
    result = send(pipeline_with_evidence())
    assert result["promotion"].status == "READY_FOR_HUMAN"
    assert result["approval"].status == "PENDING"
    assert result["approval"].staging_evidence_id == "STG-EV-500"
    assert result["staging_url"] == "https://staging.espacore.test"


def test_missing_staging_evidence_blocks_approval_creation():
    pipeline = StagingPipeline(evidence_store=StagingEvidenceStore())
    try:
        pipeline.send_verified_task_to_staging(
            execution=verified_execution(),
            source_pr=50,
            source_commit="task500",
            staging_branch="staging",
            staging_commit="abc500",
            environment=env(),
            staging_evidence_id="MISSING",
        )
    except KeyError:
        return
    raise AssertionError("missing evidence must block approval")


def test_stale_revision_blocks_approval_creation():
    try:
        send(pipeline_with_evidence(revision="old-revision"))
    except RuntimeError as exc:
        assert "staging_evidence_stale_revision" in str(exc)
        return
    raise AssertionError("stale evidence must block approval")


def test_approval_notification_links_exact_url_and_evidence():
    notifications = NotificationService()
    result = send(pipeline_with_evidence(notifications=notifications))
    approval_items = [
        item
        for item in notifications.list(project_id="espacore")
        if item.category == "APPROVAL_REQUIRED"
    ]
    assert len(approval_items) == 1
    item = approval_items[0]
    assert item.action_url == result["staging_url"]
    assert item.metadata["staging_evidence_id"] == "STG-EV-500"


def test_rejected_human_review_does_not_promote():
    pipeline = pipeline_with_evidence()
    result = send(pipeline)
    decided = pipeline.human_decision(
        promotion=result["promotion"],
        approval=result["approval"],
        decision="REJECTED",
        decided_by="owner",
        decided_at="2026-09-27T18:10:00Z",
        note="Not accepted",
    )
    assert decided["promotion"].status == "REJECTED"
    assert decided["approval"].status == "REJECTED"

    try:
        pipeline.create_production_promotion(
            promotion=decided["promotion"],
            production_pr=150,
            promoted_commit="task500",
        )
    except StagingPolicyError:
        return
    raise AssertionError("rejected task must not promote")


def test_approved_task_gets_task_specific_production_pr():
    pipeline = pipeline_with_evidence()
    result = send(pipeline)
    decided = pipeline.human_decision(
        promotion=result["promotion"],
        approval=result["approval"],
        decision="APPROVED",
        decided_by="owner",
        decided_at="2026-09-27T18:10:00Z",
    )
    promoted = pipeline.create_production_promotion(
        promotion=decided["promotion"],
        production_pr=150,
        promoted_commit="task500",
    )
    assert promoted.status == "PROMOTED_TO_MAIN"
    assert promoted.source_pr == 50
    assert promoted.production_pr == 150
    assert promoted.task_id == "TASK-500"


def test_request_changes_is_distinct_from_rejection():
    pipeline = pipeline_with_evidence()
    result = send(pipeline)
    decided = pipeline.human_decision(
        promotion=result["promotion"],
        approval=result["approval"],
        decision="CHANGES_REQUESTED",
        decided_by="owner",
        decided_at="2026-09-27T18:10:00Z",
        note="Adjust mobile layout",
    )
    assert decided["promotion"].status == "CHANGES_REQUESTED"
    assert decided["approval"].status == "CHANGES_REQUESTED"


def test_human_decision_rejects_approval_for_different_revision():
    pipeline = pipeline_with_evidence()
    result = send(pipeline)
    approval = result["approval"]
    tampered = type(approval)(
        **{**approval.__dict__, "staging_revision": "another-revision"}
    )
    try:
        pipeline.human_decision(
            promotion=result["promotion"],
            approval=tampered,
            decision="APPROVED",
            decided_by="owner",
            decided_at="2026-09-27T18:10:00Z",
        )
    except RuntimeError as exc:
        assert "approval_staging_revision_mismatch" in str(exc)
        return
    raise AssertionError("approval for a different revision must fail")
