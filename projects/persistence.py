from __future__ import annotations

from abc import ABC, abstractmethod

from projects.runtime import Project


class ProjectStore(ABC):
    @abstractmethod
    def save(self, project: Project) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, project_id: str) -> Project | None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Project]:
        raise NotImplementedError


class InMemoryProjectStore(ProjectStore):
    def __init__(self):
        self._items: dict[str, Project] = {}

    def save(self, project: Project) -> None:
        self._items[project.project_id] = project

    def get(self, project_id: str) -> Project | None:
        return self._items.get(project_id)

    def list(self) -> list[Project]:
        return list(self._items.values())
