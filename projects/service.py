from __future__ import annotations

from projects.persistence import ProjectStore
from projects.runtime import Project, ProjectConfigError, validate_project


class ProjectService:
    def __init__(self, store: ProjectStore):
        self.store = store

    def register(self, project: Project) -> Project:
        ok, failures = validate_project(project)
        if not ok:
            raise ProjectConfigError(",".join(failures))
        if self.store.get(project.project_id) is not None:
            raise ProjectConfigError("project_already_exists")
        self.store.save(project)
        return project

    def get(self, project_id: str) -> Project:
        project = self.store.get(project_id)
        if project is None:
            raise ProjectConfigError("project_not_found")
        return project

    def list(self, *, status: str | None = None) -> list[Project]:
        projects = self.store.list()
        if status is not None:
            projects = [p for p in projects if p.status == status]
        return sorted(projects, key=lambda p: p.name.lower())
