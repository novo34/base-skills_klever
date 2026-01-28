---
name: stack-standards-nextjs
description: Estándar tecnológico fijo del proyecto.
---

## Purpose
Evitar la fragmentación tecnológica y asegurar la mantenibilidad.

## Non-negotiables
- Next.js (App Router), pnpm, Prisma, next-intl, shadcn/ui, Zod.

## Stop conditions
- Introducción de tecnologías fuera del stack aprobado sin ADR.

## Required Output
- Confirmación de alineación con el stack.

## Verification
- `pnpm build` confirma la compatibilidad de todos los módulos.
