from __future__ import annotations

import pathlib
import re
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
manifest = yaml.safe_load((ROOT / "skills-manifest.yaml").read_text(encoding="utf-8"))

errors: list[str] = []
seen: set[str] = set()

for item in manifest.get("skills", []):
    sid = item.get("id")
    path = ROOT / item.get("path", "")

    if sid in seen:
        errors.append(f"duplicate skill id: {sid}")
    seen.add(sid)

    if not path.is_file():
        errors.append(f"missing skill file: {path.relative_to(ROOT)}")
        continue

    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append(f"missing frontmatter: {path.relative_to(ROOT)}")
        continue

    frontmatter = yaml.safe_load(match.group(1)) or {}
    if not frontmatter.get("name") or not frontmatter.get("description"):
        errors.append(f"incomplete frontmatter: {path.relative_to(ROOT)}")

for required in (
    "skill-priority",
    "preflight-check",
    "git-workflow-versioning",
    "ci-quality-gates",
    "code-review-quality-gates",
):
    if required not in seen:
        errors.append(f"required skill absent from manifest: {required}")

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)

print(f"OK: validated {len(seen)} manifest skills")
