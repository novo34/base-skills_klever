---
name: skill-priority
description: Define el orden de resolución de conflictos entre skills para garantizar seguridad y autonomía gobernada.
---

## Purpose
Establecer una jerarquía clara de cumplimiento para evitar ambigüedades, loops e inestabilidad en ejecuciones autónomas complejas.

## Non-negotiables
- **Regla Maestra v5.0**: Ningún objetivo de autonomía, orquestación o rendimiento puede anular las reglas de ciclo de vida del agente, memoria, presupuestos o supervisión humana.
- El orden de prioridad es absoluto: Seguridad/Datos > Estabilidad Ops > Autonomía > Orquestación > Dev.

## Conflict resolution rule
- Si dos skills entran en conflicto, sigue la de mayor prioridad.
- En conflictos de v5.0, la seguridad y la supervisión humana ganan siempre.

## Priority order (highest wins)
1. data-classification (02)
2. retention-dsar (03)
3. multi-tenant-data-isolation (04)
4. auth-security (05)
5. request-security (06)
6. logging-security (07)
7. idempotency-and-retry-control (08)
8. artifact-lifecycle-and-cleanup (09)
9. agent-lifecycle-control (10)
10. checkpointing-and-state-snapshots (11)
11. agent-memory-governance (12)
12. autonomy-limits-and-budgets (13)
13. human-supervision-escalation (14)
14. reward-alignment-and-anti-gaming (15)
15. orchestration-protocol (16)
16. handoff-contracts (17)
17. shared-state-artifacts (18)
18. parallel-work-conflict-avoidance (19)
19. core-behavior (20)
20. stack-standards-nextjs (21)
21. db-migrations-safety (30)
22. backend-api-contracts (40)
...

## Required Output
- Confirmación de cumplimiento de jerarquía v5.0.

## Verification
- Auditoría del Workplan para asegurar que los límites de autonomía no violan prioridades de seguridad.
