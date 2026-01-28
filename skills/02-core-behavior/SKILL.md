---
name: core-behavior
description: Reglas base obligatorias para cualquier cambio (calidad, claridad, cero inventos, cambios incrementales).
---

## Purpose
Definir el estándar de oro de comportamiento del agente para asegurar entregas coherentes, seguras y profesionales.

## Non-negotiables
- **No empezar sin Preflight**: Es obligatorio haber pasado la skill `preflight-check`.
- **Cambios incrementales**: Prohibido refactor masivo no solicitado.
- **Claridad**: Toda decisión técnica debe estar justificada si se desvía del estándar.

## Stop conditions
- No existen criterios de aceptación definidos.
- Se detecta una falta de alineación crítica con el stack definido en `stack-standards-nextjs`.

## Required Output
- Informe de Pre-vuelo.
- Lista resumida de cambios realizados.
- Lista de archivos tocados.
- Resultados de verificación local.

## Definition of Done (Mandatory)
- `pnpm lint` ✅
- `pnpm typecheck` ✅
- `pnpm test` ✅ (si existen)
- `pnpm build` ✅
- OpenAPI actualizado si los endpoints cambiaron.
- i18n keys añadidas (sin strings hardcoded) si la UI cambió.
- Sin PII/secrets en los logs.

## Verification
- Ejecución de los scripts de la Definition of Done antes de notificar al usuario.
