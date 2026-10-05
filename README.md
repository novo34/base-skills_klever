# Klever JEV Adaptive Skills Foundation (v8)

This repository is the reusable governance, execution-contract and adaptive-engineering foundation consumed by JEV.

It is **not the JEV application itself**. The persistent backend, dashboard, workers and real infrastructure integrations belong in `novo34/jev-platform`.

## Core principle

**Models do not govern JEV. JEV governs models.**

JEV core owns permissions, risk, task/workflow state, budgets, GitHub guards, isolated workspaces, independent verification, staging, human production approval, audit, requirement traceability and self-improvement gates.

## Adaptive engineering flow

```
Human intent
  -> IntentBrief
  -> AcceptanceContract
  -> ContextPack
  -> ExecutionBlueprint
  -> AdaptiveWorkflow
  -> isolated execution
  -> evidence + adversarial verification
  -> permanent staging
  -> explicit human decision
  -> selective production promotion
  -> learning candidates
  -> counterfactual evaluation
  -> supervised canary/rollback
```

The workflow depth is proportional to ambiguity, risk and change radius. Risk may always increase depth/gates; adaptive logic may never reduce mandatory safety controls.

## Canonical task lifecycle

```
PLANNED -> READY -> RUNNING -> VERIFYING -> VERIFIED
        -> STAGING -> AWAITING_HUMAN -> APPROVED -> DONE
```

Controlled alternatives include `BLOCKED`, `FAILED`, `CHANGES_REQUESTED` and `REJECTED`.

`VERIFIED` means independent technical verification passed. It does **not** mean production approval.

## Agent roles and capabilities

Authority roles remain intentionally small:

- Architect — intent/spec/architecture/blueprints/replanning.
- Developer — grounded implementation, TDD, debugging, simplification and cleanup.
- Verifier — independent runtime/adversarial/trace/hygiene verification.
- Integrator — integrates only the approved blueprint revision and exact promotion scope.

Technology/provider behavior is composed as capabilities. **Role != capability.** Capability composition cannot expand role permissions.

## Skills and contracts

`skills-manifest.yaml` is the machine-readable source of truth.

v8 adds the adaptive families:

- 22–31: intent, spec, planning, grounded development, TDD, debugging, simplification, context, browser verification and adversarial review.
- 47–49: adaptive workflow compilation, plan mutation and context retrieval budget.
- 51–54: skill health, evidence-based learning, improvement candidates and counterfactual evaluation.
- 55–58: capability composition, artifact review, living documentation and decision provenance.
- 59: supervised self-improvement canary/rollback.
- 91–92: repository hygiene/dead-code and duplication/reuse guard.

Critical outputs use typed schemas and runtime/test enforcement; they are not governed only by Markdown instructions.

## Repository hygiene

CI blocks obvious temporary/debug artifacts and exact duplicate code in guarded source areas unless an allowlist entry includes rationale and expiry. Uncertain/dynamic code is never auto-deleted. Refactors must account for added/replaced/removed surfaces and temporary artifacts created by the task.

## Harness boundary

Claude Code, Codex, Cursor and future harnesses are execution surfaces. They declare capabilities/limitations. JEV core retains policy, authorization, risk, audit, verification and approval.

## Release gates

`FND-032` is the historical v7 release gate.

The current Adaptive Foundation gate is **`FND-070`**. `jev-platform` PRD/SPEC/ROADMAP refresh (`PLT-001`) depends on FND-070.

## Master backlog

The canonical backlog is `backlog/jev-master-tasks.yaml`.

See:
- `docs/JEV_V8_ADAPTIVE_FOUNDATION.md`
- `docs/JEV_EXECUTION_FLOW.md`
- `docs/JEV_MASTER_BACKLOG.md`
- `docs/FOUNDATION_RELEASE_READINESS.md`
