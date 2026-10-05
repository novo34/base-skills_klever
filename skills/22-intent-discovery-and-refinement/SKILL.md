---
name: intent-discovery-and-refinement
description: Convierte una petición humana en una intención explícita, acotada y ejecutable antes de planificar o modificar código.
---

## Purpose
Evitar que una petición ambigua, incompleta o aparentemente simple se convierta directamente en implementación sin entender objetivo, alcance, impacto y evidencia necesaria.

## Non-negotiables
- Investigar primero el contexto disponible del proyecto/repositorio antes de preguntar o asumir.
- Separar hechos observados, intención inferida, supuestos y preguntas abiertas.
- No ampliar el alcance más allá de lo pedido sin una razón explícita y trazable.
- La profundidad documental y de ejecución debe ser proporcional a ambigüedad, riesgo y radio de cambio.
- Una ambigüedad material o un objetivo contradictorio bloquea la ejecución hasta ser resuelto.

## Intent depth
- L0 DIRECT_CHANGE: cambio local, reversible y claramente definido.
- L1 ACCEPTANCE_BRIEF: requiere criterios de aceptación breves.
- L2 TASK_SPEC: afecta varias superficies o contiene reglas no triviales.
- L3 SPEC_CHANGE: modifica arquitectura, contratos o requisitos existentes.
- L4 PRODUCT_CHANGE: modifica producto, modelo operativo o múltiples requisitos/roadmap.

## Required Output
Producir un IntentBrief machine-readable con:
- goal
- requested_change
- in_scope
- out_of_scope
- observed_context
- assumptions
- open_questions
- ambiguity_score
- change_radius
- risk_signals
- documentation_depth
- clarification_required
- evidence_needed

## Stop conditions
- Objetivo incompatible con políticas o decisiones bloqueadas.
- No puede determinarse el recurso/proyecto objetivo.
- Existen interpretaciones materialmente distintas con efectos diferentes.
- Falta una decisión humana requerida por política.

## Verification
- Cada supuesto está marcado como supuesto, no como hecho.
- El alcance es consistente con la petición original.
- La profundidad seleccionada está justificada.
- Ninguna implementación comienza si clarification_required=true.
