---
name: frontend-nextjs-architecture
description: Frontend pro con Next.js App Router: server/client boundaries, data-fetching, estados, performance.
---

## Non-negotiables
- Server Components por defecto.
- Client Components solo si hay interactividad real.
- No duplicar lógica: centralizar fetchers/services.
- Estados obligatorios: loading, error, empty.
- No hardcode de texto (ver i18n).

## Data fetching
- Preferir fetch en server cuando sea posible.
- Definir estrategia de cache/revalidate:
  - `no-store` si datos sensibles/tiempo real
  - `revalidate` si se puede cachear
- Evitar waterfalls: agrupar queries o usar `Promise.all`.

## Error boundaries
- Usar `error.tsx` donde aplique.
- Manejar not-found con `not-found.tsx` si aplica.

## Security
- No exponer PII en props a Client Component si no es necesario.
- No meter secrets en client bundle.

## Required output
- Qué es server vs client y por qué
- Cómo probar el flujo (pasos)
