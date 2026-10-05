from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandIntent:
    intent_id: str
    actor: str
    text: str
    project_id: str | None = None
    action: str | None = None
    target_id: str | None = None
    confidence: float = 0.0
    requires_confirmation: bool = False
    payload: dict | None = None


SUPPORTED_INTENTS = {
    "PAUSE_PROJECT",
    "RESUME_PROJECT",
    "CREATE_ORDER",
    "REQUEST_AUDIT",
    "RETRY_TASK",
    "SET_BUDGET",
    "GET_PROJECT_STATUS",
    "GET_DASHBOARD",
    "GET_REPORT",
}


def validate_intent(intent: CommandIntent) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if not intent.intent_id:
        failures.append("intent_id_missing")
    if not intent.actor:
        failures.append("actor_missing")
    if not intent.text:
        failures.append("text_missing")
    if intent.action is not None and intent.action not in SUPPORTED_INTENTS:
        failures.append("unsupported_intent")
    if not 0 <= intent.confidence <= 1:
        failures.append("confidence_out_of_range")
    return not failures, failures
