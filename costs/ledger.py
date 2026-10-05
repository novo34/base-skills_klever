from __future__ import annotations

from collections import defaultdict

from costs.runtime import CostEvent, validate_cost_event


class CostLedger:
    def __init__(self):
        self._events: list[CostEvent] = []
        self._ids: set[str] = set()

    def record(self, event: CostEvent) -> CostEvent:
        ok, failures = validate_cost_event(event)
        if not ok:
            raise ValueError(",".join(failures))
        if event.event_id in self._ids:
            raise ValueError("duplicate_cost_event")
        self._events.append(event)
        self._ids.add(event.event_id)
        return event

    def list(self, *, project_id: str | None = None) -> list[CostEvent]:
        if project_id is None:
            return list(self._events)
        return [e for e in self._events if e.project_id == project_id]

    def project_total(self, project_id: str) -> float:
        return round(sum(e.amount_chf for e in self.list(project_id=project_id)), 2)

    def provider_totals(self, *, project_id: str | None = None) -> dict[str, float]:
        totals: dict[str, float] = defaultdict(float)
        for event in self.list(project_id=project_id):
            totals[event.provider] += event.amount_chf
        return {key: round(value, 2) for key, value in sorted(totals.items())}
