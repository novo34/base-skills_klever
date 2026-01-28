---
name: checkpointing-and-state-snapshots
description: Snapshots obligatorios del estado cognitivo y operativo de agentes de larga duración.
---

## Purpose
Permitir la recuperación, el rollback y la inspección del estado del agente a lo largo del tiempo.

## Non-negotiables
- Los agentes deben crear checkpoints en intervalos o hitos definidos.
- Los checkpoints deben ser inmutables una vez creados.
- Solo el Integrador/Supervisor puede restaurar desde un checkpoint.

## Stop conditions
- Si falla la creación de un checkpoint, detener la ejecución autónoma.
- Si la integridad de un checkpoint es incierta, abortar la restauración.

## Required Output
- ID del Checkpoint.
- Timestamp.
- Resumen de estado (plan, referencias de memoria, tareas abiertas).
- Motivo del checkpoint.

## Verification
- El sistema puede restaurar a un checkpoint previo de forma determinista.
