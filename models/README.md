# JEV Model Gateway

The Model Gateway keeps AI providers replaceable.

Agents request a capability through JEV. They do not own provider credentials and they do not decide policy.

The gateway is responsible for:

- provider lookup
- model selection input
- execution
- fallback chain
- circuit breaker
- provider health
- normalized usage
- cost conversion
- audit-ready metadata

Concrete provider adapters (DeepSeek, OpenAI/Codex, Qwen, GLM) are implemented separately so provider APIs can change without changing agent contracts.

JEV policy remains above the gateway: budgets, permissions, risk and human gates cannot be bypassed by a provider.


## Credentials and failures

Provider credentials are injected by a `CredentialProvider` (for example from environment/secrets at runtime). Credentials must never be embedded in task payloads, agent prompts, repository configuration or committed files.

Provider adapters expose normalized `ProviderHealth` and raise typed provider errors. Retry is allowed only for errors explicitly marked retryable; authentication and invalid-request failures fail closed and may fall back only to another allowed provider.
