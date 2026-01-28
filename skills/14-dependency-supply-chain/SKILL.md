---
name: dependency-supply-chain
description: Gestión de Dependencias, Auditoría de Seguridad y Lockfiles.
---

## Non-negotiables
- `pnpm-lock.yaml` obligatorio.
- No añadir dependencias sin justificar motivo e impacto ante el usuario.

## Security
- Recomendar `pnpm audit` periódico.
- Evitar librerías con baja actividad o dudosa procedencia.
