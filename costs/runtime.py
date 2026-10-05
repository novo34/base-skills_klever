from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CostEvent:
    event_id: str
    project_id: str
    task_id: str | None
    provider: str
    model: str
    amount_chf: float
    units: float = 0.0
    unit_name: str = "tokens"
    category: str = "model"
    occurred_at: str | None = None


def validate_cost_event(event: CostEvent) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if not event.event_id:
        failures.append("event_id_missing")
    if not event.project_id:
        failures.append("project_id_missing")
    if not event.provider:
        failures.append("provider_missing")
    if not event.model:
        failures.append("model_missing")
    if event.amount_chf < 0:
        failures.append("negative_cost")
    if event.units < 0:
        failures.append("negative_units")
    return not failures, failures
