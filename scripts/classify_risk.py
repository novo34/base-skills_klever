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
    "css_only_change": "R0",
    "documentation_only_change": "R0",
}


def classify(flags: set[str], default: str = "R1") -> str:
    risk = default
    for flag in flags:
        candidate = MINIMUMS.get(flag)
        if candidate and RISK_ORDER[candidate] > RISK_ORDER[risk]:
            risk = candidate
    return risk


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify JEV task risk.")
    parser.add_argument("--flags", required=True, help="Comma-separated risk flags.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    flags = {item.strip() for item in args.flags.split(",") if item.strip()}
    risk = classify(flags)

    if args.json:
        print(json.dumps({"flags": sorted(flags), "risk": risk}, indent=2))
    else:
        print(risk)


if __name__ == "__main__":
    main()
