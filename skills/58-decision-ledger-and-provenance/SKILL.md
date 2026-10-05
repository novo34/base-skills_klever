---
name: decision-ledger-and-provenance
description: Registra decisiones materiales, alternativas, evidencia, alcance y supersesión de forma append-only.
---

## Purpose
Conservar por qué se tomó cada decisión y evitar que agentes reabran o contradigan decisiones sin contexto.

## Non-negotiables
- Las decisiones históricas no se borran ni reescriben.
- Una nueva decisión puede superseder otra mediante enlace explícito.
- Registrar alternativas consideradas y evidencia relevante.
- Distinguir actor, autoridad y alcance.
- Las decisiones locked respetan las reglas existentes de consenso/supervisión.

## Required Output
Producir DecisionRecord con:
- decision_id
- topic
- scope
- actor
- alternatives[]
- selected
- rationale
- evidence[]
- affected_artifacts[]
- supersedes[]
- status

## Stop conditions
- Se intenta mutar una decisión histórica.
- Se contradice una decisión locked sin proceso de reapertura autorizado.
- Falta evidencia/rationale en una decisión material.

## Verification
- Cadena de supersesión es acíclica.
- El estado vigente puede reconstruirse desde el ledger.
- Context retrieval puede filtrar decisiones por scope/relevancia.
