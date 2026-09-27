from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentHandoff:
    handoff_id: str
    task_id: str
    from_agent: str
    to_agent: str
    status: str
    summary: str
    artifacts: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()
    metadata: dict | None = None


def validate_handoff(handoff: AgentHandoff) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if not handoff.handoff_id:
        failures.append("handoff_id_missing")
    if not handoff.task_id:
        failures.append("task_id_missing")
    if not handoff.from_agent or not handoff.to_agent:
        failures.append("agent_missing")
    if handoff.from_agent == handoff.to_agent:
        failures.append("self_handoff_forbidden")
    if handoff.status not in {"PENDING", "ACCEPTED", "REJECTED", "COMPLETED"}:
        failures.append("invalid_handoff_status")
    if not handoff.summary:
        failures.append("handoff_summary_missing")
    return not failures, failures
