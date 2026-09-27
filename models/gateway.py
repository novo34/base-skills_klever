from __future__ import annotations

from dataclasses import replace

from models.circuit_breaker import CircuitBreaker
from models.errors import ModelProviderError
from models.gateway_contract import ModelRequest, ModelResponse
from models.provider_registry import ProviderRegistry
from models.retry import RetryPolicy


class ModelGatewayError(RuntimeError):
    pass


class ModelGateway:
    def __init__(
        self,
        registry: ProviderRegistry,
        *,
        circuit_breaker: CircuitBreaker | None = None,
        retry_policy: RetryPolicy | None = None,
    ):
        self.registry = registry
        self.circuit_breaker = circuit_breaker or CircuitBreaker()
        self.retry_policy = retry_policy or RetryPolicy()

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

            for attempt in range(1, self.retry_policy.max_attempts + 1):
                try:
                    response = adapter.execute(candidate)
                except ModelProviderError as exc:
                    self.circuit_breaker.failure(provider)
                    errors.append(f"{provider}:{exc.code}:attempt_{attempt}")
                    if not exc.retryable:
                        break
                    if attempt >= self.retry_policy.max_attempts:
                        break
                    continue
                except Exception as exc:
                    self.circuit_breaker.failure(provider)
                    errors.append(f"{provider}:unexpected_{type(exc).__name__}:attempt_{attempt}")
                    break

                self.circuit_breaker.success(provider)
                return response

        raise ModelGatewayError("all_model_attempts_failed:" + ",".join(errors))
