# JEV v7 Foundation

This branch converts the Klever skills constitution into a machine-consumable foundation for JEV.

## Architectural rule

Models do not govern JEV. JEV governs models.

LLM providers are replaceable workers. Governance, permissions, task state, budgets, verification, staging policy and Git history remain under JEV control.

## Repository boundary

This repository defines reusable contracts, policies, schemas, reference runtimes and validation.

The real JEV application belongs in `novo34/jev-platform`, including PostgreSQL persistence, workers, real GitHub App integration, real Docker execution, hosting/staging integrations and the dashboard.

## Foundation blocks

The v7 foundation includes contracts/reference behavior for:

1. Skills manifest and resolver.
2. Agent contracts and registry.
3. Risk Engine with R0-R4 levels.
4. Task lifecycle and requirement traceability.
5. GitHub operation guards.
6. Isolated workspace contracts.
7. Model Gateway contracts, retry/fallback and budget gating.
8. Developer, Architect, Verifier and Integrator runtimes.
9. Verification evidence and reporting.
10. Permanent staging and selective promotion policy.
11. Human approval gates.
12. Audit, notifications, costs and reporting.
13. Control/API boundaries and role authorization.
14. Master backlog with CI validation.

## Canonical safety invariants

No autonomous agent may:

- write directly to `main` or `master`;
- approve or verify its own implementation where independence is required;
- merge to production without recorded human approval;
- bypass staging when staging is required;
- execute destructive data changes without the required human gate;
- access production credentials from development workspaces;
- exceed a configured hard budget limit;
- promote the entire staging branch merely because one task was approved.

`VERIFIED` is a technical state. Production acceptance requires staging review and explicit human approval.
