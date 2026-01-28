---
name: ci-quality-gates
description: CI obligatorio para PRs: lint/typecheck/test/build + prisma validate + openapi + i18n.
---

## Purpose
Prevenir que cambios de baja calidad o que rompan el sistema lleguen a la rama principal mediante la ejecución automática de puertas de calidad.

## Non-negotiables
- Ningún cambio se integra sin pasar todos los gates definidos.
- La especificación OpenAPI debe estar sincronizada con el código.

## Stop conditions
- Si no existe un pipeline de CI, detener desarrollo de features y crear un CI mínimo primero.
- Si cualquier puerta de calidad falla, el merge queda bloqueado.

## Required Output
- Estado del pipeline de CI.
- Lista de puertas (gates) pasadas/fallidas.
- Notificación de nuevos checks añadidos.

## Verification
- CI se ejecuta en la PR.
- Todos los gates pasan satisfactoriamente antes del merge.
