---
name: logging-security
description: Seguridad Crítica - Redacción de PII y Manejo Seguro de Logs.
---

## Purpose
Evitar la fuga de secretos y PII en los sistemas de logs.

## Non-negotiables
- Redacción automática de emails, tokens y contraseñas en logs.
- Los logs deben estar estructurados para auditoría.

## Stop conditions
- Detección de PII en claro en el buffer de logs de salida.

## Required Output
- Lista de campos redactados.
- Confirmación de formato JSON.

## Verification
- Inspección de logs en desarrollo confirmando la ausencia de datos sensibles.
