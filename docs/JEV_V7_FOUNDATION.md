# JEV v7 Foundation

This branch converts the Klever skills constitution into a machine-consumable foundation for JEV.

## Architectural rule

Models do not govern JEV. JEV governs models.

LLM providers are replaceable workers. Governance, permissions, task state, budgets, verification and Git history remain in JEV and GitHub.

## First implementation blocks

1. Add a complete machine-readable skills manifest.
2. Add schemas for skills, agents, tasks, decisions and handoffs.
3. Add an Agent Registry.
4. Add a Skills Resolver.
5. Add a Risk Engine with R0-R4 levels.
6. Add PRD/SPEC requirement traceability.
7. Add GitHub Engine.
8. Add isolated execution workspaces.
9. Add Model Router.
10. Add Verification Agent and human approval gates.

## Safety invariant

No autonomous agent may write directly to `main`, merge its own work, deploy to production, execute destructive data changes, or promote persistent memory without the required gate.
