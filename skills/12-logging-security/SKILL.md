---
name: logging-security
description: Seguridad Crítica - Redacción de PII y Manejo Seguro de Logs.
---

## Rules
- Prohibido loguear secrets (keys, tokens, passwords) o PII en claro (nombres, emails, teléfonos).
- Redacción obligatoria: Usar hashing o truncado para PII si es necesario para depuración.
- Logs estructurados (JSON) para facilitar el parsing y la auditoría automática.
- Incluir un `requestId` único en cada log para correlación sin exponer datos del usuario.

## Checklist
- ¿Se están filtrando datos sensibles antes de enviarlos al sistema de logs?
- ¿El nivel de log es adecuado (evitar DEBUG con datos reales en prod)?
