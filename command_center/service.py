from __future__ import annotations

from command_center.parser import parse_command
from command_center.runtime import CommandIntent, validate_intent
from control.runtime import ControlCommand


class CommandCenter:
    def interpret(self, *, intent_id: str, actor: str, text: str) -> CommandIntent:
        intent = parse_command(intent_id=intent_id, actor=actor, text=text)
        ok, failures = validate_intent(intent)
        if not ok:
            raise ValueError(",".join(failures))
        return intent

    def to_control_command(
        self,
        intent: CommandIntent,
        *,
        confirmed: bool = False,
        resolved_project_id: str | None = None,
    ) -> ControlCommand:
        if intent.action is None:
            raise ValueError("intent_not_resolved")
        if intent.requires_confirmation and not confirmed:
            raise PermissionError("command_confirmation_required")

        project_id = resolved_project_id or intent.project_id
        if not project_id:
            raise ValueError("project_resolution_required")

        if intent.action == "SET_BUDGET":
            raise NotImplementedError("budget_command_requires_budget_control_path")

        return ControlCommand(
            command_id=f"CMD-{intent.intent_id}",
            actor=intent.actor,
            action=intent.action,
            project_id=project_id,
            target_id=intent.target_id,
            payload=intent.payload,
        )
