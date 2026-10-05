import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from models.credentials import EnvironmentCredentialProvider
from models.gateway_contract import ProviderHealth


def test_credentials_are_injected_from_environment_mapping():
    provider = EnvironmentCredentialProvider({
        "JEV_PROVIDER_DEEPSEEK_API_KEY": "secret-value"
    })
    credential = provider.get("deepseek")
    assert credential.provider == "deepseek"
    assert credential.value == "secret-value"


def test_missing_external_credential_fails_closed():
    provider = EnvironmentCredentialProvider({})
    try:
        provider.get("openai")
    except KeyError as exc:
        assert "provider_credential_missing" in str(exc)
        return
    raise AssertionError("missing credentials must fail closed")


def test_provider_health_is_normalized():
    health = ProviderHealth(ok=True, latency_ms=12.5, detail="healthy")
    assert health.ok is True
    assert health.latency_ms == 12.5
    assert health.detail == "healthy"
