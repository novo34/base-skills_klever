---
name: skill-priority
description: Define el orden de resolución de conflictos entre skills para garantizar seguridad y legalidad.
---

## Purpose
Establecer una jerarquía clara de cumplimiento para evitar ambigüedades cuando dos o más reglas entran en conflicto.

## Non-negotiables
- El orden de prioridad es absoluto y debe respetarse sin excepciones.
- Las skills de mayor prioridad anulan cualquier regla contradictoria de una skill de menor prioridad.

## Conflict resolution rule
- Si dos skills entran en conflicto, sigue la skill de mayor prioridad.
- Las skills de menor prioridad solo se aplican cuando no contradicen las reglas de mayor prioridad.

## Priority order (highest wins)
1. data-classification (20)
2. retention-dsar (21)
3. auth-security (10)
4. request-security (11)
5. logging-security (12)
6. core-behavior (02)
7. stack-standards-nextjs (03)
8. db-migrations-safety (30)
9. backend-api-contracts (40)
10. frontend-nextjs-architecture (50)
11. ui-ux-modern-system (60)
12. i18n-next-intl (70)
13. performance-budgets (16)
14. code-review-quality-gates (80)
15. deployment-strategy (06)
16. recovery-rollback (07)

## Required Output
- Confirmación de que las reglas aplicadas respetan la jerarquía de prioridad.

## Verification
- Revisión manual por parte del agente antes de cada commit para asegurar que no se han violado prioridades superiores.
