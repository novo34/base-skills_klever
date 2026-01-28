---
name: env-secrets-management
description: Gestión profesional de variables, secrets y configuración por entorno.
---

## Non-negotiables
- Prohibido commitear secrets.
- `.env.example` debe listar TODAS las variables requeridas.
- Las variables reales se configuran en plataforma (Vercel/EasyPanel).

## Validation at startup
- Validar envs al iniciar (schema Zod) y fallar rápido.
