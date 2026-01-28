---
name: request-security
description: Seguridad Crítica - Validación de Peticiones y Protección contra Ataques.
---

## Rules
- Validación obligatoria de TODA entrada externa (body, query, params, headers) con Zod.
- CSRF: Implementar protección en todas las mutaciones si se usan cookies de sesión.
- SSRF: Bloquear fetch a URLs arbitrarias; usar allowlist estricto si es necesario.
- XSS: Sanear cualquier salida de datos no controlada por el framework (React/Next).
- Rate Limiting: Aplicar a endpoints sensibles y costosos.

## Checklist
- ¿Se están validando todos los tipos de datos de la request?
- ¿Hay límites de tamaño en los bodies de las peticiones?
