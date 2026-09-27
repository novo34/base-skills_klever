from __future__ import annotations

from dataclasses import dataclass, field


class ProjectConfigError(ValueError):
    pass


@dataclass(frozen=True)
class ProjectRepository:
    repository_id: str
    full_name: str
    role: str = "other"
    primary: bool = False


@dataclass(frozen=True)
class Project:
    project_id: str
    name: str
    repository: str
    status: str
    production_branch: str
    staging_branch: str
    production_url: str | None = None
    staging_url: str | None = None
    staging_database_enabled: bool = False
    monthly_budget_chf: float | None = None
    allowed_models: tuple[str, ...] = ()
    default_model: str | None = None
    tags: tuple[str, ...] = ()
    repositories: tuple[ProjectRepository, ...] = ()
    metadata: dict = field(default_factory=dict)


def resolved_repositories(project: Project) -> tuple[ProjectRepository, ...]:
    if project.repositories:
        return project.repositories
    return (
        ProjectRepository(
            repository_id="primary",
            full_name=project.repository,
            role="other",
            primary=True,
        ),
    )


def validate_project(project: Project) -> tuple[bool, list[str]]:
    failures: list[str] = []

    if not project.project_id:
        failures.append("project_id_missing")
    if not project.name:
        failures.append("project_name_missing")
    if "/" not in project.repository:
        failures.append("repository_must_be_owner_name")

    repos = resolved_repositories(project)
    seen_ids: set[str] = set()
    seen_names: set[str] = set()
    primary = [repo for repo in repos if repo.primary]

    for repo in repos:
        if not repo.repository_id:
            failures.append("repository_id_missing")
        if repo.repository_id in seen_ids:
            failures.append("duplicate_repository_id")
        seen_ids.add(repo.repository_id)

        if "/" not in repo.full_name:
            failures.append("repository_must_be_owner_name")
        if repo.full_name in seen_names:
            failures.append("duplicate_repository")
        seen_names.add(repo.full_name)

        if repo.role not in {"frontend", "backend", "infra", "other"}:
            failures.append("invalid_repository_role")

    if len(primary) != 1:
        failures.append("exactly_one_primary_repository_required")
    elif primary[0].full_name != project.repository:
        failures.append("primary_repository_must_match_legacy_repository")

    if project.status not in {"ACTIVE", "PAUSED", "ARCHIVED", "SETUP"}:
        failures.append("invalid_project_status")

    if project.production_branch != "main":
        failures.append("production_branch_must_be_main")

    if project.staging_branch == project.production_branch:
        failures.append("staging_branch_must_differ_from_production")

    if project.status == "ACTIVE":
        if not project.staging_url:
            failures.append("active_project_staging_url_missing")
        if not project.staging_database_enabled:
            failures.append("active_project_staging_database_required")

    if project.monthly_budget_chf is not None and project.monthly_budget_chf < 0:
        failures.append("monthly_budget_must_be_non_negative")

    if project.default_model and project.default_model not in project.allowed_models:
        failures.append("default_model_not_allowed")

    return not failures, failures
