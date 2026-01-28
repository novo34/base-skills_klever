---
name: db-migrations-safety
description: Migraciones de base de datos seguras y reversibles.
---

## Purpose
Evolucionar el esquema de datos sin downtime ni pérdida de integridad.

## Non-negotiables
- Migraciones siempre reversibles.
- No realizar cambios destructivos (drop column/table) sin fase previa de deprecación.

## Stop conditions
- Migración que bloquea tablas grandes en producción sin análisis de impacto.

## Required Output
- Script de migración y script de rollback.

## Verification
- `prisma migrate status` OK.
