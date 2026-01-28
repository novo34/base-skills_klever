---
name: auth-security
description: Seguridad Crítica - Autenticación y Gestión de Sesiones.
---

## Purpose
Garantizar la identidad y sesión segura de los usuarios en el sistema.

## Non-negotiables
- Cookies de sesión `httpOnly`, `secure`, `sameSite=Lax/Strict`.
- No confiar en el cliente para la lógica de autorización.

## Stop conditions
- Uso de tokens accesibles desde JavaScript o falta de validación en el servidor.

## Required Output
- Configuración de seguridad de la cookie.
- Flujo de autorización verificado.

## Verification
- Auditoría manual del flujo de login/logout y gestión de roles.
