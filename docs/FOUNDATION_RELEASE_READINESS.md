# JEV Adaptive Foundation Release Readiness

## Purpose


This document defines readiness of `base-skills_klever` v8 Adaptive Foundation for consumption by `jev-platform`.

`FND-032` remains the historical v7 release gate. The current release gate is **FND-070**.

## Closure status

As of 2026-10-05:

- `FND-070` is **DONE** after explicit operator approval.
- `PLT-001` documentation refresh is **DONE**.
- Adaptive Foundation validators/tests/release checks passed before promotion.
- PR #2 was merged into protected canonical `main` at merge commit `7dc4954fd87ce62702a2c606621d6e9142d23625`.
- `main` is the official JEV Foundation v8 branch.
- Historical branches `jev-v7-foundation` and `jev-v8-adaptive-foundation` are no longer active development branches.
- No `jev-platform` implementation work was started as part of this Foundation closure.

## Required capabilities

Before FND-070 can be accepted, Foundation must have green evidence for:

- skills 22–31, 47–49, 51–59 and 91–92;
- typed IntentBrief, AcceptanceContract, ExecutionBlueprint, ContextPack, PlanRevision, DecisionRecord, LearningCandidate, CounterfactualEvalReport and HygieneReport contracts;
- adaptive workflow compilation and bounded context retrieval;
- versioned plan mutation and stale-plan protection;
- role/capability separation and harness capability blocking;
- artifact review bound to exact revisions;
- living-document impact and end-to-end Requirement Graph;
- append-only/scoped decision provenance;
- skill-health and evidence-based learning;
- versioned replay corpus and counterfactual evaluation;
- supervised self-improvement with human approval, canary and rollback;
- repository hygiene, duplicate/reuse, cleanup evidence and cleanup-debt gates;
- adaptive risk minimums;
- independent Verifier evidence for runtime, trace, hygiene and adversarial review;
- Integrator enforcement of approved blueprint revision and exact promotion scope;
- positive/negative tests and deterministic end-to-end scenarios;
- documentation/manifest/backlog alignment.

## Deliberately Platform-only

Foundation does not claim real external execution for providers, GitHub App, Docker/VM workers, PostgreSQL, queues, hosting, browser/database collectors, Telegram/WhatsApp, image providers, production deployment or dashboard UI. Harness profiles are conservative contracts; active Platform adapters must declare actual runtime capability.

## Release invariant

FND-070 may be marked DONE only when:

1. every FND-033..FND-069 task is DONE;
2. CI/validators/tests are green;
3. no unexplained P0/P1 repository-hygiene debt remains;
4. self-improvement safety regressions are proven to block;
5. documentation is aligned to v8;
6. the operator explicitly accepts the Adaptive Foundation for the subsequent PRD/SPEC/ROADMAP refresh.

The release invariant is satisfied. `PLT-001` is DONE; subsequent Platform implementation remains a separate controlled phase.
