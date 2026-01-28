---
name: retention-dsar
description: Gestión de Retención de Datos y Derechos de los Interesados (DSAR).
---

## Purpose
Garantizar el cumplimiento legal sobre el ciclo de vida de los datos personales y los derechos de los usuarios.

## Non-negotiables
- Todo dato P1/P2 debe tener un periodo de retención definido.
- El sistema debe soportar el borrado total (derecho al olvido) y la exportación.

## Stop conditions
- Ausencia de estrategia de anonimización o borrado para nuevas entidades de datos.

## Required Output
- Actualización de `RETENTION.md`.
- Flujo de cumplimiento DSAR verificado.

## Verification
- Ejecución de script de borrado/anonimizado en entorno de pruebas satisfactorio.
