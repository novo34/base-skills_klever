from __future__ import annotations


def requirements_for_triggers(triggers: set[str]) -> dict[str, bool]:
    return {
        "requires_backend": bool(triggers.intersection({"backend", "api", "auth"})),
        "requires_frontend": bool(triggers.intersection({"frontend", "ui", "ux"})),
        "requires_database": bool(triggers.intersection({"database", "migration", "schema"})),
        "requires_e2e": not triggers.issubset({"documentation"}),
    }
