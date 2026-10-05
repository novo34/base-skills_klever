from __future__ import annotations

import json
import pathlib
import re
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

SKILL_SCHEMA_MAP = {
    "22-intent-discovery-and-refinement": "intent-brief.schema.json",
    "23-spec-and-constraints": "acceptance-contract.schema.json",
    "24-planning-task-breakdown": "execution-blueprint.schema.json",
    "25-source-grounded-development": "source-grounding.schema.json",
    "26-incremental-test-driven-development": "tdd-evidence.schema.json",
    "27-debugging-error-recovery": "debugging-report.schema.json",
    "28-code-simplification": "simplification-report.schema.json",
    "29-context-engineering": "context-pack.schema.json",
    "30-browser-runtime-verification": "browser-runtime-evidence.schema.json",
    "31-adversarial-doubt-review": "adversarial-review.schema.json",
    "47-adaptive-workflow-compilation": "adaptive-workflow.schema.json",
    "48-plan-mutation-and-replanning": "plan-revision.schema.json",
    "49-context-budget-and-retrieval": "context-retrieval-plan.schema.json",
}

REQUIRED_SKILLS = [
    "22-intent-discovery-and-refinement",
    "23-spec-and-constraints",
    "24-planning-task-breakdown",
    "25-source-grounded-development",
    "26-incremental-test-driven-development",
    "27-debugging-error-recovery",
    "28-code-simplification",
    "29-context-engineering",
    "30-browser-runtime-verification",
    "31-adversarial-doubt-review",
    "47-adaptive-workflow-compilation",
    "48-plan-mutation-and-replanning",
    "49-context-budget-and-retrieval",
]

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Non-negotiables",
    "## Required Output",
    "## Stop conditions",
    "## Verification",
]


def main() -> None:
    errors: list[str] = []

    manifest = yaml.safe_load(
        (ROOT / "skills-manifest.yaml").read_text(encoding="utf-8")
    ) or {}
    by_id = {
        item.get("id"): item
        for item in manifest.get("skills", [])
        if item.get("id")
    }

    for skill_id in REQUIRED_SKILLS:
        expected_path = ROOT / "skills" / skill_id / "SKILL.md"
        item = by_id.get(skill_id)

        if item is None:
            errors.append(f"adaptive skill missing from manifest: {skill_id}")
            continue
        if item.get("path") != expected_path.relative_to(ROOT).as_posix():
            errors.append(f"adaptive skill path mismatch: {skill_id}")
        if not expected_path.is_file():
            errors.append(f"adaptive skill file missing: {skill_id}")
            continue

        text = expected_path.read_text(encoding="utf-8")
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not frontmatter_match:
            errors.append(f"adaptive skill missing frontmatter: {skill_id}")
        else:
            frontmatter = yaml.safe_load(frontmatter_match.group(1)) or {}
            if not frontmatter.get("name") or not frontmatter.get("description"):
                errors.append(f"adaptive skill incomplete frontmatter: {skill_id}")

        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{skill_id} missing required section: {section}")

    for skill_id, schema_name in SKILL_SCHEMA_MAP.items():
        schema_path = ROOT / "schemas" / schema_name
        if not schema_path.is_file():
            errors.append(f"{skill_id} required schema missing: {schema_name}")
            continue
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON schema {schema_name}: {exc}")
            continue
        if schema.get("type") != "object":
            errors.append(f"{schema_name} root must be object")
        if not schema.get("required"):
            errors.append(f"{schema_name} must declare required fields")
        if schema.get("additionalProperties") is not False:
            errors.append(f"{schema_name} must reject undeclared root properties")

    manifest_priorities = [
        by_id[skill_id].get("priority")
        for skill_id in REQUIRED_SKILLS
        if skill_id in by_id
    ]
    if len(set(manifest_priorities)) != len(manifest_priorities):
        errors.append("adaptive skills must have unique priorities")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        sys.exit(1)

    print(
        f"OK: {len(REQUIRED_SKILLS)} adaptive skills are registered, structurally complete, "
        f"and backed by {len(SKILL_SCHEMA_MAP)} typed output contracts"
    )


if __name__ == "__main__":
    main()
