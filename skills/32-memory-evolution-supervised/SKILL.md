---
name: memory-evolution-supervised
description: Evolución controlada y supervisada de memoria en agentes autónomos.
---

## Purpose
Permitir que los agentes mejoren con el tiempo evitando el aprendizaje no seguro, incorrecto o que refuerce errores propios.

## Non-negotiables
- Los agentes NO pueden promocionar memoria a "Long-term" de forma autónoma.
- Toda evolución de memoria debe ser supervisada y explícitamente aprobada por un humano o un proceso de auditoría superior.
- La evolución de la memoria debe ser reversible (versionada).

## Stop conditions
- Si la fuente del aprendizaje no es clara o está viciada.
- Si la nueva memoria contradice el conocimiento base inmutable (Frozen).
- Si falta la aprobación formal del Supervisor de Memoria.

## Required Output
- Candidato a memoria (Memory candidate).
- Fuente (Tarea, incidente, revisión).
- Cambio de categoría propuesto.
- Evaluación de riesgo.
- Registro de aprobación.

## Verification
- Los cambios en la memoria son rastreables y están logueados.
- Es posible realizar un rollback a un estado de memoria previo conocido.
