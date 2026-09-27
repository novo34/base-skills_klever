import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


run_guard = load("run_guard", "scripts/run_guard.py")
lock_manager = load("lock_manager", "scripts/lock_manager.py")


def test_budget_blocks_next_action_when_cost_would_exceed():
    limits = run_guard.Limits(max_actions=10, max_retries=3, max_cost_usd=1.0)
    usage = run_guard.Usage(actions=2, retries=0, cost_usd=0.9)
    ok, reason = run_guard.can_take_action(limits, usage, estimated_cost_usd=0.2)
    assert ok is False
    assert reason == "estimated_cost_exceeds_budget"


def test_action_limit_is_hard_stop():
    limits = run_guard.Limits(max_actions=3, max_retries=3, max_cost_usd=10)
    usage = run_guard.Usage(actions=3, retries=0, cost_usd=0)
    ok, reason = run_guard.can_take_action(limits, usage)
    assert ok is False
    assert reason == "max_actions_reached"


def test_lock_prevents_other_agent_write():
    locks = lock_manager.acquire_lock([], "prisma/schema.prisma", "database-agent", "TASK-1")
    try:
        lock_manager.assert_write_allowed(locks, "prisma/schema.prisma", "backend-agent", "TASK-2")
    except PermissionError:
        return
    raise AssertionError("conflicting writer must be blocked")


def test_owner_can_write_and_release_lock():
    locks = lock_manager.acquire_lock([], "src/api.ts", "developer", "TASK-3")
    lock_manager.assert_write_allowed(locks, "src/api.ts", "developer", "TASK-3")
    released = lock_manager.release_lock(locks, "src/api.ts", "developer", "TASK-3")
    assert released[0]["status"] == "RELEASED"
