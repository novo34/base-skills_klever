# Klever JEV Skills Foundation (v7)

This repository is the reusable governance and execution-contract foundation consumed by JEV.

It is **not the JEV application itself**. The JEV product, persistent backend, dashboard, workers and real infrastructure integrations belong in `novo34/jev-platform`.

## Core principle

**Models do not govern JEV. JEV governs models.**

AI providers are replaceable workers. JEV owns:

- permissions and risk policy
- task state and transitions
- skills and agent contracts
- budgets and hard stops
- GitHub guards
- workspace isolation contracts
- independent verification
- permanent staging policy
- human production approval
- audit and traceability

## Canonical task flow

```
PLANNED
  -> READY
  -> RUNNING
  -> VERIFYING
  -> VERIFIED
  -> STAGING
  -> AWAITING_HUMAN
  -> APPROVED
  -> DONE
```

Controlled alternate states include `BLOCKED`, `FAILED`, `CHANGES_REQUESTED`, and `REJECTED`.

`VERIFIED` means automated/independent technical verification passed. It does **not** mean the task is approved for production.

## Branch and staging model

- `main` = production
- `staging` = permanent online validation environment
- `feat/TASK-...` = task-specific development branch

Staging uses its own persistent non-production database. A human reviews the exact staging result before production merge.

Approval is task/PR-specific. JEV must never promote the complete staging branch to `main` simply because one task was approved.

## Human approval

Current policy requires human approval for every production merge.

Additional critical operations such as production deployment, destructive data changes and persistent-memory promotion are also human-gated.

## Agent roles

Initial roles:

- Architect — architecture, ADRs, workplans, risk assessment
- Developer — implementation in isolated task workspaces/branches
- Verifier — independent read-only verification
- Integrator — controlled integration and conflict resolution

The model/provider used by an agent is independent from the agent role.

## Skills

The machine-readable source of truth is `skills-manifest.yaml`.

Baseline mandatory skills include:

- `00-skill-priority`
- `01-preflight-check`
- `20-core-behavior`
- `36-git-workflow-versioning`
- `37-ci-quality-gates`
- `90-code-review-quality`

CI validates both the manifest and agent references to skills.

## Master backlog

The canonical backlog is:

`backlog/jev-master-tasks.yaml`

It distinguishes:

- `FOUNDATION` — contracts/policy/reference behavior in this repository
- `PLATFORM` — real application/infrastructure implementation in `jev-platform`
- `BOTH` — foundation contract plus platform implementation

A contract existing here never means the corresponding external integration is already running in production.

## CI

The foundation CI validates:

- skills and agent skill references
- canonical backlog integrity
- lifecycle/risk contract consistency
- pytest suite
- planning smoke test

See `docs/JEV_MASTER_BACKLOG.md` and `docs/JEV_EXECUTION_FLOW.md` for the canonical execution model.
