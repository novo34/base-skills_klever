from __future__ import annotations

from staging.readiness import StagingReadinessEvidence


def build_readiness_evidence(
    *,
    evidence_id: str,
    project_id: str,
    task_id: str,
    repository_id: str,
    staging_url: str,
    revision: str,
    collected_at: str,
    provider_result: dict,
) -> StagingReadinessEvidence:
    steps = provider_result.get("steps") or {}

    deploy = steps.get("deploy")
    database = steps.get("database")
    migrations = steps.get("migrations")
    seed = steps.get("seed")
    health = steps.get("health")
    e2e = steps.get("e2e")

    health_metadata = getattr(health, "metadata", {}) if health is not None else {}

    return StagingReadinessEvidence(
        evidence_id=evidence_id,
        project_id=project_id,
        task_id=task_id,
        repository_id=repository_id,
        staging_url=staging_url,
        revision=revision,
        collected_at=collected_at,
        deployment_active=bool(deploy and deploy.ok),
        web_reachable=bool(
            health and health.ok and health_metadata.get("web_reachable", False)
        ),
        backend_reachable=bool(
            health and health.ok and health_metadata.get("backend_reachable", False)
        ),
        database_connected=bool(database and database.ok),
        migrations_current=bool(migrations and migrations.ok),
        test_data_ready=bool(seed and seed.ok),
        online_e2e_passed=bool(e2e and e2e.ok),
    )
