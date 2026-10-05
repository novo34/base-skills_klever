# JEV Master Backlog

The machine-readable canonical backlog is `backlog/jev-master-tasks.yaml`.

## Scope rules

- **FOUNDATION**: reusable governance, contracts, schemas, policies, reference runtimes, validators and tests in `base-skills_klever`.
- **PLATFORM**: real product/runtime implementation in `jev-platform`.

No task is DONE until every acceptance criterion is satisfied. Dependencies must be DONE before dependents begin unless a recorded exception exists.

## Current milestone sequence

```
Historical v7 Foundation (FND-032) ✅
  -> Adaptive Foundation expansion (FND-033..FND-069) ✅
  -> Adaptive release readiness (FND-070) ✅
  -> PRD/SPEC/ROADMAP refresh (PLT-001) ✅
  -> JEV Platform implementation (next controlled phase)
```

`FND-032` is historical and does **not** authorize Platform development. `FND-070` and `PLT-001` are complete. The canonical Foundation is protected `main`; Platform implementation starts only under its own task-control gates.

## Development Control Gate / NEXT_TASK

Platform execution is now controlled by the canonical backlog itself.

- PLATFORM declaration order is the execution order.
- The first PLATFORM task whose status is not `DONE` or `DEFERRED` is the only task that can become `NEXT_TASK`.
- A later task may not start simply because its dependencies happen to be satisfied.
- `BLOCKED` on the current task blocks progression; later tasks remain forbidden.
- At most one PLATFORM task may be `READY`, `IN_PROGRESS` or `VERIFYING`.
- Starting work requires explicit operator authorization for the exact resolved `NEXT_TASK`.
- New work discovered during implementation must be inserted into the backlog through PlanRevision/decision governance before implementation.
- From the control epoch after `PLT-001`, `DONE` requires completion evidence for every acceptance criterion plus independent `verified_by` metadata.
- Only `DONE` satisfies dependencies; `DEFERRED` does not silently unlock dependents.

Reference implementation: `scripts/development_control.py`, `scripts/next_task.py` and `scripts/validate_development_control.py`.

## Adaptive Foundation workstreams

- Intent/spec/planning: 22–24
- Grounded implementation and verification: 25–31
- Workflow/context adaptation: 47–49
- Skill health/learning/evaluation: 51–54
- Capability/artifact/docs/decision governance: 55–58
- Supervised self-improvement: 59
- Repository hygiene/reuse: 91–92
- Cross-cutting agent/risk/validator/E2E/docs integration: FND-065..069

## Non-negotiable backlog rules

1. Contract existence never means external integration is operational.
2. Human approval is required for production merge.
3. Approval is task/PR-specific; never promote all staging.
4. Adaptive workflows cannot reduce mandatory gates.
5. Learning/evolution cannot self-promote protected controls.
6. Repository cleanup never auto-deletes uncertain/dynamic code.
7. Platform work starts only from the next eligible Platform task after explicit operator authorization; completed Foundation/documentation gates are not reopened without a recorded PlanRevision/decision.
