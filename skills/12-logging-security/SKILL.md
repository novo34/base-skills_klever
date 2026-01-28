---
name: logging-security
description: Seguridad Crítica - Redacción de PII y Manejo Seguro de Logs.
---

## Purpose
Evitar la fuga accidental de datos sensibles y personales a través de los sistemas de registro y observabilidad.

## Non-negotiables
- Prohibición absoluta de loguear información de identificación personal (PII) o secretos en claro.
- Uso de hashing criptográfico para identificar registros de usuario en logs si es estrictamente necesario.

## Stop conditions
- Si en la revisión manual se detecta un email, contraseña o token en una cadena de log.

## Required Output
- Lista de campos redactados en la implementación.
- Confirmación de cumplimiento de la política de logs.

## Verification
- Inspección de los logs generados en modo desarrollo para asegurar la redacción correcta.
