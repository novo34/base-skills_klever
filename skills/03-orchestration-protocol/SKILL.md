---
name: orchestration-protocol
description: Protocolo determinista para coordinar múltiples agentes con roles, fases, gates y orden de integración.
---

## Purpose
Habilitar la ejecución multi-agente fiable mediante la imposición de separación de roles, trabajo por fases e integración controlada y estable.

## Non-negotiables
- Ejecutar siempre el preflight primero y generar un `docs/orchestration/WORKPLAN.md` antes de la implementación.
- **V4.1 - Declaración de Estabilidad**: Cada rol debe declarar explícitamente la idempotencia de sus acciones y el ciclo de vida de sus artefactos en su handoff.

## Stop conditions
- Si el alcance o los criterios de estabilidad no están claros.
- Si se detectan loops de agentes o duplicación de trabajo sin controles de idempotencia.

## Required Output
Generar o actualizar `docs/orchestration/WORKPLAN.md`.
Generar esqueleto de `docs/orchestration/HANDOFFS.md`.

## Verification
- El Workplan existe y define claramente el ciclo de vida de los entregables.
