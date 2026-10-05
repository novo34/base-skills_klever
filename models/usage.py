from __future__ import annotations

from costs.runtime import CostEvent
from models.gateway_contract import ModelResponse


def cost_event_from_response(
    response: ModelResponse,
    *,
    event_id: str,
    project_id: str,
    task_id: str | None,
    occurred_at: str | None = None,
) -> CostEvent:
    return CostEvent(
        event_id=event_id,
        project_id=project_id,
        task_id=task_id,
        provider=response.provider,
        model=response.model,
        amount_chf=response.usage.estimated_cost_chf,
        units=float(response.usage.total_tokens),
        unit_name="tokens",
        category="model",
        occurred_at=occurred_at,
    )
