---
name: request-security
description: Seguridad Crítica - Validación de Peticiones y Protección contra Ataques.
---

## Purpose
Blindar la aplicación contra ataques de inyección, CSRF y SSRF.

## Non-negotiables
- Validación obligatoria con `Zod` de TODA entrada externa.
- Sanatización de salidad para prevenir XSS.

## Stop conditions
- Endpoints de mutación sin protección CSRF (si se usan cookies).

## Required Output
- Esquemas de validación Zod.
- Política de rate-limiting.

## Verification
- Pruebas de inyección malformada bloqueadas.
