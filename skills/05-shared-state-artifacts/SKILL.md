---
name: shared-state-artifacts
description: Estado compartido y artefactos fuente de verdad para evitar duplicación, loops y decisiones inconsistentes.
---

## Purpose
Proporcionar una única fuente de verdad para el plan, estado, decisiones y progreso entre múltiples agentes.

## Non-negotiables
- El estado compartido reside en `docs/orchestration/`.
- Los agentes deben leer el estado compartido antes de actuar.
- Los agentes deben actualizar el estado compartido tras completar su rol.

## Stop conditions
- Si el estado compartido falta o está obsoleto: detenerse y regenerar/actualizar antes de continuar.
- Si dos agentes discrepan en un contrato (OpenAPI/DB/i18n): detenerse y requerir resolución del Integrador registrada en `DECISIONS.md`.

## Required Output
- `docs/orchestration/STATE.md` (o STATE.json) con:
  - Fase actual (Plan / Implement / Integrate / Verify / Release).
  - Contratos: Ubicación OpenAPI, esquema Prisma, lista de locales i18n.
  - Roles asignados.
  - Tareas actuales y estado.
- `docs/orchestration/DECISIONS.md` para resoluciones de conflictos y decisiones arquitectónicas.

## Verification
- El archivo de estado existe y se actualiza tras completar cada rol.
- Las decisiones se registran cuando ocurren conflictos.
