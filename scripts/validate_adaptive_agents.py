from __future__ import annotations

import pathlib
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

EXPECTED = {
    "architect": {
        "required_skills": {
            "22-intent-discovery-and-refinement",
            "23-spec-and-constraints",
            "24-planning-task-breakdown",
            "47-adaptive-workflow-compilation",
            "48-plan-mutation-and-replanning",
            "55-capability-composition",
        },
        "forbidden": {"code_write", "self_verify", "production_approve", "self_promote_improvement"},
    },
    "developer": {
        "required_skills": {
            "25-source-grounded-development",
            "26-incremental-test-driven-development",
            "28-code-simplification",
            "91-repository-hygiene-and-dead-code",
            "92-duplication-and-reuse-guard",
        },
        "forbidden": {"self_verify", "production_approve", "production_merge", "self_promote_improvement"},
    },
    "verifier": {
        "required_skills": {
            "30-browser-runtime-verification",
            "31-adversarial-doubt-review",
            "91-repository-hygiene-and-dead-code",
            "92-duplication-and-reuse-guard",
        },
        "forbidden": {"code_write", "self_repair_reviewed_code", "production_approve", "self_promote_improvement"},
    },
    "integrator": {
        "required_skills": {
            "24-planning-task-breakdown",
            "47-adaptive-workflow-compilation",
            "48-plan-mutation-and-replanning",
            "56-artifact-conversation-and-review",
        },
        "forbidden": {"self_verify", "production_approve", "whole_staging_promotion", "self_promote_improvement"},
    },
}

errors: list[str] = []

for role, expected in EXPECTED.items():
    path = ROOT / "agents" / f"{role}.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    skills = set(((data.get("skills") or {}).get("mandatory") or []))
    forbidden = set(data.get("forbidden_actions") or [])
    permissions = set(data.get("permissions") or [])

    missing_skills = expected["required_skills"] - skills
    if missing_skills:
        errors.append(f"{role}: missing adaptive skills {sorted(missing_skills)}")

    missing_forbidden = expected["forbidden"] - forbidden
    if missing_forbidden:
        errors.append(f"{role}: missing forbidden actions {sorted(missing_forbidden)}")

    if role == "developer":
        if data.get("can_merge") is not False:
            errors.append("developer: can_merge must remain false")
        if "pull_request_review" in permissions:
            errors.append("developer: verification permission forbidden")
    if role == "verifier":
        if data.get("can_write_code") is not False:
            errors.append("verifier: can_write_code must remain false")
    if role == "integrator" and data.get("can_merge") is not False:
        errors.append("integrator: autonomous merge permission must remain false")

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)

print("OK: adaptive agent contracts preserve role authority and separation of duties")
