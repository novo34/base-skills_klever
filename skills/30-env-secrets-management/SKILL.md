---
name: env-secrets-management
description: Gestión segura de variables y secretos.
---

## Purpose
Evitar la exposición de credenciales y configurar entornos dinámicos.

## Non-negotiables
- No secretos en Git. Usar `.env.example`.

## Stop conditions
- Secreto expuesto en historial de Git.

## Required Output
- Lista de variables necesarias.

## Verification
- Validación con Zod al arranque.
