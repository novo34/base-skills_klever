import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from command_center.service import CommandCenter


def test_pause_project_command_is_structured():
    center = CommandCenter()
    intent = center.interpret(
        intent_id="INT-1",
        actor="owner",
        text="Pausa Espacore",
    )
    assert intent.action == "PAUSE_PROJECT"
    assert intent.project_id == "espacore"

    command = center.to_control_command(intent)
    assert command.action == "PAUSE_PROJECT"
    assert command.project_id == "espacore"


def test_budget_command_requires_confirmation():
    center = CommandCenter()
    intent = center.interpret(
        intent_id="INT-2",
        actor="owner",
        text="No gastes más de CHF 20 en Espacore",
    )
    assert intent.action == "SET_BUDGET"
    assert intent.payload["limit_chf"] == 20.0
    assert intent.requires_confirmation is True

    try:
        center.to_control_command(intent)
    except PermissionError as exc:
        assert "command_confirmation_required" in str(exc)
        return
    raise AssertionError("budget change must require confirmation")


def test_unknown_command_is_not_executed():
    center = CommandCenter()
    intent = center.interpret(
        intent_id="INT-3",
        actor="owner",
        text="Haz algo raro",
    )
    assert intent.action is None
    assert intent.confidence == 0.0


def test_project_hint_can_resolve_deterministic_intent():
    center = CommandCenter()
    intent = center.interpret(
        intent_id="INT-HINT",
        actor="owner",
        text="Audita TASK-12",
        project_id_hint="espacore",
    )
    assert intent.project_id == "espacore"
    command = center.to_control_command(intent)
    assert command.project_id == "espacore"


def test_confirmed_budget_intent_becomes_control_command():
    center = CommandCenter()
    intent = center.interpret(
        intent_id="INT-BUDGET-CONFIRMED",
        actor="owner",
        text="No gastes más de CHF 20 en Espacore",
    )
    command = center.to_control_command(intent, confirmed=True)
    assert command.action == "SET_BUDGET"
    assert command.project_id == "espacore"
    assert command.payload["monthly_limit_chf"] == 20.0
