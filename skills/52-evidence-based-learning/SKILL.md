---
name: evidence-based-learning
description: Convierte observaciones repetidas en candidatos de aprendizaje versionados, acotados y supervisados.
---

## Purpose
Permitir aprendizaje útil sin convertir cada sesión o corrección en una regla global insegura.

## Non-negotiables
- Separar OBSERVATION, HYPOTHESIS, PATTERN, PROJECT_RULE, GLOBAL_RULE, SKILL_CANDIDATE y POLICY_CANDIDATE.
- Todo candidato registra scope, confidence, evidence y contradictions.
- Contradicciones reducen confianza y nunca se silencian.
- Ningún candidato global se activa sin evaluación y aprobación requerida.
- Memoria/aprendizaje permanece reversible y versionado.

## Required Output
Producir LearningCandidate con:
- candidate_id
- kind
- scope
- statement
- confidence
- evidence[]
- contradictions[]
- source_events[]
- status

## Stop conditions
- Fuente no trazable.
- Evidencia única insuficiente para generalización.
- Contradicción con policy/Frozen knowledge.
- Se intenta promocionar sin evaluación.

## Verification
- El candidato puede reconstruirse desde sus fuentes.
- Project scope no se eleva silenciosamente a global.
- La promoción usa los gates de memoria/evolución existentes.
