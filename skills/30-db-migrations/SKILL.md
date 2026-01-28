---
name: db-migrations-safety
description: Cambios de DB seguros (Prisma + Postgres/MySQL). Patrón expand/contract, backfills, constraints, performance.
---

## Non-negotiables
- Cambios de esquema SOLO vía Prisma migrations.
- Prohibido editar DB “a mano” como solución.
- Prohibido introducir NOT NULL sin plan de backfill.
- Prohibido borrar columnas/tablas sin deprecation plan.

## Expand/Contract (obligatorio para prod)
1) Expand: añadir columnas/tabla nullable, sin romper.
2) Backfill: job/script para completar datos.
3) Contract: aplicar NOT NULL/constraints/borrar viejo cuando esté migrado.

## Constraints & indexes
- Añadir constraints intencionalmente (unique, FK, NOT NULL) con migración segura.
- Crear índices para nuevas consultas.
- Documentar impacto: “tablas grandes” requieren cuidado (locks).

## Prisma rules
- `prisma migrate` con nombres claros.
- `prisma validate` antes de commit.
- Siempre revisar el SQL generado (cuando sea crítico).

## Required output
- Qué migraciones se crean/modifican
- Plan de rollback (aunque sea simple)
- Riesgo de locking/performance (1 párrafo)
