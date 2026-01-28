---
name: dependency-supply-chain
description: Seguridad en la cadena de suministro.
---

## Purpose
Prevenir ataques a través de librerías externas.

## Non-negotiables
- Lockfile obligatorio. Auditar vulnerabilidades.

## Stop conditions
- Vulnerabilidades críticas sin parches.

## Required Output
- `pnpm audit` result.

## Verification
- Clean audit.
