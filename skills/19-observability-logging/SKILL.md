---
name: observability-logging
description: Observabilidad pro: logs estructurados, request-id, redaction, error tracking, métricas básicas.
---

## Purpose
Proporcionar una visibilidad completa y estructurada del comportamiento del sistema para facilitar el diagnóstico y la mejora continua.

## Non-negotiables
- Todos los logs producidos en el servidor deben seguir una estructura JSON consistente.
- Cada petición debe estar vinculada a un `requestId` único propagado en toda la traza.

## Stop conditions
- Si los logs no incluyen metadatos básicos (timestamp, level, context).

## Required Output
- Ejemplos de logs estructurados generados por la nueva funcionalidad.
- Configuración de alertas críticas (si aplica).

## Verification
- Trazabilidad de una petición completa a través del flujo del sistema mediante el `requestId`.
