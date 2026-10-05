# JEV v8 Adaptive Foundation

This branch evolves the v7 governance foundation into an adaptive engineering foundation while preserving all v7 safety invariants.

## Architectural rule

**Models do not govern JEV. JEV governs models.**

Models, providers and harnesses are replaceable workers. JEV core owns policy, authorization, risk, audit, workflow state, verification, staging and human approval.

## Adaptive architecture

The v8 Foundation defines contracts/reference behavior for:

1. Intent discovery with ambiguity, change radius and proportional documentation depth.
2. Acceptance contracts with observable verification criteria.
3. Execution Blueprints with dependency DAGs, parallel groups, capabilities, evidence, rollback and versioned plan revisions.
4. Source-grounded development, incremental TDD, debugging and behavior-preserving simplification.
5. Context Packs with explicit budgets and bounded iterative retrieval.
6. Browser/runtime verification and adversarial doubt review.
7. Adaptive workflow compilation that may increase depth from risk but never reduce mandatory gates.
8. Capability composition over stable authority roles.
9. Harness capability contracts that expose capabilities/limitations without duplicating JEV governance.
10. Artifact conversation/review with revision-bound explicit decisions.
11. Living-document governance and an end-to-end Requirement Graph.
12. Append-only decision provenance with scoped retrieval.
13. Skill health, evidence-based learning and improvement candidate generation.
14. Versioned replay corpus and counterfactual baseline-vs-candidate evaluation.
15. Supervised self-improvement using human approval, isolated canary, monitoring and proven rollback.
16. Repository hygiene, dead-code classification, duplicate/reuse guard, cleanup evidence and health debt metrics.

## Safety invariants

No adaptive workflow, learning process, skill or harness may:

- write directly to production branches;
- self-verify when independent verification is required;
- infer production approval from chat;
- promote an improvement without required human approval;
- weaken authorization, audit, risk, verifier independence or human-approval controls;
- silently execute a stale blueprint revision;
- expand promotion scope beyond the exact approved task/PR;
- delete uncertain/dynamic code solely because static references are absent;
- increase cleanup debt silently;
- rewrite historical decisions, plan revisions or evaluation corpus evidence.

## Foundation vs Platform

Foundation defines schemas, policies, reference runtimes, validators and tests.

The real deployed implementation remains in `novo34/jev-platform`: persistent storage, queues/workers, GitHub App, Docker/VM execution, real providers, real browser/database collectors, staging/deployment infrastructure and UI.

FND-032 remains the historical v7 release gate. The current Adaptive Foundation release gate is **FND-070**. Platform documentation/development stays blocked until FND-070 is accepted.
