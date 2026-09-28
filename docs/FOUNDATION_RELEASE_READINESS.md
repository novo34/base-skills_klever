# JEV Foundation Release Readiness

## Purpose

This document defines what it means for `base-skills_klever` to be ready for consumption by `jev-platform`.

The foundation is a governance/contract/reference implementation. It is **not** the deployed JEV product.

## Foundation capabilities completed

The foundation defines and tests:

- canonical task lifecycle with permanent staging and human review;
- risk levels R0-R4 and machine-validated contract consistency;
- skills manifest and agent skill references;
- Architect, Developer, Verifier and Integrator role contracts;
- structured edit plans and Developer delivery handoff, with protected Git internals and CI workflow paths;
- independent Verifier collectors and independence rules;
- multiagent DAG scheduling, locks, handoffs and explicit conflict resolution;
- GitHub guards preventing direct production writes;
- workspace isolation contracts;
- provider-neutral Model Gateway with retry, fallback, circuit breaker and mandatory budget guard;
- fail-closed budget enforcement when project policy is absent;
- mandatory server-side authorization and ActorContext for Control Layer execution;
- risk reclassification from actual changed file paths before pull-request review, including R4 classification for CI workflow/supply-chain changes;
- hard budget stops before paid model calls;
- project registry with multiple repositories and repository-specific environments;
- permanent staging provider contract with explicit allowlisted database/secret references;
- immutable staging-readiness evidence;
- approval linked to exact staging evidence and URL;
- selective promotion by approved task commit/migrations;
- append-only audit contracts;
- automatic notification routing;
- Quality Center trace ingestion;
- structured natural-language command interpretation with untrusted-input delimiters and anti-injection instructions;
- audited/confirmed budget control;
- multimodal intake for text, image, screenshot, file and link;
- visual reference roles (current/base, edit target, style reference, desired result, requirement document);
- Web/Telegram/WhatsApp channel-neutral ingress contracts requiring verified authentication and identity evidence;
- attachment-source validation that rejects unsafe schemes and local/private destinations, with runtime DNS/redirect revalidation and connection pinning required in the real platform; the real HTTP client must connect to the same validated/pinned address (or equivalent transport guarantee) to close DNS-rebinding TOCTOU;
- circuit breaker half-open recovery after a configurable reset timeout;
- mandatory manual staging review policy for visual changes;
- CI gates validating backlog, lifecycle/risk contracts, fail-closed security defaults, real PR/push changed-path risk classification, documentation, tests and smoke planning.

## Deliberately NOT claimed as implemented here

The following require the real `jev-platform` runtime and external credentials/infrastructure. Provider-specific foundation profiles exist for DeepSeek, OpenAI/Codex, Qwen and GLM, but the real API adapters remain platform work:

- real DeepSeek API adapter;
- real OpenAI/Codex API adapter;
- real Qwen API adapter;
- real GLM API adapter;
- GitHub App installation-token integration;
- real Docker/VM workspace workers and resource limits;
- PostgreSQL persistence;
- queue/worker infrastructure;
- real hosting deployment adapter (Dokploy/VPS/Vercel/etc.);
- real staging database provisioning;
- real browser/API/database collectors;
- real production deployment;
- real Telegram Bot API integration;
- real WhatsApp Business/Cloud API integration;
- real image generation/edit provider integration;
- dashboard/UI;
- production secrets management, backups and observability.

Those are PLATFORM implementation tasks. A foundation contract existing does not mean an external service is already operational.

## Release invariant

Before development of `jev-platform` starts:

1. all `FND-*` tasks except this release task must be DONE;
2. CI must be green;
3. limitations above must remain explicit;
4. PRD, SPEC and ROADMAP in `jev-platform` must be updated from the final foundation decisions;
5. `jev-platform` implementation must follow those updated documents.

## Repository boundary

`base-skills_klever` answers:

> What must JEV do, allow, forbid, record and verify?

`jev-platform` answers:

> How does the real deployed product execute those contracts using databases, workers, providers, GitHub, Docker, hosting and UI?

This separation is intentional and release-critical.
