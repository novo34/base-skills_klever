from __future__ import annotations

from models.gateway_contract import ModelProviderAdapter


class ProviderRegistry:
    def __init__(self):
        self._providers: dict[str, ModelProviderAdapter] = {}

    def register(self, provider: str, adapter: ModelProviderAdapter) -> None:
        if not provider:
            raise ValueError("provider_name_required")
        if provider in self._providers:
            raise ValueError("provider_already_registered")
        self._providers[provider] = adapter

    def get(self, provider: str) -> ModelProviderAdapter:
        if provider not in self._providers:
            raise KeyError("provider_not_registered")
        return self._providers[provider]

    def available(self) -> tuple[str, ...]:
        return tuple(sorted(self._providers))
