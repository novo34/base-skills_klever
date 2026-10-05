import pathlib
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PROVIDERS = {
    "deepseek": ROOT / "models/providers/deepseek.yaml",
    "openai": ROOT / "models/providers/openai-codex.yaml",
    "qwen": ROOT / "models/providers/qwen.yaml",
    "glm": ROOT / "models/providers/glm.yaml",
}


def test_all_required_provider_profiles_exist_and_are_normalized():
    for expected, path in PROVIDERS.items():
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert data["provider"] == expected
        assert data["implementation_scope"] == "PLATFORM"
        assert data["normalized"]["request"] == "ModelRequest"
        assert data["normalized"]["response"] == "ModelResponse"
        assert data["normalized"]["usage"] == "ModelUsage"
        assert data["requirements"]["timeout"] == "required"
        assert data["requirements"]["circuit_breaker"] == "required"
        assert data["requirements"]["credentials"] == "external_only"
        assert data["requirements"]["usage_normalization"] == "required"
        assert data["requirements"]["cost_normalization_chf"] == "required"
