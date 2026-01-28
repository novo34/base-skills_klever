---
name: agent-lifecycle-control
description: Control explícito del ciclo de vida de agentes autónomos de larga duración.
---

## Purpose
Asegurar que los agentes de larga duración puedan ser iniciados, pausados, reanudados, inspeccionados y terminados de forma segura.

## Non-negotiables
- Cada agente autónomo debe declarar su estado de ciclo de vida.
- Los agentes deben soportar pausa y parada segura en cualquier momento.
- Ningún agente puede auto-reiniciarse tras una terminación sin autorización explícita.

## Stop conditions
- Si el estado del ciclo de vida es indefinido o se pierde, detener la ejecución.
- Si el agente no puede ser pausado de forma segura, abortar la ejecución.

## Required Output
- Estado actual: INIT / RUNNING / PAUSED / STOPPED / TERMINATED.
- Motivo del cambio de estado.
- Confirmación de parada segura (safe-stop).

## Verification
- El agente puede ser pausado y reanudado sin pérdida de estado.
- La terminación deja el sistema en un estado consistente.
