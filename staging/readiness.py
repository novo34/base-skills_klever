from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StagingReadinessRequirements:
    require_web: bool = True
    require_backend: bool = True
    require_database: bool = True
    require_migrations: bool = True
    require_test_data: bool = True
    require_online_e2e: bool = True


@dataclass(frozen=True)
class StagingReadinessEvidence:
    evidence_id: str
    project_id: str
    task_id: str
    repository_id: str
    staging_url: str
    revision: str
    collected_at: str
    deployment_active: bool
    web_reachable: bool
    backend_reachable: bool
    database_connected: bool
    migrations_current: bool
    test_data_ready: bool
    online_e2e_passed: bool


@dataclass(frozen=True)
class StagingReadinessResult:
    ready: bool
    failures: tuple[str, ...]
    evidence: StagingReadinessEvidence


def evaluate_readiness(
    evidence: StagingReadinessEvidence,
    requirements: StagingReadinessRequirements | None = None,
) -> StagingReadinessResult:
    requirements = requirements or StagingReadinessRequirements()
    failures: list[str] = []

    if not evidence.deployment_active:
        failures.append("deployment_not_active")
    if requirements.require_web and not evidence.web_reachable:
        failures.append("web_not_reachable")
    if requirements.require_backend and not evidence.backend_reachable:
        failures.append("backend_not_reachable")
    if requirements.require_database and not evidence.database_connected:
        failures.append("database_not_connected")
    if requirements.require_migrations and not evidence.migrations_current:
        failures.append("migrations_not_current")
    if requirements.require_test_data and not evidence.test_data_ready:
        failures.append("test_data_not_ready")
    if requirements.require_online_e2e and not evidence.online_e2e_passed:
        failures.append("online_e2e_not_passed")

    return StagingReadinessResult(
        ready=not failures,
        failures=tuple(failures),
        evidence=evidence,
    )
