from __future__ import annotations

from projects.runtime import Project, ProjectConfigError, validate_project


class ProjectRegistry:
    def __init__(self):
        self._projects: dict[str, Project] = {}

    def register(self, project: Project) -> Project:
        ok, failures = validate_project(project)
        if not ok:
            raise ProjectConfigError(",".join(failures))
        if project.project_id in self._projects:
            raise ProjectConfigError("project_already_exists")
        self._projects[project.project_id] = project
        return project

    def update(self, project: Project) -> Project:
        ok, failures = validate_project(project)
        if not ok:
            raise ProjectConfigError(",".join(failures))
        if project.project_id not in self._projects:
            raise ProjectConfigError("project_not_found")
        self._projects[project.project_id] = project
        return project

    def get(self, project_id: str) -> Project:
        if project_id not in self._projects:
            raise ProjectConfigError("project_not_found")
        return self._projects[project_id]

    def list(self, *, status: str | None = None) -> list[Project]:
        projects = list(self._projects.values())
        if status is not None:
            projects = [p for p in projects if p.status == status]
        return sorted(projects, key=lambda p: p.name.lower())

    def resolve_repository(self, project_id: str) -> str:
        return self.get(project_id).repository

    def pause(self, project_id: str) -> Project:
        current = self.get(project_id)
        updated = Project(
            **{**current.__dict__, "status": "PAUSED"}
        )
        self._projects[project_id] = updated
        return updated
