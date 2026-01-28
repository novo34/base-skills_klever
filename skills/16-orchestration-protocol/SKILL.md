---
name: orchestration-protocol
description: Protocolo determinista para coordinar múltiples agentes con roles, fases y gates.
---

## Purpose
Habilitar la ejecución multi-agente fiable mediante la separación de roles, trabajo por fases e integración controlada.

## Non-negotiables
- Generar `docs/orchestration/WORKPLAN.md` antes de cualquier implementación multi-agente.
- Solo un agente (Integrador) puede consolidar cambios transversales.

## Stop conditions
- Conflictos de roles sin resolución del Integrador.

## Required Output
- `WORKPLAN.md` actualizado.
- Esqueleto de `HANDOFFS.md`.

## Verification
- Los roles asignados operan dentro de sus límites de propiedad.
