---
name: db-migrations-safety
description: Cambios de DB seguros (Prisma + Postgres/MySQL). Patrón expand/contract, backfills, constraints, performance.
---

## Purpose
Asegurar que los cambios en el esquema de la base de datos se realicen sin interrupción del servicio y con capacidad de reversión segura.

## Non-negotiables
- Los cambios de esquema deben realizarse exclusivamente a través de Prisma Migrations.
- Prohibido realizar cambios destructivos (DROP) sin un plan de deprecación previo.

## Stop conditions
- Si se intenta añadir una columna `NOT NULL` en una tabla con datos existentes sin un plan de backfill.
- Si el plan de migración bloquea tablas grandes en horas críticas de producción.

## Required Output
- Archivos de migración de Prisma generados.
- Plan de Rollback para la migración.
- Análisis de impacto en el rendimiento (locking).

## Verification
- `pnpm prisma validate` satisfactorio.
- Revisión del SQL generado para confirmar la seguridad de la migración.
