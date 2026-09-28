from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.classify_risk import RISK_ORDER, classify, derive_flags_from_paths


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate automatic risk classification against the real changed paths."
    )
    parser.add_argument(
        "--paths-file",
        required=True,
        help="Newline-delimited file containing the real changed paths.",
    )
    args = parser.parse_args()

    path_file = pathlib.Path(args.paths_file)
    if not path_file.is_file():
        raise SystemExit("ERROR: changed paths file missing")

    paths = {
        line.strip()
        for line in path_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    if not paths:
        raise SystemExit("ERROR: no changed paths supplied to risk gate")

    derived = derive_flags_from_paths(paths)
    risk = classify(set(), changed_paths=paths)

    minimums = {
        "auth_or_authorization_change": "R3",
        "multi_tenant_isolation_change": "R3",
        "database_schema_change": "R2",
        "public_api_contract_change": "R2",
        "ci_workflow_or_supply_chain_change": "R4",
        "production_deploy": "R4",
    }
    failures: list[str] = []
    for flag in sorted(derived):
        minimum = minimums.get(flag)
        if minimum is not None and RISK_ORDER[risk] < RISK_ORDER[minimum]:
            failures.append(
                f"{flag} requires at least {minimum}, but real diff classified {risk}"
            )

    payload = {
        "changed_paths": sorted(paths),
        "derived_flags": sorted(derived),
        "risk": risk,
    }
    print(json.dumps(payload, indent=2))

    if failures:
        print("\n".join(f"ERROR: {item}" for item in failures))
        sys.exit(1)


if __name__ == "__main__":
    main()
