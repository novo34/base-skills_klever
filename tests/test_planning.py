import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("plan_task", ROOT / "scripts" / "plan_task.py")
plan_task = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(plan_task)


def test_css_change_is_r0_and_single_developer():
    plan = plan_task.build_plan(
        "TASK-001",
        {"ui", "frontend", "implementation"},
        {"css_only_change"},
    )
    assert plan["risk"] == "R0"
    assert plan["agents"] == ["developer"]
    assert plan["gates"]["human_approval"] is False
    assert plan["gates"]["direct_main_write_allowed"] is False


def test_auth_change_is_at_least_r3():
    plan = plan_task.build_plan(
        "TASK-002",
        {"auth", "backend", "api", "implementation"},
        {"auth_or_authorization_change"},
    )
    assert plan["risk"] == "R3"
    assert "architect" in plan["agents"]
    assert "developer" in plan["agents"]
    assert "verifier" in plan["agents"]
    assert "05-auth-security" in plan["skills"]


def test_production_destructive_change_is_r4_human_gated():
    plan = plan_task.build_plan(
        "TASK-003",
        {"database", "deployment", "implementation"},
        {"production_deploy", "destructive_data_change"},
    )
    assert plan["risk"] == "R4"
    assert plan["gates"]["human_approval"] is True
    assert "integrator" in plan["agents"]


def test_mandatory_skills_always_load():
    plan = plan_task.build_plan("TASK-004", set(), set())
    for skill in (
        "00-skill-priority",
        "01-preflight-check",
        "20-core-behavior",
        "36-git-workflow-versioning",
        "37-ci-quality-gates",
        "90-code-review-quality",
    ):
        assert skill in plan["skills"]


def test_unknown_flags_fall_back_to_r1():
    plan = plan_task.build_plan(
        "TASK-005",
        {"implementation"},
        {"unclassified_change"},
    )
    assert plan["risk"] == "R1"


def test_high_risk_flag_wins_over_low_risk_flag():
    plan = plan_task.build_plan(
        "TASK-006",
        {"auth", "frontend", "implementation"},
        {"css_only_change", "auth_or_authorization_change"},
    )
    assert plan["risk"] == "R3"
