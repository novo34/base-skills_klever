import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from projects.persistence import InMemoryProjectStore
from projects.runtime import Project, ProjectConfigError
from projects.service import ProjectService


def make_project(**overrides):
    data = dict(
        project_id="espacore",
        name="Espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        status="ACTIVE",
        production_branch="main",
        staging_branch="staging",
        production_url="https://example.com",
        staging_url="https://staging.example.com",
        staging_database_enabled=True,
        monthly_budget_chf=100.0,
        allowed_models=("deepseek", "openai"),
        default_model="deepseek",
        tags=("web", "b2b"),
    )
    data.update(overrides)
    return Project(**data)


def test_active_project_registers_with_separate_staging():
    service = ProjectService(InMemoryProjectStore())
    project = service.register(make_project())
    assert project.production_branch == "main"
    assert project.staging_branch == "staging"
    assert project.staging_database_enabled is True


def test_active_project_requires_staging_database():
    service = ProjectService(InMemoryProjectStore())
    try:
        service.register(make_project(staging_database_enabled=False))
    except ProjectConfigError as exc:
        assert "active_project_staging_database_required" in str(exc)
        return
    raise AssertionError("active project without staging DB must fail")


def test_staging_cannot_equal_main():
    service = ProjectService(InMemoryProjectStore())
    try:
        service.register(make_project(staging_branch="main"))
    except ProjectConfigError as exc:
        assert "staging_branch_must_differ_from_production" in str(exc)
        return
    raise AssertionError("staging branch must differ from main")


def test_default_model_must_be_allowed():
    service = ProjectService(InMemoryProjectStore())
    try:
        service.register(make_project(default_model="unknown"))
    except ProjectConfigError as exc:
        assert "default_model_not_allowed" in str(exc)
        return
    raise AssertionError("default model must be in allow-list")


def test_duplicate_project_is_rejected():
    service = ProjectService(InMemoryProjectStore())
    service.register(make_project())
    try:
        service.register(make_project())
    except ProjectConfigError as exc:
        assert "project_already_exists" in str(exc)
        return
    raise AssertionError("duplicate project id must fail")
