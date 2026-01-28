---
name: idempotency-and-retry-control
description: Previene loops y efectos secundarios en ejecuciones multi-agent.
---

## Purpose
Garantizar ejecuciones predecibles y sin duplicados en sistemas autónomos y distribuidos.

## Non-negotiables
- Las operaciones de mutación deben ser idempotentes (misma entrada = mismo estado).
- Los reintentos deben tener un límite máximo y un backoff exponencial.

## Stop conditions
- Operación de escritura no idempotente sin plan de compensación.

## Required Output
- Estrategia de idempotencia por paso.
- Política de reintentos declarada.

## Verification
- Re-ejecución de tareas confirmando la ausencia de duplicados en DB/FS.
