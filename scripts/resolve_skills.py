from __future__ import annotations

import argparse
import json
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_manifest() -> dict:
    return yaml.safe_load((ROOT / "skills-manifest.yaml").read_text(encoding="utf-8")) or {}


def resolve_skills(triggers: set[str]) -> list[dict]:
    manifest = load_manifest()
    selected: list[dict] = []

    for skill in manifest.get("skills", []):
        skill_triggers = set(skill.get("triggers", []))
        if skill.get("mandatory") or "all" in skill_triggers or triggers.intersection(skill_triggers):
            selected.append(skill)

    selected.sort(key=lambda item: item.get("priority", 0), reverse=True)
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve JEV skills for a classified task.")
    parser.add_argument(
        "--triggers",
        required=True,
        help="Comma-separated task triggers, e.g. auth,api,implementation",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    triggers = {item.strip() for item in args.triggers.split(",") if item.strip()}
    resolved = resolve_skills(triggers)

    if args.json:
        print(json.dumps({
            "triggers": sorted(triggers),
            "skills": [
                {
                    "id": skill["id"],
                    "path": skill["path"],
                    "priority": skill["priority"],
                }
                for skill in resolved
            ],
        }, indent=2))
        return

    for skill in resolved:
        print(f'{skill["priority"]:>4}  {skill["id"]}  {skill["path"]}')


if __name__ == "__main__":
    main()
