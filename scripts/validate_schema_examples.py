from __future__ import annotations

import json
import pathlib
import sys

from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "adaptive"
SCHEMAS = ROOT / "schemas"


def validate_examples(root: pathlib.Path = ROOT) -> list[str]:
    errors: list[str] = []
    examples_dir = root / "examples" / "adaptive"
    schemas_dir = root / "schemas"

    if not examples_dir.is_dir():
        return ["adaptive examples directory missing"]

    for example_path in sorted(examples_dir.glob("*.json")):
        try:
            wrapper = json.loads(example_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{example_path.name}: invalid JSON: {exc}")
            continue

        schema_name = wrapper.get("schema")
        payload = wrapper.get("payload")
        if not schema_name or not isinstance(payload, dict):
            errors.append(f"{example_path.name}: requires schema + object payload")
            continue

        schema_path = schemas_dir / schema_name
        if not schema_path.is_file():
            errors.append(f"{example_path.name}: schema not found: {schema_name}")
            continue

        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        failures = sorted(validator.iter_errors(payload), key=lambda item: list(item.path))
        for failure in failures:
            path = ".".join(str(part) for part in failure.path) or "<root>"
            errors.append(
                f"{example_path.name}:{path}: {failure.message}"
            )

    return errors


def main() -> None:
    errors = validate_examples()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        sys.exit(1)
    count = len(list(EXAMPLES.glob("*.json")))
    print(f"OK: validated {count} adaptive schema examples")


if __name__ == "__main__":
    main()
