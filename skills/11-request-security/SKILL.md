---
name: request-security
description: Seguridad Crítica - Validación de Peticiones y Protección contra Ataques.
---

## Purpose
Blindar todos los puntos de entrada de la aplicación contra ataques comunes mediante una validación rigurosa y políticas de seguridad proactivas.

## Non-negotiables
- Toda entrada externa debe pasar por un esquema de validación de `Zod`.
- Implementación obligatoria de protección CSRF en mutaciones basadas en cookies.

## Stop conditions
- Si se detecta el uso de `eval()` o inyecciones directas de HTML sin saneamiento.
- Si se permite el acceso a URLs externas sin una allowlist controlada (SSRF risk).

## Required Output
- Esquemas de validación aplicados.
- Política de rate-limiting definida para el recurso.

## Verification
- Pruebas de inyección de datos malformados bloqueadas por validación.
- Verificación de cabeceras de seguridad activas.
