import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orders.runtime import WorkOrder
from orders.service import WorkOrderService
from orchestrator.project_context import ProjectContextResolver
from projects.persistence import InMemoryProjectStore
from projects.runtime import Project, ProjectRepository
from projects.service import ProjectService


def service():
    store = InMemoryProjectStore()
    projects = ProjectService(store)
    projects.register(Project(
        project_id="espacore",
        name="Espacore",
        repository="novo34/rediseno-web-espacore-gmbh",
        status="ACTIVE",
        production_branch="main",
        staging_branch="staging",
        production_url="https://espacore.example",
        staging_url="https://staging.espacore.example",
        staging_database_enabled=True,
        monthly_budget_chf=100.0,
        allowed_models=("deepseek", "openai"),
        default_model="deepseek",
    ))
    return WorkOrderService(ProjectContextResolver(projects))


def test_order_resolves_project_repository_and_staging():
    result = service().create(WorkOrder(
        order_id="ORD-1",
        project_id="espacore",
        title="Fix contact form",
        description="Validate and fix contact form flow",
        status="QUEUED",
        budget_limit_chf=10.0,
    ))
    assert result["project"].repository == "novo34/rediseno-web-espacore-gmbh"
    assert result["project"].staging_branch == "staging"
    assert result["project"].default_model == "deepseek"


def test_order_cannot_exceed_project_budget():
    try:
        service().create(WorkOrder(
            order_id="ORD-2",
            project_id="espacore",
            title="Large change",
            description="Large change",
            budget_limit_chf=150.0,
        ))
    except ValueError as exc:
        assert "order_budget_exceeds_project_budget" in str(exc)
        return
    raise AssertionError("order over project budget must fail")


def multi_repo_service():
    store = InMemoryProjectStore()
    projects = ProjectService(store)
    projects.register(Project(
        project_id="multi",
        name="Multi",
        repository="novo34/multi-web",
        status="ACTIVE",
        production_branch="main",
        staging_branch="staging",
        staging_url="https://staging.multi.example",
        staging_database_enabled=True,
        allowed_models=("deepseek",),
        default_model="deepseek",
        repositories=(
            ProjectRepository(
                repository_id="web",
                full_name="novo34/multi-web",
                role="frontend",
                primary=True,
            ),
            ProjectRepository(
                repository_id="api",
                full_name="novo34/multi-api",
                role="backend",
                primary=False,
            ),
        ),
    ))
    return WorkOrderService(ProjectContextResolver(projects))


def test_multi_repo_order_requires_explicit_target_repository():
    try:
        multi_repo_service().create(WorkOrder(
            order_id="ORD-M1",
            project_id="multi",
            title="Change API",
            description="Change API",
        ))
    except ValueError as exc:
        assert "target_repository_required" in str(exc)
        return
    raise AssertionError("multi-repo order must select repository")


def test_multi_repo_order_resolves_selected_repository():
    result = multi_repo_service().create(WorkOrder(
        order_id="ORD-M2",
        project_id="multi",
        title="Change API",
        description="Change API",
        target_repository="api",
    ))
    assert result["repository"].full_name == "novo34/multi-api"
    assert result["order"].target_repository == "api"
