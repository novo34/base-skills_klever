---
name: plan-mutation-and-replanning
description: Permite revisar un ExecutionBlueprint sin perder trazabilidad, seguridad ni validez del DAG.
---

## Purpose
Adaptar el plan cuando aparecen hechos nuevos sin improvisar cambios invisibles durante la ejecución.

## Non-negotiables
- Toda mutación crea una nueva revision; nunca reescribe el historial.
- Registrar actor, razón, evidencia e impactos.
- Revalidar dependencias, locks, riesgo, presupuesto, evidencia y aprobaciones.
- No continuar ejecución con un blueprint obsoleto.
- Mutaciones de alto impacto requieren la aprobación que corresponda por política.

## Allowed operations
- INSERT
- SPLIT
- REORDER
- BLOCK
- REPLACE
- REMOVE

## Required Output
Producir PlanRevision con:
- revision_id
- blueprint_id
- from_revision
- to_revision
- actor
- reason
- evidence[]
- operations[]
- dependency_impact[]
- risk_impact
- budget_impact

## Stop conditions
- La nueva revisión introduce ciclos.
- Se elimina un paso que cubre un requisito sin reemplazo equivalente.
- Se omite evidencia/gate obligatorio.
- No existe una razón/evidencia para la mutación.

## Verification
- El DAG revisado es válido.
- La cobertura requisito -> paso -> evidencia permanece completa.
- La revisión anterior sigue disponible.
