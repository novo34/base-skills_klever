from __future__ import annotations

import pathlib
import yaml

from projects.runtime import Project
from projects.service import ProjectService


class ProjectCatalogLoader:
    def __init__(self, service: ProjectService):
        self.service = service

    def load_file(self, path: pathlib.Path) -> Project:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        project = Project(
            project_id=data["project_id"],
            name=data["name"],
            repository=data["repository"],
            status=data["status"],
            production_branch=data.get("production_branch", "main"),
            staging_branch=data.get("staging_branch", "staging"),
            production_url=data.get("production_url"),
            staging_url=data.get("staging_url"),
            staging_database_enabled=bool(data.get("staging_database_enabled", False)),
            monthly_budget_chf=data.get("monthly_budget_chf"),
            allowed_models=tuple(data.get("allowed_models", [])),
            default_model=data.get("default_model"),
            tags=tuple(data.get("tags", [])),
            metadata=data.get("metadata", {}),
        )
        return self.service.register(project)

    def load_directory(self, directory: pathlib.Path) -> list[Project]:
        loaded = []
        for path in sorted(directory.glob("*.yaml")):
            loaded.append(self.load_file(path))
        return loaded
