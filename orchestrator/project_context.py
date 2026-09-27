from __future__ import annotations

from dataclasses import dataclass

from projects.runtime import ProjectRepository, resolved_repositories
from projects.service import ProjectService


@dataclass(frozen=True)
class ProjectContext:
    project_id: str
    name: str
    repository: str
    repositories: tuple[ProjectRepository, ...]
    production_branch: str
    staging_branch: str
    production_url: str | None
    staging_url: str | None
    staging_database_enabled: bool
    monthly_budget_chf: float | None
    allowed_models: tuple[str, ...]
    default_model: str | None

    def resolve_repository(self, target: str | None = None) -> ProjectRepository:
        repos = self.repositories

        if target is None:
            if len(repos) != 1:
                raise ValueError("target_repository_required")
            return repos[0]

        matches = [
            repo for repo in repos
            if repo.repository_id == target or repo.full_name == target
        ]
        if len(matches) != 1:
            raise ValueError("target_repository_not_found")
        return matches[0]


class ProjectContextResolver:
    def __init__(self, projects: ProjectService):
        self.projects = projects

    def resolve(self, project_id: str) -> ProjectContext:
        project = self.projects.get(project_id)
        if project.status != "ACTIVE":
            raise RuntimeError("project_not_active")

        return ProjectContext(
            project_id=project.project_id,
            name=project.name,
            repository=project.repository,
            repositories=resolved_repositories(project),
            production_branch=project.production_branch,
            staging_branch=project.staging_branch,
            production_url=project.production_url,
            staging_url=project.staging_url,
            staging_database_enabled=project.staging_database_enabled,
            monthly_budget_chf=project.monthly_budget_chf,
            allowed_models=project.allowed_models,
            default_model=project.default_model,
        )
