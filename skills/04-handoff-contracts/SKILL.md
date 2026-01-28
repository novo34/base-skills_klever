---
name: handoff-contracts
description: Contratos de traspaso entre agentes: entradas/salidas, formato fijo, y criterios de aceptación por módulo.
---

## Purpose
Prevenir la ambigüedad y el retrabajo estandarizando los traspasos (handoffs) entre agentes con una estructura determinante.

## Non-negotiables
- Cada rol debe producir una sección de handoff usando la plantilla obligatoria.
- Los handoffs deben declarar archivos tocados, contratos impactados (DB/OpenAPI/i18n) y pasos de verificación.
- Ningún agente puede implementar cambios fuera de su límite de rol asignado.

## Stop conditions
- Si un rol no puede producir los artefactos requeridos (ej. actualización OpenAPI): detenerse y escalar al Integrador.
- Si un agente toca archivos fuera de su scope: detenerse y revertir/evitar el cambio.

## Required Output
Añadir a `docs/orchestration/HANDOFFS.md` usando esta plantilla exacta:

### HANDOFF: <ROLE> -> Integrator
- Summary:
- Files touched:
- Contracts changed:
  - OpenAPI:
  - DB/Prisma:
  - i18n keys:
- Risks:
- Verification:
- Ready-to-merge checklist:
  - [ ] Lint
  - [ ] Typecheck
  - [ ] Tests
  - [ ] Build
  - [ ] OpenAPI synced
  - [ ] i18n synced

## Verification
- Cada rol produce un handoff válido.
- El Integrador realiza el merge solo tras satisfacer el checklist.
