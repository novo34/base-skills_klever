---
name: idempotency-and-retry-control
description: Previene loops, duplicación y efectos secundarios en ejecuciones multi-agent con reintentos.
---

## Purpose
Garantizar que las ejecuciones repetidas, los reintentos o los fallos parciales no produzcan efectos secundarios duplicados ni estados inconsistentes.

## Non-negotiables
- Cualquier operación que escriba datos, genere artefactos o mute el estado DEBE ser idempotente.
- Los agentes deben detectar resultados de ejecuciones previas antes de volver a ejecutar un paso.
- Los reintentos deben estar acotados y documentados.

## Stop conditions
- Si una operación no puede hacerse idempotente, detenerse y escalar al Integrador.
- Si un reintento duplicaría datos o artefactos, detenerse y proponer una alternativa segura.

## Required Output
- Estrategia de idempotencia para cada paso de mutación:
  - Identificador utilizado (request-id, hash, key).
  - Qué se verifica antes de la ejecución.
- Política de reintentos (reintentos máximos, backoff, condición de aborto).

## Verification
- Ejecutar el mismo paso dos veces no produce efectos secundarios adicionales.
- No se crean registros o archivos duplicados en caso de reintento.
