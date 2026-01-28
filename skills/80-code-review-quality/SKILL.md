---
name: code-review-quality-gates
description: Reglas de calidad para PRs: types, tests, seguridad, rendimiento, DX. Bloquea merges inseguros.
---

## Purpose
Mantener la calidad y la salud a largo plazo de la base de código mediante revisiones rigurosas y automatizadas.

## Non-negotiables
- TypeScript estricto habilitado; evitar el uso de `any` sin una justificación técnica excepcional.
- Eliminación de código muerto (dead code) y exportaciones no utilizadas.

## Stop conditions
- Si la PR reduce la cobertura de tests críticos.
- Si no se cumplen los estándares definidos en el resto de skills (jerarquía v3.0).

## Required Output
- Resumen de la revisión de calidad.
- Resultados de los comandos de verificación obligatorios.

## Verification
- `pnpm lint`, `pnpm typecheck`, `pnpm test` pasados satisfactoriamente.
