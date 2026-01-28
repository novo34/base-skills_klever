---
name: recovery-rollback
description: Plan de Recuperación ante Fallos y Rollback de Emergencia.
---

## Purpose
Proporcionar un mecanismo de respuesta rápida para restaurar el servicio estable en caso de fallos críticos post-despliegue.

## Non-negotiables
- El plan de rollback debe estar documentado ANTES del despliegue manual en producción.
- Priorizar la restauración del servicio sobre la investigación del error en caliente.

## Stop conditions
- Si no existe una versión anterior estable identificada o mapeada.
- Si un cambio en la base de datos es irreversible y compromete el rollback de código.

## Required Output
- Pasos críticos de rollback realizados (si aplica).
- Informe breve de contención de incidentes.

## Verification
- Servicio restaurado y verificado mediante Health Checks.
- Documento `docs/runbooks/ROLLBACK.md` actualizado.
