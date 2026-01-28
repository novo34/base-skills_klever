---
name: deployment-strategy
description: Estrategias de Despliegue Seguro, Entornos y Health Checks.
---

## Environments
- Separación clara entre `dev`, `staging` y `prod`.
- Promoción de builds: La misma imagen/build debe fluir entre entornos.

## Rules
- Health Checks: El despliegue no es exitoso hasta que los health checks pasen.
- Migraciones: Deben ser compatibles hacia atrás (patrón expand/contract) durante el despliegue.
- Configuración: Validar todas las variables de entorno (`env`) al inicio.

## Required Artifacts
- `docs/runbooks/DEPLOY.md`: Pasos exactos del despliegue.
