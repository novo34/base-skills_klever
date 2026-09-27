from __future__ import annotations

from dataclasses import dataclass

from projects.service import ProjectService


@dataclass(frozen=True)
class ProjectContext:
    project_id: str
    name: str
    repository: str
    production_branch: str
    staging_branch: str
    production_url: str | None
    staging_url: str | None
    staging_database_enabled: bool
    monthly_budget_chf: float | None
    allowed_models: tuple[str, ...]
    default_model: str | None


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
            production_branch=project.production_branch,
            staging_branch=project.staging_branch,
            production_url=project.production_url,
            staging_url=project.staging_url,
            staging_database_enabled=project.staging_database_enabled,
            monthly_budget_chf=project.monthly_budget_chf,
            allowed_models=project.allowed_models,
            default_model=project.default_model,
        )
