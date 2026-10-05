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


def test_catalog_loads_multiple_repositories(tmp_path):
    config = tmp_path / "multi.yaml"
    config.write_text(
        """
project_id: multi
name: Multi
repository: novo34/multi-web
status: SETUP
production_branch: main
staging_branch: staging
allowed_models:
  - deepseek
default_model: deepseek
repositories:
  - repository_id: web
    full_name: novo34/multi-web
    role: frontend
    primary: true
    production_branch: main
    staging_branch: staging
  - repository_id: api
    full_name: novo34/multi-api
    role: backend
    primary: false
    production_branch: main
    staging_branch: integration
    staging_url: https://api-staging.example
    staging_database_enabled: true
    environment_metadata:
      hosting: api-host
""".strip(),
        encoding="utf-8",
    )

    service = ProjectService(InMemoryProjectStore())
    project = ProjectCatalogLoader(service).load_file(config)

    assert len(project.repositories) == 2
    assert project.repositories[1].repository_id == "api"
    assert project.repositories[1].role == "backend"
    assert project.repositories[1].staging_branch == "integration"
    assert project.repositories[1].staging_url == "https://api-staging.example"
    assert project.repositories[1].environment_metadata["hosting"] == "api-host"
