from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
errors: list[str] = []


def load_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


state_module = load_module("jev_state_machine", ROOT / "orchestrator" / "state_machine.py")
control_module = load_module("jev_control_runtime", ROOT / "control" / "runtime.py")
command_module = load_module("jev_command_runtime", ROOT / "command_center" / "runtime.py")
orders_module = load_module("jev_orders_runtime", ROOT / "orders" / "runtime.py")
notifications_module = load_module("jev_notifications_runtime", ROOT / "notifications" / "runtime.py")

runtime_states = set(state_module.ALLOWED)
for targets in state_module.ALLOWED.values():
    runtime_states.update(targets)

task_schema = json.loads((ROOT / "schemas" / "task.schema.json").read_text(encoding="utf-8"))
state_schema = json.loads((ROOT / "schemas" / "task-state-machine.schema.json").read_text(encoding="utf-8"))
decision_schema = json.loads((ROOT / "schemas" / "decision.schema.json").read_text(encoding="utf-8"))
control_schema = json.loads((ROOT / "schemas" / "control-command.schema.json").read_text(encoding="utf-8"))
command_schema = json.loads((ROOT / "schemas" / "command-intent.schema.json").read_text(encoding="utf-8"))
order_schema = json.loads((ROOT / "schemas" / "work-order.schema.json").read_text(encoding="utf-8"))
notification_schema = json.loads((ROOT / "schemas" / "notification.schema.json").read_text(encoding="utf-8"))

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

runtime_actions = set(control_module.ALLOWED_ACTIONS)
control_actions = set(control_schema["properties"]["action"]["enum"])
command_actions = {
    item for item in command_schema["properties"]["action"]["enum"]
    if item is not None
}
supported_intents = set(command_module.SUPPORTED_INTENTS)

for name, actions in {
    "control-command.schema": control_actions,
    "command-intent.schema": command_actions,
    "command-center runtime": supported_intents,
}.items():
    if actions != runtime_actions:
        errors.append(
            f"{name} action drift: "
            f"runtime_only={sorted(runtime_actions - actions)} "
            f"contract_only={sorted(actions - runtime_actions)}"
        )

order_states = set(order_schema["properties"]["status"]["enum"])
if order_states != set(orders_module.ALLOWED_ORDER_STATES):
    errors.append(
        "work-order state drift: "
        f"runtime_only={sorted(set(orders_module.ALLOWED_ORDER_STATES) - order_states)} "
        f"schema_only={sorted(order_states - set(orders_module.ALLOWED_ORDER_STATES))}"
    )

runtime_priorities = {"LOW", "NORMAL", "HIGH", "URGENT"}
schema_priorities = set(order_schema["properties"]["priority"]["enum"])
if runtime_priorities != schema_priorities:
    errors.append("work-order priority drift")

runtime_work_types = {
    "GENERAL",
    "IMAGE_REPLACEMENT",
    "IMAGE_GENERATION",
    "IMAGE_EDIT",
    "UI_REFERENCE_REDESIGN",
}
schema_work_types = set(order_schema["properties"]["work_type"]["enum"])
if runtime_work_types != schema_work_types:
    errors.append("work-order type drift")

notification_categories = set(notification_schema["properties"]["category"]["enum"])
if notification_categories != set(notifications_module.ALLOWED_CATEGORIES):
    errors.append("notification category drift")

notification_severities = set(notification_schema["properties"]["severity"]["enum"])
if notification_severities != set(notifications_module.ALLOWED_SEVERITIES):
    errors.append("notification severity drift")

if "production_promoted" not in state_schema["properties"]:
    errors.append("task-state-machine schema missing production_promoted gate")

doc_text = (ROOT / "docs" / "JEV_EXECUTION_FLOW.md").read_text(encoding="utf-8")
missing_doc_states = sorted(state for state in runtime_states if state not in doc_text)
if missing_doc_states:
    errors.append(
        "canonical execution flow missing lifecycle states: "
        + ", ".join(missing_doc_states)
    )
if "production_promoted=true" not in doc_text:
    errors.append("canonical execution flow missing DONE production-promotion gate")

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)

print(
    "OK: lifecycle, risk, control, work-order and notification contracts aligned "
    f"({len(runtime_states)} states, {len(policy_risks)} risk levels, "
    f"{len(runtime_actions)} control actions)"
)
