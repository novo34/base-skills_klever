from __future__ import annotations

import json
import pathlib
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED_HARNESSES = ("claude-code.yaml", "codex.yaml", "cursor.yaml")
REQUIRED_SCHEMAS = (
    "capability-composition.schema.json",
    "harness-capability-contract.schema.json",
    "artifact-review.schema.json",
    "documentation-impact.schema.json",
    "decision-record.schema.json",
    "requirement-graph.schema.json",
)


def main() -> None:
    errors: list[str] = []

    for name in REQUIRED_HARNESSES:
        path = ROOT / "harnesses" / name
        if not path.is_file():
            errors.append(f"missing harness contract: {name}")
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for key in (
            "harness",
            "version",
            "capabilities",
            "limitations",
            "supports_browser",
            "supports_tools",
            "supports_structured_output",
        ):
            if key not in data:
                errors.append(f"{name}: missing field {key}")
        if not isinstance(data.get("capabilities"), list):
            errors.append(f"{name}: capabilities must be list")
        if not isinstance(data.get("limitations"), list):
            errors.append(f"{name}: limitations must be list")

    for name in REQUIRED_SCHEMAS:
        path = ROOT / "schemas" / name
        if not path.is_file():
            errors.append(f"missing governance schema: {name}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid governance schema {name}: {exc}")
            continue
        if data.get("type") != "object":
            errors.append(f"{name}: root must be object")
        if not data.get("required"):
            errors.append(f"{name}: required fields missing")
        if data.get("additionalProperties") is not False:
            errors.append(f"{name}: root additionalProperties must be false")

    readme = ROOT / "harnesses" / "README.md"
    if not readme.is_file():
        errors.append("harnesses README missing")
    else:
        text = readme.read_text(encoding="utf-8")
        for phrase in (
            "JEV core owns policy",
            "typed unsupported/blocking result",
            "No harness prompt may weaken",
        ):
            if phrase not in text:
                errors.append(f"harnesses README missing boundary statement: {phrase}")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        sys.exit(1)

    print("OK: adaptive governance and harness contracts are structurally valid")


if __name__ == "__main__":
    main()
