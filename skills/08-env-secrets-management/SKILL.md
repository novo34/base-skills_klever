---
name: env-secrets-management
description: Gestión profesional de variables, secrets y configuración por entorno.
---

## Purpose
Asegurar que los secretos y configuraciones sensibles se manejen de forma segura, evitando fugas de seguridad en el repositorio.

## Non-negotiables
- Prohibido subir secretos al control de versiones.
- Uso obligatorio de `.env.example` actualizado.

## Stop conditions
- Si se detecta un secreto commiteado, rotar el secreto inmediatamente y documentar.
- Si faltan variables críticas para el arranque de la aplicación.

## Required Output
- Lista de variables añadidas a `.env.example`.
- Confirmación de configuración en plataforma (Vercel/etc).

## Verification
- La aplicación arranca correctamente con el esquema de validación de `Zod` para variables de entorno.
