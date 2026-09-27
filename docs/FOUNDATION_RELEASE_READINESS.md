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
- structured edit plans and Developer delivery handoff;
- independent Verifier collectors and independence rules;
- multiagent DAG scheduling, locks, handoffs and explicit conflict resolution;
- GitHub guards preventing direct production writes;
- workspace isolation contracts;
- provider-neutral Model Gateway with retry, fallback, circuit breaker and budget guard;
- hard budget stops before paid model calls;
- project registry with multiple repositories and repository-specific environments;
- permanent staging provider contract;
- immutable staging-readiness evidence;
- approval linked to exact staging evidence and URL;
- selective promotion by approved task commit/migrations;
- append-only audit contracts;
- automatic notification routing;
- Quality Center trace ingestion;
- structured natural-language command interpretation;
- audited/confirmed budget control;
- multimodal intake for text, image, screenshot, file and link;
- visual reference roles (current/base, edit target, style reference, desired result, requirement document);
- Web/Telegram/WhatsApp channel-neutral ingress contracts;
- mandatory manual staging review policy for visual changes;
- CI gates validating backlog, lifecycle/risk contracts, documentation, tests and smoke planning.

## Deliberately NOT claimed as implemented here

The following require the real `jev-platform` runtime and external credentials/infrastructure:

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

1. all FOUNDATION tasks except this release task must be DONE;
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
