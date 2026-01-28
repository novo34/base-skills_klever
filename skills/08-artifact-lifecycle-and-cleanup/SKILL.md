---
name: artifact-lifecycle-and-cleanup
description: Control del ciclo de vida de artefactos generados por agentes para evitar acumulación y confusión.
---

## Purpose
Mantener un espacio de trabajo limpio y auditable definiendo la propiedad, la vida útil y las reglas de limpieza de los artefactos generados.

## Non-negotiables
- Todo artefacto generado debe tener:
  - Rol propietario (Owner).
  - Propósito.
  - Ciclo de vida (temporal / permanente).
- Los artefactos temporales deben ser limpiados o promocionados explícitamente.

## Stop conditions
- Si se genera un artefacto sin propiedad o ciclo de vida declarado, detenerse y documentarlo.
- Si artefactos obsoletos entran en conflicto con el estado actual, detenerse y limpiar antes de proceder.

## Required Output
Actualizar `docs/orchestration/STATE.md` con:
- Nombre del artefacto.
- Propietario.
- Ciclo de vida.
- Estado (activo / depurado / eliminado).
Plan de limpieza para artefactos obsoletos.

## Verification
- No quedan artefactos no utilizados o ambiguos tras completar la tarea.
- El estado del repositorio es explicable y mínimo.
