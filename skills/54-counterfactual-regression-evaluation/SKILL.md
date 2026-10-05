---
name: counterfactual-regression-evaluation
description: Compara baseline y candidato sobre el mismo corpus para detectar mejoras y regresiones.
---

## Purpose
Evaluar cambios de JEV mediante comparación reproducible, no mediante impresión subjetiva.

## Non-negotiables
- Baseline y candidato usan el mismo corpus/version.
- Seguridad y calidad crítica tienen veto sobre mejoras de coste/latencia.
- Reportar incertidumbre y casos sin conclusión.
- El corpus no puede reescribirse silenciosamente para favorecer un candidato.
- Métricas incluyen calidad, seguridad, coste, latencia, correcciones y completion.

## Required Output
Producir CounterfactualEvalReport con:
- corpus_version
- baseline_version
- candidate_version
- scenario_results[]
- aggregate_metrics
- regressions[]
- wins[]
- uncertainty[]
- verdict

## Stop conditions
- Corpus/version no coincide.
- Faltan resultados del baseline o candidato.
- Existe regresión crítica de seguridad/calidad.
- Métricas no son comparables.

## Verification
- Repetición produce el mismo conjunto de escenarios.
- Cada verdict se deriva de reglas explícitas.
- PASS nunca oculta regresiones críticas.
