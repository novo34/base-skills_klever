---
name: data-classification
description: Clasificación de Datos y Principios de Minimización (Suiza nFADP / revFADP + GDPR).
---

## Purpose
Establecer un marco de clasificación de datos para aplicar controles de seguridad proporcionales al riesgo y cumplir con las normativas de protección de datos (nFADP/GDPR).

## Non-negotiables
- Clasificación obligatoria de todos los campos de datos nuevos.
- Minimización: No se permiten campos de datos personales sin una justificación de propósito clara.
- Los datos P0 (Secretos) y P1/P2 (PII/Sensibles) deben estar protegidos con medidas de cifrado y acceso restringido.

## Stop conditions
- Si se propone procesar datos personales sin haber actualizado el `DATA_MAP.md`.
- Si se detecta almacenamiento de secretos en campos de texto plano.

## Required Output
- Clasificación de los nuevos datos introducidos (P0-P3).
- Actualización de `DATA_MAP.md`.

## Verification
- Auditoría de los campos de la base de datos para confirmar que no hay fuga de datos sensibles en tablas operativas.
