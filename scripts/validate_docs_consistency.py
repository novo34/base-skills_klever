from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

canonical = {
    "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
    "foundation": (ROOT / "docs" / "JEV_V7_FOUNDATION.md").read_text(encoding="utf-8"),
    "execution": (ROOT / "docs" / "JEV_EXECUTION_FLOW.md").read_text(encoding="utf-8"),
    "human": (ROOT / "docs" / "HUMAN_STAGING_APPROVAL_FLOW.md").read_text(encoding="utf-8"),
    "staging": (ROOT / "staging" / "README.md").read_text(encoding="utf-8"),
    "multiagent": (ROOT / "agents_runtime" / "MULTIAGENT.md").read_text(encoding="utf-8"),
}

errors: list[str] = []

for name, text in canonical.items():
    if "v6.0" in text or "Ultimate Swarm Layer" in text:
        errors.append(f"{name}: obsolete v6 wording remains")

execution = canonical["execution"]
if "Human approval is required for every merge to production" not in execution:
    errors.append("execution: production merge human-approval rule missing")

if "`VERIFIED` → `STAGING`" not in execution:
    errors.append("execution: VERIFIED must flow to STAGING")

if "`VERIFIED` means" not in canonical["README.md"]:
    errors.append("README: VERIFIED semantics not explicit")

if "does **not** mean the task is approved for production" not in canonical["README.md"]:
    errors.append("README: VERIFIED must not imply production approval")

if "never promotes the complete staging branch" not in canonical["human"]:
    errors.append("human flow: selective promotion rule missing")

if "Verifier does not repair the code it reviews" not in canonical["multiagent"]:
    errors.append("multiagent: verifier independence wording missing")

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)

print("OK: canonical documentation is consistent with JEV v7 lifecycle and approval policy")
