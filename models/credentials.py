from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderCredential:
    provider: str
    value: str


class CredentialProvider(ABC):
    @abstractmethod
    def get(self, provider: str) -> ProviderCredential:
        raise NotImplementedError


class EnvironmentCredentialProvider(CredentialProvider):
    def __init__(self, env: dict[str, str]):
        self.env = env

    def get(self, provider: str) -> ProviderCredential:
        key = f"JEV_PROVIDER_{provider.upper()}_API_KEY"
        value = self.env.get(key)
        if not value:
            raise KeyError("provider_credential_missing")
        return ProviderCredential(provider=provider, value=value)
