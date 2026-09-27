from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ApiResponse:
    ok: bool
    data: Any = None
    error: str | None = None
    request_id: str | None = None


def success(data: Any, *, request_id: str | None = None) -> ApiResponse:
    return ApiResponse(ok=True, data=data, request_id=request_id)


def failure(error: str, *, request_id: str | None = None) -> ApiResponse:
    return ApiResponse(ok=False, error=error, request_id=request_id)
