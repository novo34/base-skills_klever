---
name: skill-health-and-stocktake
description: Evalúa salud, utilidad, solapamiento, coste y regresiones de skills con evidencia.
---

## Purpose
Evitar acumulación de skills redundantes, obsoletas o contraproducentes y convertir su mantenimiento en una disciplina medible.

## Non-negotiables
- Métricas no equivalen automáticamente a autoridad de modificación.
- Una skill no se retira por baja frecuencia si cubre un riesgo crítico.
- Diferenciar activación correcta, falsa activación y activación omitida.
- Conservar benchmark, coste, latencia, correcciones, fallos del verifier y freshness.
- KEEP, IMPROVE, MERGE, RETIRE y DEFER requieren rationale y evidencia.

## Required Output
Producir SkillHealthReport con:
- skill_id
- activation_count
- successful_activations
- false_activations
- missed_activations
- verifier_failure_rate
- correction_rate
- average_cost
- average_latency_ms
- overlap_score
- freshness
- benchmark_status
- recommendation
- evidence[]

## Stop conditions
- Métricas insuficientes para una recomendación irreversible.
- Se intenta retirar una skill crítica sin evaluación de cobertura sustituta.
- La evidencia mezcla proyectos/scopes incompatibles.

## Verification
- Las métricas son reproducibles desde eventos/evals.
- La recomendación no autoaplica cambios.
- MERGE identifica explícitamente el destino propuesto.
