from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.classify_risk import RISK_ORDER, classify, derive_flags_from_paths
from scripts.validate_changed_paths_risk import validate_changed_paths_risk

ACK_PATTERN = re.compile(
    r"(?mi)^\s*JEV-INDEPENDENT-REVIEW:\s*acknowledged\s*$"
)

SELF_PROTECTION_PREFIXES = (
    ".github/workflows/",
    ".github/CODEOWNERS",
    "scripts/validate_security_defaults.py",
    "scripts/validate_changed_paths_risk.py",
    "scripts/independent_review.py",
    "scripts/classify_risk.py",
    "policies/risk-levels.yaml",
    "docs/REQUIRED_GITHUB_SECURITY_SETTINGS.md",
)


def is_self_protection_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return any(
        normalized == protected or normalized.startswith(protected)
        for protected in SELF_PROTECTION_PREFIXES
    )


def review_pull_request(
    paths: set[str],
    *,
    declared_risk: str,
    pr_body: str,
) -> dict:
    if not paths:
        raise ValueError("no_changed_paths")

    risk_payload = validate_changed_paths_risk(
        paths,
        declared_risk=declared_risk,
    )

    self_protection_paths = sorted(
        path for path in paths if is_self_protection_path(path)
    )
    derived_flags = derive_flags_from_paths(paths)
    derived_risk = classify(set(), changed_paths=paths)

    requires_ack = bool(self_protection_paths) or RISK_ORDER[derived_risk] >= RISK_ORDER["R4"]
    acknowledged = bool(ACK_PATTERN.search(pr_body))

    if self_protection_paths and declared_risk != "R4":
        raise PermissionError("self_protection_change_requires_R4")

    if requires_ack and not acknowledged:
        raise PermissionError(
            "independent_review_acknowledgement_required"
        )

    return {
        **risk_payload,
        "self_protection_paths": self_protection_paths,
        "requires_acknowledgement": requires_ack,
        "acknowledged": acknowledged,
        "review_mode": "single_operator_base_controlled_automation",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run a base-controlled independent review for single-operator PRs "
            "without executing code from the PR head."
        )
    )
    parser.add_argument("--paths-file", required=True)
    parser.add_argument("--pr-body-file", required=True)
    parser.add_argument("--declared-risk", required=True, choices=[f"R{i}" for i in range(5)])
    args = parser.parse_args()

    paths = {
        line.strip()
        for line in pathlib.Path(args.paths_file)
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    }
    pr_body = pathlib.Path(args.pr_body_file).read_text(encoding="utf-8")

    try:
        payload = review_pull_request(
            paths,
            declared_risk=args.declared_risk,
            pr_body=pr_body,
        )
    except (ValueError, PermissionError) as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1)

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
