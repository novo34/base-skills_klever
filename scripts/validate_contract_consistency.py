from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
errors: list[str] = []

# Runtime state machine
state_path = ROOT / "orchestrator" / "state_machine.py"
spec = importlib.util.spec_from_file_location("jev_state_machine", state_path)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)
runtime_states = set(module.ALLOWED)
for targets in module.ALLOWED.values():
    runtime_states.update(targets)

# Schemas
task_schema = json.loads((ROOT / "schemas" / "task.schema.json").read_text(encoding="utf-8"))
state_schema = json.loads((ROOT / "schemas" / "task-state-machine.schema.json").read_text(encoding="utf-8"))
decision_schema = json.loads((ROOT / "schemas" / "decision.schema.json").read_text(encoding="utf-8"))

task_states = set(task_schema["properties"]["status"]["enum"])
state_schema_states = set(state_schema["properties"]["state"]["enum"])

if runtime_states != task_states:
    errors.append(
        "task.schema state drift: "
        f"runtime_only={sorted(runtime_states - task_states)} "
        f"schema_only={sorted(task_states - runtime_states)}"
    )

if runtime_states != state_schema_states:
    errors.append(
        "task-state-machine schema drift: "
        f"runtime_only={sorted(runtime_states - state_schema_states)} "
        f"schema_only={sorted(state_schema_states - runtime_states)}"
    )

# Risk policy
risk_policy = yaml.safe_load(
    (ROOT / "policies" / "risk-levels.yaml").read_text(encoding="utf-8")
) or {}
policy_risks = set((risk_policy.get("levels") or {}).keys())
task_risks = set(task_schema["properties"]["risk"]["enum"])
state_risks = set(state_schema["properties"]["risk"]["enum"])
decision_risks = set(decision_schema["properties"]["risk"]["enum"])

for name, risks in {
    "task.schema": task_risks,
    "task-state-machine.schema": state_risks,
    "decision.schema": decision_risks,
}.items():
    if risks != policy_risks:
        errors.append(
            f"{name} risk drift: "
            f"policy_only={sorted(policy_risks - risks)} "
            f"schema_only={sorted(risks - policy_risks)}"
        )

# Canonical docs must mention every lifecycle state explicitly.
doc_text = (ROOT / "docs" / "JEV_EXECUTION_FLOW.md").read_text(encoding="utf-8")
missing_doc_states = sorted(state for state in runtime_states if state not in doc_text)
if missing_doc_states:
    errors.append(
        "canonical execution flow missing lifecycle states: "
        + ", ".join(missing_doc_states)
    )

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)

print(
    "OK: lifecycle and risk contracts aligned "
    f"({len(runtime_states)} states, {len(policy_risks)} risk levels)"
)
