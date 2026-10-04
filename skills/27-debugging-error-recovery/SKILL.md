---
name: debugging-error-recovery
description: Diagnostica fallos mediante reproducción, hipótesis verificables, causa raíz y recuperación trazable.
---

## Purpose
Evitar arreglos por ensayo y error que ocultan síntomas, introducen regresiones o pierden conocimiento útil del incidente.

## Non-negotiables
- Reproducir el fallo antes de reparar cuando sea reproducible.
- Diferenciar síntoma, causa probable y causa raíz confirmada.
- Registrar hipótesis descartadas relevantes para evitar ciclos.
- La recuperación no puede saltarse riesgo, tests, staging, aprobación o rollback.
- Un workaround temporal debe estar identificado y tener condición de retirada.

## Workflow
1. Capturar error y contexto.
2. Reproducir.
3. Reducir el caso.
4. Formular hipótesis.
5. Obtener evidencia.
6. Confirmar causa raíz.
7. Corregir mínimamente.
8. Añadir prevención/regresión.
9. Verificar recuperación.

## Required Output
- reproduction
- observations[]
- hypotheses[]
- root_cause
- fix
- regression_evidence
- recurrence_prevention
- residual_risk
- rollback_or_recovery

## Stop conditions
- No puede distinguirse causa de correlación.
- El arreglo exige una decisión de arquitectura/producto no autorizada.
- La reparación destruye datos o requiere producción sin gate correspondiente.

## Verification
- El caso original deja de fallar por la causa explicada.
- Existe evidencia contra recurrencia razonable.
- No se declara causa raíz sin evidencia suficiente.
