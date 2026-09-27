from __future__ import annotations

import argparse
import json
import pathlib
import yaml

try:
    from scripts.classify_risk import classify as classify_with_paths, derive_flags_from_paths
except ModuleNotFoundError:
    from classify_risk import classify as classify_with_paths, derive_flags_from_paths

ROOT = pathlib.Path(__file__).resolve().parents[1]
RISK_ORDER = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4}

RISK_FLAGS = {
    "production_deploy": "R4",
    "destructive_data_change": "R4",
    "persistent_memory_promotion": "R4",
    "auth_or_authorization_change": "R3",
    "multi_tenant_isolation_change": "R3",
    "database_schema_change": "R2",
    "public_api_contract_change": "R2",
    "ci_workflow_or_supply_chain_change": "R4",
    "ci_workflow_or_supply_chain_change": "R4",
    "css_only_change": "R0",
    "documentation_only_change": "R0",
}


def load_yaml(path: str) -> dict:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def classify_risk(flags: set[str], default: str = "R1") -> str:
    known = [RISK_FLAGS[flag] for flag in flags if flag in RISK_FLAGS]
    if not known:
        return default
    return max(known, key=lambda level: RISK_ORDER[level])


def resolve_skills(triggers: set[str]) -> list[dict]:
    manifest = load_yaml("skills-manifest.yaml")
    selected = []
    for skill in manifest.get("skills", []):
        skill_triggers = set(skill.get("triggers", []))
        if skill.get("mandatory") or "all" in skill_triggers or triggers.intersection(skill_triggers):
            selected.append(skill)
    return sorted(selected, key=lambda item: item.get("priority", 0), reverse=True)


def select_agents(risk: str) -> list[str]:
    registry = load_yaml("agents/registry.yaml")
    return list(registry.get("risk_assignments", {}).get(risk, []))


def select_models(risk: str, agents: list[str]) -> dict:
    router = load_yaml("models/model-router.yaml")
    route = router.get("routing", {}).get(risk, {})
    preferred = route.get("preferred", [])
    overrides = router.get("role_overrides", {})
    return {
        "preferred": preferred,
        "role_minimum_tiers": {
            agent: overrides.get(agent, {}).get("minimum_tier", "economy")
            for agent in agents
        },
    }


def build_plan(
    task_id: str,
    triggers: set[str],
    flags: set[str],
    *,
    changed_paths: set[str] | None = None,
) -> dict:
    risk = classify_with_paths(flags, changed_paths=changed_paths)
    derived_flags = derive_flags_from_paths(changed_paths or set())
    agents = select_agents(risk)
    skills = resolve_skills(triggers)

    return {
        "task_id": task_id,
        "risk": risk,
        "declared_risk_flags": sorted(flags),
        "derived_risk_flags": sorted(derived_flags),
        "agents": agents,
        "skills": [item["id"] for item in skills],
        "model_route": select_models(risk, agents),
        "gates": {
            "production_human_approval": True,
            "critical_operation_human_approval": risk == "R4",
            "verification_required": risk != "R0",
            "direct_main_write_allowed": False,
        },
        "git": {
            "branch_required": True,
            "pull_request_required": True,
            "self_merge_allowed": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a deterministic JEV execution plan.")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--triggers", default="")
    parser.add_argument("--flags", default="")
    args = parser.parse_args()

    triggers = {x.strip() for x in args.triggers.split(",") if x.strip()}
    flags = {x.strip() for x in args.flags.split(",") if x.strip()}

    print(json.dumps(build_plan(args.task_id, triggers, flags), indent=2))


if __name__ == "__main__":
    main()
