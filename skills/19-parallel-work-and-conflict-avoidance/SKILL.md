---
name: parallel-work-conflict-avoidance
description: Propiedad de archivos y bloqueos para evitar conflictos.
---

## Purpose
Permitir el trabajo en paralelo sin colisiones en Git ni implementaciones duplicadas.

## Non-negotiables
- Propiedad de archivos por rol (DB, Backend, Frontend, QA).
- Uso de `LOCKED_FILES` en el estado compartido para áreas de alto tráfico.

## Stop conditions
- Intento de modificación de un archivo bloqueado por otro rol.

## Required Output
- Registro de áreas de propiedad y bloqueos activos.

## Verification
- No existen conflictos de merge en la integración final.
