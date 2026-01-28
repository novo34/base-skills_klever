---
name: skill-priority
description: Define el orden de resolución de conflictos entre skills para garantizar seguridad y estabilidad operacional.
---

## Purpose
Establecer una jerarquía clara de cumplimiento para evitar ambigüedades, loops e inestabilidad en ejecuciones complejas.

## Non-negotiables
- **Regla Maestra v4.1**: La orquestación y el rendimiento NUNCA anulan las reglas de idempotencia, aislamiento de datos o limpieza.
- El orden de prioridad es absoluto. Seguridad/Datos > Estabilidad Ops > Orquestación > Dev.

## Conflict resolution rule
- Si dos skills entran en conflicto, sigue la de mayor prioridad.
- En conflictos de v4.1, la seguridad/privacidad ganan siempre; luego gobierna la estabilidad operacional.

## Priority order (highest wins)
1. data-classification (24)
2. retention-dsar (25)
3. multi-tenant-data-isolation (09)
4. auth-security (13)
5. request-security (14)
6. logging-security (15)
7. idempotency-and-retry-control (07)
8. artifact-lifecycle-and-cleanup (08)
9. orchestration-protocol (03)
10. handoff-contracts (04)
11. shared-state-artifacts (05)
12. parallel-work-conflict-avoidance (06)
13. core-behavior (02)
14. stack-standards-nextjs (10)
15. db-migrations-safety (30)
16. backend-api-contracts (40)
17. frontend-nextjs-architecture (50)
18. ui-ux-modern-system (60)
19. i18n-next-intl (70)
20. performance-budgets (22)
21. code-review-quality-gates (80)
22. deployment-strategy (16)
23. recovery-rollback (17)

## Required Output
- Confirmación de cumplimiento de jerarquía v4.1.

## Verification
- Validación del Integrador sobre el respeto a las protecciones de aislamiento e idempotencia.
