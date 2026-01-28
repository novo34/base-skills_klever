---
name: decision-finalization-and-locking
description: Bloqueo y cierre definitivo de decisiones para evitar re-litigación por agentes.
---

## Purpose
Prevenir que los agentes reabran o ignoren decisiones ya finalizadas y acordadas por el swarm.

## Non-negotiables
- Las decisiones finalizadas son inmutables a menos que se abra un proceso formal de reapertura.
- Las decisiones bloqueadas (locked) no pueden ser puenteadas por nuevos agentes que se unan al proceso.

## Stop conditions
- Si un agente intenta sobreescribir una decisión bloqueada sin autorización.

## Required Output
- ID de decisión vinculada.
- Timestamp de bloqueo.
- Condiciones de reapertura (si existen).

## Verification
- Las decisiones bloqueadas se mantienen vigentes y son respetadas por todos los agentes del sistema.
