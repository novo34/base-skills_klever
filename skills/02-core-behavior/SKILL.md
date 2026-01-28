---
name: core-behavior
description: Reglas base obligatorias para cualquier cambio (calidad, claridad, multi-agente).
---

## Purpose
Definir el estándar de comportamiento del agente, asegurando consistencia incluso en colaboraciones complejas entre múltiples IAs.

## Non-negotiables
- **No empezar sin Preflight**: Confirmar el `WORKPLAN.md` si hay modo multi-agente.
- **Handoffs**: Cada tarea completada en un rol debe cerrar su `HANDOFFS.md`.
- **Integridad**: Mantener el `STATE.md` actualizado en cada fase.

## Stop conditions
- Se detecta una falta de alineación con el estado compartido del proyecto.
- Un agente intenta realizar cambios en un área bloqueada (locked) por otro rol.

## Required Output
- Informe de Pre-vuelo (v4.0 con Workplan).
- Handoff completo al Integrador.
- Estado del proyecto actualizado en `docs/orchestration/STATE.md`.

## Definition of Done (Mandatory)
- `pnpm lint/typecheck/test/build` ✅
- Handoffs completos registrados ✅
- State actualizado ✅
- Decisones registradas en `DECISIONS.md` ✅

## Verification
- Validación del Integrador sobre los handoffs de cada agente colaborador.
