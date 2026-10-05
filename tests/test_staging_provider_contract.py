import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from staging.adapter import (
    StagingDeploymentRequest,
    StagingProviderAdapter,
    StagingStepResult,
)
from staging.provider_policy import StagingProviderPolicyError, StagingReferencePolicy
from staging.provider_service import StagingProviderService


class FakeStagingAdapter(StagingProviderAdapter):
    def __init__(self, fail_step=None):
        self.fail_step = fail_step
        self.calls = []

    def _result(self, name):
        self.calls.append(name)
        return StagingStepResult(ok=name != self.fail_step, detail=name)

    def deploy(self, request):
        return self._result("deploy")

    def verify_database(self, request):
        return self._result("database")

    def apply_migrations(self, request):
        return self._result("migrations")

    def seed_test_data(self, request):
        return self._result("seed")

    def health_check(self, request):
        return self._result("health")

    def run_online_e2e(self, request):
        return self._result("e2e")


def policy():
    return StagingReferencePolicy(
        database_refs=frozenset({"secret://espacore/staging-db"}),
        secret_refs=frozenset({"secret://espacore/staging-app"}),
    )


def service(adapter):
    return StagingProviderService(adapter, reference_policy=policy())


def request(**overrides):
    data = dict(
        project_id="espacore",
        task_id="TASK-1",
        repository_id="web",
        repository="novo34/rediseno-web-espacore-gmbh",
        source_branch="feat/TASK-1",
        staging_branch="staging",
        staging_url="https://staging.example",
        database_ref="secret://espacore/staging-db",
        environment_kind="PERMANENT_STAGING",
        secret_refs=("secret://espacore/staging-app",),
    )
    data.update(overrides)
    return StagingDeploymentRequest(**data)


def test_permanent_staging_runs_all_provider_steps():
    adapter = FakeStagingAdapter()
    result = service(adapter).prepare(request())
    assert result["ready"] is True
    assert adapter.calls == [
        "deploy",
        "database",
        "migrations",
        "seed",
        "health",
        "e2e",
    ]


def test_failed_staging_step_stops_pipeline():
    adapter = FakeStagingAdapter(fail_step="migrations")
    result = service(adapter).prepare(request())
    assert result["ready"] is False
    assert result["failed_step"] == "migrations"
    assert adapter.calls == ["deploy", "database", "migrations"]


def test_production_database_reference_is_forbidden():
    try:
        service(FakeStagingAdapter()).prepare(
            request(database_ref="secret://espacore/production-db")
        )
    except StagingProviderPolicyError as exc:
        assert "staging_database_reference_not_allowed" in str(exc)
        return
    raise AssertionError("production DB reference must never enter staging")


def test_production_secret_reference_is_forbidden():
    try:
        service(FakeStagingAdapter()).prepare(
            request(secret_refs=("secret://espacore/production-api",))
        )
    except StagingProviderPolicyError as exc:
        assert "staging_secret_reference_not_allowed" in str(exc)
        return
    raise AssertionError("production secret must never enter staging")


def test_staging_is_distinct_from_ephemeral_workspace():
    try:
        service(FakeStagingAdapter()).prepare(
            request(environment_kind="EPHEMERAL_WORKSPACE")
        )
    except StagingProviderPolicyError as exc:
        assert "environment_must_be_permanent_staging" in str(exc)
        return
    raise AssertionError("workspace must not be treated as permanent staging")


def test_opaque_live_database_reference_is_rejected_when_not_allowlisted():
    try:
        service(FakeStagingAdapter()).prepare(
            request(database_ref="vault://finance/main")
        )
    except StagingProviderPolicyError as exc:
        assert "staging_database_reference_not_allowed" in str(exc)
        return
    raise AssertionError("non-allowlisted database reference must be rejected")
