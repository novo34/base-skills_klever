---
name: auth-security
description: Seguridad Crítica - Autenticación y Gestión de Sesiones.
---

## Rules
- Preferir sesiones por cookie `httpOnly`, `secure`, `sameSite=Lax/Strict`.
- No confiar nunca en `userId` o `tenantId` provenientes del cliente para lógica de propiedad.
- Implementar rotación de tokens y expiración corta por defecto.
- Proteger contra ataques de fuerza bruta en endpoints de login/reset.

## Checklist
- ¿Se valida la identidad en cada petición protegida?
- ¿El usuario está identificado de forma única en el server?
- ¿Las cookies tienen los flags de seguridad correctos?
