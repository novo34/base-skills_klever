from __future__ import annotations


class ModelProviderError(RuntimeError):
    retryable = False
    code = "provider_error"


class ProviderTimeoutError(ModelProviderError):
    retryable = True
    code = "provider_timeout"


class ProviderRateLimitError(ModelProviderError):
    retryable = True
    code = "provider_rate_limited"


class ProviderUnavailableError(ModelProviderError):
    retryable = True
    code = "provider_unavailable"


class ProviderAuthError(ModelProviderError):
    retryable = False
    code = "provider_auth_failed"


class ProviderInvalidRequestError(ModelProviderError):
    retryable = False
    code = "provider_invalid_request"
