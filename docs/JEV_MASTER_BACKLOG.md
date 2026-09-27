# JEV Master Backlog

This is the canonical execution backlog for JEV.

It exists to prevent scope loss and to distinguish clearly between:

- **FOUNDATION**: reusable rules, contracts, policy and deterministic reference behavior in `base-skills_klever`.
- **PLATFORM**: real application/runtime implementation in `jev-platform`.
- **BOTH**: a foundation contract plus a concrete platform implementation.

## Rules

1. No task may be marked DONE without meeting every acceptance criterion.
2. Dependencies must be DONE before a dependent task begins unless an explicit exception is recorded.
3. P0 tasks are release blockers.
4. `jev-platform` must not be modified until its PRD/SPEC/ROADMAP update task (PLT-001) is accepted.
5. "Contract exists" and "works against a real external service" are never treated as equivalent.
6. Staging is permanent per project; task workspaces are temporary.
7. Human approval is required for production merge.
8. A task approval promotes only the approved task/PR, never the entire staging branch.
9. Multimodal/channel work must flow through the same Control Layer, authorization, audit, verification and staging gates.

## Current milestone sequence

```
Foundation completion
  -> PRD/SPEC/ROADMAP update
  -> JEV Platform core
  -> GitHub + Workspace + Model providers
  -> Developer + Verifier
  -> Permanent staging
  -> Human approval
  -> Dashboard/Quality/Costs
  -> Multimodal/Channels
  -> Pilot repo
  -> Espacore
  -> Nuvurent
  -> JEV self-development
```

The machine-readable source is `backlog/jev-master-tasks.yaml`.
