from __future__ import annotations

from dataclasses import replace

from models.circuit_breaker import CircuitBreaker
from models.gateway_contract import ModelRequest, ModelResponse
from models.provider_registry import ProviderRegistry


class ModelGatewayError(RuntimeError):
    pass


class ModelGateway:
    def __init__(
        self,
        registry: ProviderRegistry,
        *,
        circuit_breaker: CircuitBreaker | None = None,
    ):
        self.registry = registry
        self.circuit_breaker = circuit_breaker or CircuitBreaker()

    def execute(
        self,
        request: ModelRequest,
        *,
        fallback_chain: tuple[tuple[str, str], ...] = (),
    ) -> ModelResponse:
        attempts = ((request.provider, request.model),) + fallback_chain
        errors: list[str] = []

        for provider, model in attempts:
            if not self.circuit_breaker.allow(provider):
                errors.append(f"{provider}:circuit_open")
                continue

            adapter = self.registry.get(provider)
            candidate = replace(request, provider=provider, model=model)

            try:
                response = adapter.execute(candidate)
            except Exception as exc:
                self.circuit_breaker.failure(provider)
                errors.append(f"{provider}:{type(exc).__name__}")
                continue

            self.circuit_breaker.success(provider)
            return response

        raise ModelGatewayError("all_model_attempts_failed:" + ",".join(errors))
