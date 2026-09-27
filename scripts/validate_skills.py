from __future__ import annotations

import pathlib
import re
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
manifest_path = ROOT / "skills-manifest.yaml"
manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}

errors: list[str] = []
seen_ids: set[str] = set()
seen_paths: set[str] = set()

manifest_skills = manifest.get("skills", [])
repo_skills = sorted(
    p.relative_to(ROOT).as_posix()
    for p in (ROOT / "skills").glob("*/SKILL.md")
)

for item in manifest_skills:
    sid = item.get("id")
    rel_path = item.get("path", "")
    path = ROOT / rel_path

    if not sid:
        errors.append("manifest skill without id")
        continue
    if sid in seen_ids:
        errors.append(f"duplicate skill id: {sid}")
    seen_ids.add(sid)

    if rel_path in seen_paths:
        errors.append(f"duplicate skill path: {rel_path}")
    seen_paths.add(rel_path)

    if not path.is_file():
        errors.append(f"missing skill file: {rel_path}")
        continue

    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append(f"missing frontmatter: {rel_path}")
        continue

    frontmatter = yaml.safe_load(match.group(1)) or {}
    if not frontmatter.get("name") or not frontmatter.get("description"):
        errors.append(f"incomplete frontmatter: {rel_path}")

manifest_paths = sorted(seen_paths)
if manifest_paths != repo_skills:
    missing = sorted(set(repo_skills) - set(manifest_paths))
    extra = sorted(set(manifest_paths) - set(repo_skills))
    if missing:
        errors.append("skills missing from manifest: " + ", ".join(missing))
    if extra:
        errors.append("manifest paths without SKILL.md: " + ", ".join(extra))

priorities = [item.get("priority") for item in manifest_skills]
if any(not isinstance(p, int) for p in priorities):
    errors.append("every skill must have an integer priority")

mandatory_ids = {
    "00-skill-priority",
    "01-preflight-check",
    "20-core-behavior",
    "36-git-workflow-versioning",
    "37-ci-quality-gates",
    "90-code-review-quality",
}
for required in mandatory_ids:
    item = next((x for x in manifest_skills if x.get("id") == required), None)
    if not item or not item.get("mandatory"):
        errors.append(f"mandatory baseline skill missing or not mandatory: {required}")

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)

print(f"OK: validated {len(manifest_skills)} skills; manifest fully covers repository")


# Validate agent contracts reference real manifest skill IDs.
agent_dir = ROOT / "agents"
for agent_path in sorted(agent_dir.glob("*.yaml")):
    if agent_path.name == "registry.yaml":
        continue
    agent = yaml.safe_load(agent_path.read_text(encoding="utf-8")) or {}
    mandatory = ((agent.get("skills") or {}).get("mandatory") or [])
    for skill_id in mandatory:
        if skill_id not in seen_ids:
            errors.append(
                f"agent {agent_path.name} references unknown skill id: {skill_id}"
            )
