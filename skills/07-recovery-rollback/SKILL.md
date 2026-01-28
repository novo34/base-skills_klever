---
name: recovery-rollback
description: Plan de Recuperación ante Fallos y Rollback de Emergencia.
---

## Rules
- Rollback Automático: Si los health checks fallan post-deploy, el sistema debe revertir automáticamente si la plataforma lo soporta.
- Procedimiento Manual: Pasos claros para revertir a la versión anterior estable.
- Integridad de DB: Los rollbacks de código no siempre revierten cambios de DB; los cambios de DB deben ser seguros.

## Required Artifacts
- `docs/runbooks/ROLLBACK.md`: Pasos críticos para restaurar el servicio en segundos/minutos.
- `docs/runbooks/INCIDENTS.md`: Registro y gestión de fallos.
