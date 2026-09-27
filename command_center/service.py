from __future__ import annotations

from command_center.model_interpreter import ModelCommandInterpreter
from command_center.parser import parse_command
from command_center.runtime import CommandIntent, validate_intent
from control.runtime import ControlCommand


class CommandCenter:
    def __init__(self, interpreter: ModelCommandInterpreter | None = None):
        self.interpreter = interpreter

    def interpret(
        self,
        *,
        intent_id: str,
        actor: str,
        text: str,
        project_id_hint: str | None = None,
    ) -> CommandIntent:
        if self.interpreter is not None:
            intent = self.interpreter.interpret(
                intent_id=intent_id,
                actor=actor,
                text=text,
                project_id_hint=project_id_hint,
            )
        else:
            intent = parse_command(
                intent_id=intent_id,
                actor=actor,
                text=text,
            )
            if intent.project_id is None and project_id_hint is not None:
                intent = CommandIntent(
                    **{
                        **intent.__dict__,
                        "project_id": project_id_hint,
                    }
                )

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
