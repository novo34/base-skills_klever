---
name: context-budget-and-retrieval
description: Recupera contexto en iteraciones acotadas respetando un presupuesto explícito.
---

## Purpose
Encontrar el contexto mínimo suficiente mediante ciclos dispatch -> evaluate -> refine en lugar de cargar información masiva por defecto.

## Non-negotiables
- Definir presupuesto y máximo de iteraciones antes de recuperar.
- Recuperar REQUIRED antes que OPTIONAL.
- Detener cuando el contexto crítico esté satisfecho.
- No ocultar contexto REQUIRED ausente.
- Toda expansión del presupuesto debe estar justificada.

## Required Output
Producir ContextRetrievalPlan con:
- task_id
- budget
- max_iterations
- required_queries[]
- optional_queries[]
- stop_when[]

Cada iteración debe registrar:
- query
- candidates
- selected
- missing_required
- next_refinement
- budget_used

## Stop conditions
- Se alcanza max_iterations con contexto REQUIRED ausente.
- El presupuesto se agotó sin autorización para ampliarlo.
- Fuentes críticas se contradicen.

## Verification
- El ContextPack final cabe en presupuesto o documenta la excepción.
- La recuperación termina por criterio explícito, no por agotamiento accidental.
- Provenance permite reconstruir cada inclusión.
