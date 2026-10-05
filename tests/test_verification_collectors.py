import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from verification.collector_service import CollectorService
from verification.collectors import CollectorResult, VerificationCollectors, VerificationContext


class FakeCollectors(VerificationCollectors):
    def __init__(self, overrides=None):
        self.overrides = overrides or {}

    def _result(self, name):
        value = self.overrides.get(name)
        if isinstance(value, Exception):
            raise value
        if isinstance(value, CollectorResult):
            return value
        return CollectorResult(
            collector=name,
            status="PASS",
            evidence_ref=f"evidence://{name}",
        )

    def collect_ci(self, context):
        return self._result("ci")

    def collect_unit(self, context):
        return self._result("unit")

    def collect_integration(self, context):
        return self._result("integration")

    def collect_e2e(self, context):
        return self._result("e2e")

    def collect_diff(self, context):
        return self._result("diff")

    def collect_backend(self, context):
        return self._result("backend")

    def collect_frontend(self, context):
        return self._result("frontend")

    def collect_database(self, context):
        return self._result("database")


def context():
    return VerificationContext(
        task_id="TASK-1",
        project_id="espacore",
        repository="novo34/example",
        ref="feat/TASK-1",
        staging_url="https://staging.example",
    )


def test_collectors_build_evidence_without_caller_booleans():
    bundle = CollectorService(FakeCollectors()).collect(
        context=context(),
        triggers={"backend", "api"},
        requirement_ids=("REQ-API-001",),
    )

    assert bundle.blocked is False
    assert bundle.evidence.ci_passed is True
    assert bundle.evidence.backend_verified is True
    assert bundle.evidence.frontend_verified is True
    assert bundle.evidence.database_verified is True


def test_collector_exception_becomes_blocked_evidence():
    bundle = CollectorService(
        FakeCollectors({"backend": RuntimeError("API unavailable")})
    ).collect(
        context=context(),
        triggers={"backend", "api"},
        requirement_ids=("REQ-API-001",),
    )

    assert bundle.blocked is True
    assert "backend" in bundle.blocked_collectors
    assert bundle.evidence.backend_verified is False


def test_failed_collector_is_not_converted_to_pass():
    bundle = CollectorService(
        FakeCollectors({
            "integration": CollectorResult("integration", "FAIL", detail="failed")
        })
    ).collect(
        context=context(),
        triggers={"backend"},
        requirement_ids=("REQ-API-001",),
    )

    assert bundle.evidence.integration_passed is False
