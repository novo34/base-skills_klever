import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestrator.project_context import ProjectContextResolver
from projects.catalog import ProjectCatalogLoader
from projects.persistence import InMemoryProjectStore
from projects.service import ProjectService


def test_catalog_loads_setup_project_without_fake_staging():
    store = InMemoryProjectStore()
    service = ProjectService(store)
    loader = ProjectCatalogLoader(service)

    project = loader.load_file(ROOT / "projects" / "catalog" / "espacore.yaml")

    assert project.project_id == "espacore"
    assert project.repository == "novo34/rediseno-web-espacore-gmbh"
    assert project.status == "SETUP"
    assert project.staging_url is None
    assert project.staging_database_enabled is False


def test_setup_project_cannot_be_used_for_execution():
    store = InMemoryProjectStore()
    service = ProjectService(store)
    ProjectCatalogLoader(service).load_file(
        ROOT / "projects" / "catalog" / "espacore.yaml"
    )

    resolver = ProjectContextResolver(service)

    try:
        resolver.resolve("espacore")
    except RuntimeError as exc:
        assert "project_not_active" in str(exc)
        return

    raise AssertionError("SETUP project must not be executable")
