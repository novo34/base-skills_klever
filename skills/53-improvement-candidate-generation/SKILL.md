---
name: improvement-candidate-generation
description: Genera propuestas de mejora de JEV a partir de fallos, correcciones, coste, solapamiento y capacidades ausentes.
---

## Purpose
Detectar mejoras de forma sistemática sin otorgar al sistema autoridad para autoaplicarlas.

## Non-negotiables
- Toda propuesta necesita evidencia y problema observable.
- Incluir beneficio esperado, riesgo, contratos afectados y rollback concept.
- Distinguir mejora de skill, runtime, policy, documentation, agent contract o tooling.
- No aplicar, promover ni editar controles críticos desde esta skill.
- Propuestas que debilitan seguridad/approval/audit se rechazan.

## Required Output
Producir ImprovementCandidate con:
- candidate_id
- problem
- evidence[]
- improvement_type
- proposed_change
- expected_benefit
- risk
- affected_contracts[]
- rollback_concept
- evaluation_plan
- status

## Stop conditions
- No existe evidencia del problema.
- La propuesta reduce un gate de seguridad.
- No puede definirse cómo medir el beneficio/regresión.

## Verification
- Cada propuesta puede evaluarse contra baseline.
- La propuesta permanece CANDIDATE hasta aprobación.
- No se confunde popularidad/frecuencia con mejora de calidad.
