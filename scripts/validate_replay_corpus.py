from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CORPUS = ROOT / "evals" / "replay-corpus.v1.json"

errors: list[str] = []

if not CORPUS.is_file():
    errors.append("replay corpus missing")
else:
    try:
        data = json.loads(CORPUS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid replay corpus JSON: {exc}")
        data = {}

    if data.get("corpus_version") != "v1":
        errors.append("unexpected replay corpus version")
    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        errors.append("replay corpus must contain scenarios")
    else:
        ids = []
        for scenario in scenarios:
            sid = scenario.get("scenario_id")
            ids.append(sid)
            for key in ("scenario_id", "description", "input", "expected_safety", "expected_quality"):
                if key not in scenario:
                    errors.append(f"{sid or '<unknown>'}: missing {key}")
            if not scenario.get("expected_safety"):
                errors.append(f"{sid}: expected_safety must not be empty")
            if not scenario.get("expected_quality"):
                errors.append(f"{sid}: expected_quality must not be empty")
        if len(ids) != len(set(ids)):
            errors.append("duplicate replay scenario id")
        if any(not isinstance(sid, str) or not sid for sid in ids):
            errors.append("invalid replay scenario id")

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)

print(f"OK: replay corpus v1 is deterministic and contains {len(data['scenarios'])} scenarios")
