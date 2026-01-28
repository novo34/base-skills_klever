---
name: shared-state-artifacts
description: Fuente de verdad única para el estado del proyecto y agentes.
---

## Purpose
Asegurar que todos los agentes tengan la misma visión del plan, decisiones y progreso.

## Non-negotiables
- El estado reside en `/docs/orchestration/`.
- Los agentes DEBEN leer el estado antes de actuar y actualizarlo al terminar.

## Stop conditions
- Estado compartido ausente o desactualizado.

## Required Output
- `STATE.md` (o JSON) actualizado.
- `DECISIONS.md` para resoluciones de conflictos.

## Verification
- El archivo de estado refleja la realidad del repositorio.
