from __future__ import annotations

from typing import Any


def github_ci_status(checks: dict[str, Any]) -> str:
    status = checks.get("status")
    conclusion = checks.get("conclusion")

    if conclusion:
        return str(conclusion).lower()
    if status == "success":
        return "success"
    if status in {"completed", "complete"} and checks.get("success") is True:
        return "success"
    return str(status or "unknown").lower()


def command_exit_code(result: dict[str, Any] | None) -> int | None:
    if result is None:
        return None
    value = result.get("exit_code")
    return value if isinstance(value, int) else None
