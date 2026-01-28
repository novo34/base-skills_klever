---
name: core-behavior
description: Reglas base obligatorias para cualquier cambio (calidad, claridad, cero inventos, cambios incrementales).
---

## Non-negotiables
- Cambios incrementales. Prohibido refactor masivo o reestructura sin solicitud explícita.
- Prohibido asumir silenciosamente. Si falta info crítica: detenerse y pedirla.
- Mantener el scope: tocar solo módulos/archivos necesarios.
- No romper build/tests. Si algo falla, se arregla antes de “dar por terminado”.
- No introducir dependencias nuevas sin justificar (ver skill supply-chain).

## Stop conditions (si ocurre, NO implementar)
- No existen criterios de aceptación (qué se considera “listo”).
- No está definida la fuente de verdad (DB schema/Prisma, OpenAPI, i18n locales, auth model).
- La tarea implica datos personales y no existe DATA_MAP/RETENTION (ver protección de datos).
- Falta cualquier secret/variable requerida y no hay plan de envs (ver env-secrets).

## Required output for ANY task
1) Plan de Pre-vuelo (ver preflight-check).
2) Cambios realizados (bullets).
3) Archivos tocados.
4) Verificación local (comandos exactos).
5) Riesgos / follow-ups.
