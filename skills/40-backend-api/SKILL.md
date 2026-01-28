---
name: backend-api-contracts
description: Backend pro: REST consistente + OpenAPI, errores, paginación, idempotencia, seguridad por defecto.
---

## Purpose
Establecer un contrato de comunicación claro, seguro y escalable entre el cliente y el servidor mediante APIs consistentes.

## Non-negotiables
- Todo endpoint debe estar documentado en la especificación OpenAPI.
- Uso de un formato de error estándar: `{ "error": { "code": string, "message": string } }`.
- Validación obligatoria de peticiones con `Zod`.

## Stop conditions
- Si el endpoint no incluye controles de autorización (tenant scoping).
- Si una operación de creación crítica no es idempotente.

## Required Output
- Resumen del contrato del endpoint (URL, Method, Params, Response).
- Casos de error y códigos de estado HTTP asociados.

## Verification
- Pruebas de integración contra el endpoint confirmando el contrato y la seguridad.
