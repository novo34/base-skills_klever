from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.classify_risk import RISK_ORDER, classify, derive_flags_from_paths

VALID_RISKS = frozenset(RISK_ORDER)


def validate_changed_paths_risk(
    paths: set[str],
    *,
    declared_risk: str,
) -> dict:
    if not paths:
        raise ValueError("no_changed_paths")
    if declared_risk not in VALID_RISKS:
        raise ValueError("declared_risk_required")

    derived_flags = derive_flags_from_paths(paths)
    derived_risk = classify(set(), changed_paths=paths)

    if RISK_ORDER[derived_risk] > RISK_ORDER[declared_risk]:
        raise PermissionError(
            f"declared_risk_too_low:{declared_risk}<derived:{derived_risk}"
        )

    return {
        "changed_paths": sorted(paths),
        "derived_flags": sorted(derived_flags),
        "declared_risk": declared_risk,
        "derived_risk": derived_risk,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate declared risk against the real changed paths."
    )
    parser.add_argument(
        "--paths-file",
        required=True,
        help="Newline-delimited file containing real changed paths.",
    )
    parser.add_argument(
        "--declared-risk",
        required=True,
        choices=sorted(VALID_RISKS),
        help="Risk explicitly declared for the PR/task.",
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

    try:
        payload = validate_changed_paths_risk(
            paths,
            declared_risk=args.declared_risk,
        )
    except (ValueError, PermissionError) as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
