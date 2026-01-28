---
name: stack-standards-nextjs
description: Estándar fijo del stack: Next.js App Router + TS strict + pnpm + Prisma + next-intl + REST+OpenAPI + shadcn.
---

## Purpose
Definir un stack tecnológico fijo y no negociable para evitar decisiones arquitectónicas inconsistentes.

## Non-negotiables
- Uso obligatorio de `pnpm` como gestor de paquetes.
- Uso de `Prisma` para la capa de base de datos.
- Uso de `next-intl` para internacionalización.
- UI basada en `Tailwind CSS` y `shadcn/ui`.
- Validación de datos externos con `Zod`.

## Stop conditions
- Si el repositorio no usa `pnpm`, no migrar automáticamente. Proponer plan.
- Si la ubicación de OpenAPI es desconocida, detenerse y preguntar.
- Si Prisma no está inicializado, proponer pasos de configuración antes de crear modelos.

## Required Output
- Confirmación de componentes del stack en uso.
- Lista de scripts verificados.
- Notificación de cualquier desviación del estándar.

## Verification
- `pnpm lint`
- `pnpm typecheck`
- `pnpm test`
- `pnpm build`
