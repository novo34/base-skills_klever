from __future__ import annotations

import argparse
import json

RISK_ORDER = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4}

MINIMUMS = {
    "production_deploy": "R4",
    "destructive_data_change": "R4",
    "persistent_memory_promotion": "R4",
    "auth_or_authorization_change": "R3",
    "multi_tenant_isolation_change": "R3",
    "database_schema_change": "R2",
    "public_api_contract_change": "R2",
    "ci_workflow_or_supply_chain_change": "R4",
    "css_only_change": "R0",
    "documentation_only_change": "R0",
}

PATH_RULES = (
    (("authz/", "authorization/", "auth/"), "auth_or_authorization_change"),
    (("github_guard.py", "scripts/github_guard.py"), "auth_or_authorization_change"),
    (("approvals/", "policies/risk-levels.yaml"), "auth_or_authorization_change"),
    (("models/credentials.py", "secrets/", "credentials/"), "auth_or_authorization_change"),
    (("migrations/", "alembic/", "prisma/schema.prisma", "schema.sql"), "database_schema_change"),
    (("api/", "schemas/api-", "openapi"), "public_api_contract_change"),
    ((".github/workflows/",), "ci_workflow_or_supply_chain_change"),
    (("production/", "deploy/production", "prod/"), "production_deploy"),
)


def derive_flags_from_paths(paths: set[str]) -> set[str]:
    derived: set[str] = set()
    normalized: set[str] = set()
    for raw_path in paths:
        path = raw_path.replace("\\", "/")
        while path.startswith("./"):
            path = path[2:]
        normalized.add(path.lower())
    for path in normalized:
        for markers, flag in PATH_RULES:
            if any(path == marker or path.startswith(marker) or marker in path for marker in markers):
                derived.add(flag)
    return derived


def classify(
    flags: set[str],
    default: str = "R1",
    *,
    changed_paths: set[str] | None = None,
) -> str:
    effective_flags = set(flags)
    if changed_paths is not None:
        effective_flags.update(derive_flags_from_paths(changed_paths))
    known = [MINIMUMS[flag] for flag in effective_flags if flag in MINIMUMS]
    if not known:
        return default
    return max(known, key=lambda level: RISK_ORDER[level])


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify JEV task risk.")
    parser.add_argument("--flags", default="", help="Comma-separated declared risk flags.")
    parser.add_argument("--paths", default="", help="Comma-separated changed file paths.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    flags = {item.strip() for item in args.flags.split(",") if item.strip()}
    paths = {item.strip() for item in args.paths.split(",") if item.strip()}
    derived = derive_flags_from_paths(paths)
    risk = classify(flags, changed_paths=paths)

    if args.json:
        print(json.dumps({
            "declared_flags": sorted(flags),
            "derived_flags": sorted(derived),
            "risk": risk,
        }, indent=2))
    else:
        print(risk)


if __name__ == "__main__":
    main()
