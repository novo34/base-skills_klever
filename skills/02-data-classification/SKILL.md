---
name: data-classification
description: Clasificación de Datos y Principios de Minimización (Suiza nFADP / revFADP + GDPR).
---

## Purpose
Establecer un marco de clasificación de datos para aplicar controles de seguridad proporcionales al riesgo y cumplir con las normativas internacionales.

## Non-negotiables
- Clasificación obligatoria: P0 (Secrets), P1 (PII), P2 (Sensible), P3 (Telemetría).
- Minimización: No procesar datos personales sin propósito justificado.

## Stop conditions
- Procesamiento de PII sin haber actualizado el `DATA_MAP.md`.

## Required Output
- Niveles de clasificación asignados (P0-P3).
- Actualización de `DATA_MAP.md`.

## Verification
- Auditoría de esquema confirmando que no hay PII en tablas de baja seguridad.
