---
name: skill-priority
description: Define el orden de resolución de conflictos entre skills para garantizar seguridad y gobernanza.
---

## Purpose
Establecer una jerarquía clara de cumplimiento para evitar ambigüedades cuando múltiples agentes trabajan en paralelo y las reglas entran en conflicto.

## Non-negotiables
- El orden de prioridad es absoluto.
- **Regla Maestra v4.0**: En caso de conflicto, Seguridad y Privacidad siempre ganan; después gobierna Orchestration sobre el desarrollo.
- Los agentes de menor prioridad no pueden contradecir reglas de mayor prioridad.

## Conflict resolution rule
- Si dos skills entran en conflicto, sigue la skill de mayor prioridad.
- Multi-agent orchestration jamás puede anular las skills de Safety/Privacy.
- Las skills de desarrollo (Backend, Frontend) aplican solo si no contradicen Orchestration o Safety.

## Priority order (highest wins)
1. data-classification (21)
2. retention-dsar (22)
3. auth-security (10)
4. request-security (11)
5. logging-security (12)
6. orchestration-protocol (03)
7. handoff-contracts (04)
8. shared-state-artifacts (05)
9. parallel-work-conflict-avoidance (06)
10. core-behavior (02)
11. stack-standards-nextjs (07)
12. db-migrations-safety (30)
13. backend-api-contracts (40)
14. frontend-nextjs-architecture (50)
15. ui-ux-modern-system (60)
16. i18n-next-intl (70)
17. performance-budgets (19)
18. code-review-quality-gates (80)
19. deployment-strategy (13)
20. recovery-rollback (14)

## Required Output
- Confirmación de que el plan multi-agente respeta la jerarquía de seguridad.

## Verification
- Revisión cruzada de estados compartidos en `docs/orchestration/` contra reglas de prioridad.
