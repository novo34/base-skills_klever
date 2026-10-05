from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ControlCommand:
    command_id: str
    actor: str
    action: str
    project_id: str
    target_id: str | None = None
    payload: dict | None = None


ALLOWED_ACTIONS = {
    "CREATE_ORDER",
    "PAUSE_PROJECT",
    "RESUME_PROJECT",
    "APPROVE_TASK",
    "REQUEST_CHANGES",
    "REJECT_TASK",
    "RETRY_TASK",
    "REQUEST_AUDIT",
    "GET_PROJECT_STATUS",
    "GET_DASHBOARD",
    "GET_REPORT",
    "SET_BUDGET",
}


def validate_command(command: ControlCommand) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if not command.command_id:
        failures.append("command_id_missing")
    if not command.actor:
        failures.append("actor_missing")
    if command.action not in ALLOWED_ACTIONS:
        failures.append("unsupported_action")
    if not command.project_id:
        failures.append("project_id_missing")
    return not failures, failures
