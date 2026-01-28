---
name: ci-quality-gates
description: CI obligatorio para PRs: lint/typecheck/test/build + prisma validate + openapi + i18n.
---

## Gates obligatorios (bloquean merge)
- `pnpm lint`
- `pnpm typecheck`
- `pnpm test`
- `pnpm build`
- Prisma: `pnpm prisma validate`
- i18n: Sin keys faltantes.

## OpenAPI sync rule
- Si se toca endpoint: actualizar `docs/openapi.yaml`.
- El CI verifica que el output esté actualizado.
