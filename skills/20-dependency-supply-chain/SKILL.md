---
name: dependency-supply-chain
description: Gestión de Dependencias, Auditoría de Seguridad y Lockfiles.
---

## Purpose
Mitigar los riesgos de ataques a la cadena de suministro mediante el control estricto y la auditoría de dependencias externas.

## Non-negotiables
- El archivo `pnpm-lock.yaml` es la única fuente de verdad para las versiones de dependencias.
- No se permiten nuevas dependencias sin una justificación técnica clara aprobada en el Preflight.

## Stop conditions
- Si una dependencia presenta vulnerabilidades críticas no mitigables reportadas por `pnpm audit`.

## Required Output
- Informe de impacto de la nueva dependencia (tamaño del bundle, seguridad).
- Justificación de por qué no se puede resolver con el código base actual.

## Verification
- `pnpm audit` finaliza sin errores críticos o altos.
