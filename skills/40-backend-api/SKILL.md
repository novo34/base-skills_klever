---
name: backend-api-contracts
description: Backend pro: REST consistente + OpenAPI, errores, paginación, idempotencia, seguridad por defecto.
---

## Non-negotiables
- Cada endpoint tiene:
  - Zod validation (request)
  - Response shape consistente
  - Error shape consistente
  - Update de OpenAPI (sync obligatorio)
- Autorización/tenant scoping obligatorio (ver security + data protection).

## Error shape estándar
- `{ "error": { "code": string, "message": string, "details"?: any, "requestId"?: string } }`

## Status codes (mínimo)
- 200/201 OK
- 400 validation
- 401 unauthenticated
- 403 forbidden
- 404 not found
- 409 conflict
- 429 rate limited
- 500 internal

## Pagination
- Obligatoria para listas:
  - `page`, `pageSize` o `cursor`
  - devolver `items` + `meta`

## Idempotencia
- Operaciones de creación críticas (facturas, pagos, exports):
  - soportar idempotency key o deduplicación por constraint.

## Timeouts & retries
- Llamadas externas: timeout + manejo de error claro.
- Prohibido “infinite retry”.

## OpenAPI
- La spec debe ser fuente de verdad o generada; en ambos casos: SIEMPRE consistente.
- Cada cambio de endpoint implica actualización de OpenAPI o regeneración verificable.

## Required output
- Lista de endpoints tocados
- Cambios en OpenAPI
- Casos de error y cómo probarlos
