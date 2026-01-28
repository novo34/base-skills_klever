---
name: code-review-quality-gates
description: Revisión de código y estándares de calidad.
---

## Purpose
Mantener la excelencia técnica mediante auditoría mutua.

## Non-negotiables
- Zero warnings en lint.
- Cobertura de tests críticos.

## Stop conditions
- Merge de código complejo sin tests unitarios.

## Required Output
- Checklist de revisión aprobado.

## Verification
- `pnpm quality` pasa al 100%.
