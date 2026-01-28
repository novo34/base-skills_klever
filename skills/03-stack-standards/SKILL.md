---
name: stack-standards-nextjs
description: Estándar fijo del stack: Next.js App Router + TS strict + pnpm + Prisma + next-intl + REST+OpenAPI + shadcn.
---

## Non-negotiable defaults
- Next.js (App Router).
- TypeScript strict.
- pnpm.
- Prisma (Postgres/MySQL).
- next-intl.
- REST + OpenAPI.
- Tailwind + shadcn/ui.
- Zod (validación).

## Scripts esperados (package.json)
- `lint` -> eslint
- `typecheck` -> tsc --noEmit
- `test` -> vitest
- `build` -> next build
- `dev` -> next dev
