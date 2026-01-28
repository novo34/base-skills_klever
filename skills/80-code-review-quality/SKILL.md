---
name: code-review-quality-gates
description: Reglas de calidad para PRs: types, tests, seguridad, rendimiento, DX. Bloquea merges inseguros.
---

## Non-negotiables
- TypeScript strict: evitar `any` y casts sin justificar.
- Nada de “console.log” en prod (usar logger y redaction).
- No duplicar código: extraer helpers cuando haya repetición clara.
- Funciones pequeñas y legibles.
- No introducir dependencias sin justificar (ver supply-chain).
- Mantener OpenAPI y i18n al día.

## PR checklist (obligatorio)
- Lint/typecheck/test/build OK
- UI con estados completos
- Seguridad: authz/validation/PII logs OK
- Migraciones: plan seguro OK
- Docs: ADR/Runbook si cambió arquitectura/operación

## Required output
- Verificación local (comandos)
- Riesgos + mitigación
