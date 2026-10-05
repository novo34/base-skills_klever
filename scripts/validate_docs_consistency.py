from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

canonical = {
    "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
    "foundation": (ROOT / "docs" / "JEV_V8_ADAPTIVE_FOUNDATION.md").read_text(encoding="utf-8"),
    "execution": (ROOT / "docs" / "JEV_EXECUTION_FLOW.md").read_text(encoding="utf-8"),
    "readiness": (ROOT / "docs" / "FOUNDATION_RELEASE_READINESS.md").read_text(encoding="utf-8"),
    "backlog": (ROOT / "docs" / "JEV_MASTER_BACKLOG.md").read_text(encoding="utf-8"),
    "human": (ROOT / "docs" / "HUMAN_STAGING_APPROVAL_FLOW.md").read_text(encoding="utf-8"),
    "staging": (ROOT / "staging" / "README.md").read_text(encoding="utf-8"),
    "multiagent": (ROOT / "agents_runtime" / "MULTIAGENT.md").read_text(encoding="utf-8"),
}

errors: list[str] = []

for name, text in canonical.items():
    if "Ultimate Swarm Layer" in text:
        errors.append(f"{name}: obsolete swarm wording remains")

execution = canonical["execution"]
readme = canonical["README.md"]
foundation = canonical["foundation"]
readiness = canonical["readiness"]
backlog = canonical["backlog"]

required_execution = (
    "IntentBrief",
    "AcceptanceContract",
    "ContextPack",
    "ExecutionBlueprint",
    "AdaptiveWorkflow",
    "PlanRevision",
    "Human approval is required for every production merge",
    "whole staging branch is never promoted",
)
for phrase in required_execution:
    if phrase not in execution:
        errors.append(f"execution: missing adaptive statement: {phrase}")

for phrase in (
    "Models do not govern JEV. JEV governs models.",
    "FND-070",
    "91–92",
    "Role != capability.",
):
    if phrase not in readme:
        errors.append(f"README: missing v8 statement: {phrase}")

for phrase in (
    "FND-070",
    "Adaptive Foundation",
    "self-improvement",
    "Repository hygiene",
):
    if phrase not in foundation:
        errors.append(f"foundation: missing v8 statement: {phrase}")

if "FND-032" not in readiness or "historical v7" not in readiness:
    errors.append("readiness: FND-032 must be explicitly historical")
if "FND-070" not in readiness or "operator explicitly accepts" not in readiness:
    errors.append("readiness: adaptive final gate/operator acceptance missing")

if "FND-032" not in backlog or "does **not** authorize Platform development" not in backlog:
    errors.append("backlog docs: historical gate semantics missing")
if "PLT-001" not in backlog or "FND-070" not in backlog:
    errors.append("backlog docs: PLT-001/FND-070 dependency missing")

if "never promotes the complete staging branch" not in canonical["human"]:
    errors.append("human flow: selective promotion rule missing")

if "Verifier does not repair the code it reviews" not in canonical["multiagent"]:
    errors.append("multiagent: verifier independence wording missing")

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)

print("OK: canonical documentation is aligned with JEV v8 Adaptive Foundation")
