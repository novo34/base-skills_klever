---
name: handoff-contracts
description: Contratos de traspaso estandarizados entre agentes.
---

## Purpose
Prevenir ambigüedades en la entrega de tareas entre agentes paralelos.

## Non-negotiables
- Uso obligatorio de la plantilla de handoff para cada rol completado.
- Declarar explícitamente la idempotencia y el ciclo de vida de los entregables.

## Stop conditions
- Handoff sin checklist de verificación (lint, typecheck, etc.) completado.

## Required Output
- Entrada registrada en `docs/orchestration/HANDOFFS.md`.

## Verification
- El Integrador valida el handoff antes del merge.
