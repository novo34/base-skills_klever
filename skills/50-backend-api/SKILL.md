---
name: backend-api-contracts
description: Desarrollo de APIs REST bajo contrato OpenAPI.
---

## Purpose
Garantizar la interoperabilidad mediante contratos estrictos.

## Non-negotiables
- Alineación total con el `openapi.yaml`.
- Validación Zod en todos los inputs de los handlers.

## Stop conditions
- Cambio en la firma de un endpoint sin actualizar la documentación.

## Required Output
- Endpoint documentado y validado.

## Verification
- Swagger/Scalar refleja los cambios correctamente.
