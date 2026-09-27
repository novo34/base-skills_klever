import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from budgets.runtime import BudgetPolicy
from budgets.service import BudgetExceededError, BudgetService


def policy():
    return BudgetPolicy(
        project_id="espacore",
        monthly_limit_chf=100.0,
        daily_limit_chf=20.0,
        task_limit_chf=10.0,
        warning_threshold_pct=80.0,
        hard_stop=True,
    )


def test_budget_allows_action_below_limits():
    result = BudgetService().require_budget(
        policy=policy(),
        month_spend_chf=20.0,
        day_spend_chf=5.0,
        task_spend_chf=2.0,
        estimated_next_cost_chf=1.0,
    )
    assert result["allowed"] is True
    assert result["exceeded"] == []


def test_budget_warns_near_threshold():
    result = BudgetService().evaluate(
        policy=policy(),
        month_spend_chf=80.0,
        day_spend_chf=1.0,
        task_spend_chf=1.0,
        estimated_next_cost_chf=0.0,
    )
    assert "monthly" in result["warnings"]


def test_budget_hard_stop_blocks_next_action():
    try:
        BudgetService().require_budget(
            policy=policy(),
            month_spend_chf=95.0,
            day_spend_chf=10.0,
            task_spend_chf=9.5,
            estimated_next_cost_chf=1.0,
        )
    except BudgetExceededError as exc:
        assert "budget_hard_stop" in str(exc)
        assert "task" in str(exc)
        return
    raise AssertionError("hard stop must block over-budget action")


def test_soft_budget_can_allow_overage():
    soft = BudgetPolicy(
        project_id="espacore",
        task_limit_chf=5.0,
        hard_stop=False,
    )
    result = BudgetService().require_budget(
        policy=soft,
        month_spend_chf=0.0,
        day_spend_chf=0.0,
        task_spend_chf=5.0,
        estimated_next_cost_chf=1.0,
    )
    assert result["allowed"] is True
    assert result["exceeded"] == ["task"]
