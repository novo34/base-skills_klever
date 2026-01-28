---
name: observability-logging
description: Observabilidad pro: logs estructurados, request-id, redaction, error tracking, métricas básicas.
---

## Rules
- Logs estructurados (JSON) en server.
- Request correlation: `requestId` único por petición.
- Redacción de PII (ver logging-security).

## What to log
- Inicio/fin de request con status + duración.
- Errores operativos con code + requestId.
- Eventos de seguridad.
