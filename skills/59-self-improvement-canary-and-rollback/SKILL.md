---
name: self-improvement-canary-and-rollback
description: Promueve mejoras de JEV mediante evaluación, aprobación humana, canary aislado, monitorización y rollback probado.
---

## Purpose
Permitir auto-mejora supervisada sin permitir que JEV degrade sus propias salvaguardas.

## Non-negotiables
- Flujo obligatorio: proposal -> review -> benchmark -> human approval -> isolated canary -> monitor -> promote/rollback.
- Seguridad, autorización, audit, verifier independence y human approval no pueden debilitarse.
- Rollback debe estar definido y probado antes de canary/promotion.
- Canary no puede escribir directamente a producción.
- Una regresión crítica fuerza rollback.

## Required Output
Producir SelfImprovementRelease con:
- candidate_id
- benchmark_report
- human_approval
- canary_scope
- rollback_proof
- monitoring_metrics[]
- canary_result
- promotion_status

## Stop conditions
- Falta aprobación humana.
- Benchmark no es PASS.
- Rollback no probado.
- Candidato modifica/relaja controles protegidos.
- Canary detecta regresión crítica.

## Verification
- Ninguna promoción existe sin cadena completa de evidencia.
- El baseline permanece recuperable.
- Rollback puede ejecutarse sin depender del candidato.
