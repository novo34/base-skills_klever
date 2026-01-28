---
name: retention-dsar
description: Gestión de Retención de Datos y Derechos de los Interesados (DSAR).
---

## Purpose
Garantizar que los datos personales no se conserven más tiempo del necesario y que los usuarios puedan ejercer sus derechos legales (acceso, borrado, rectificación).

## Non-negotiables
- Toda entidad que contenga PII debe tener una política de retención definida.
- Debe existir un camino técnico para la exportación y el borrado total de los datos de un usuario.

## Stop conditions
- Si no existe una estrategia para cumplir con una solicitud de borrado (Right to be Forgotten).

## Required Output
- Actualización de `RETENTION.md` con las nuevas entidades de datos.
- Confirmación de que el flujo de DSAR soporta los nuevos datos.

## Verification
- Prueba técnica de borrado/anonimización confirmada en base de datos.
