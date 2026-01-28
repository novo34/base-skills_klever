---
name: auth-security
description: Seguridad Crítica - Autenticación y Gestión de Sesiones.
---

## Purpose
Establecer mecanismos de autenticación y gestión de sesiones impenetrables para prevenir el acceso no autorizado y la suplantación de identidad.

## Non-negotiables
- Sesiones gestionadas exclusivamente mediante cookies con flags `httpOnly`, `secure` y `sameSite`.
- Verificación de identidad obligatoria en el lado del servidor para cada petición protegida.

## Stop conditions
- Si se propone usar `localStorage` para tokens de sesión.
- Si el mecanismo de autenticación no incluye protección contra ataques de fuerza bruta.

## Required Output
- Descripción del flujo de autenticación utilizado.
- Configuración de flags de seguridad de las cookies.

## Verification
- Verificación de que los tokens no son accesibles desde JavaScript (XSS hardening).
- Auditoría manual del flujo de login y cierre de sesión.
