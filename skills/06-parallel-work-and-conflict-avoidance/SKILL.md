---
name: parallel-work-conflict-avoidance
description: Reglas para trabajo en paralelo: ownership por carpeta, locks, y prevención de conflictos en Git.
---

## Purpose
Permitir la ejecución paralela segura sin conflictos de merge ni implementaciones duplicadas.

## Non-negotiables
- **Propiedad de archivos por Rol**:
  - DB Agent: `prisma/`, migraciones, cambios de esquema.
  - Backend Agent: `src/server/`, handlers, edits OpenAPI.
  - Frontend Agent: `src/app/`, `src/components/`.
  - Security Agent: políticas, validación, redacción, docs.
  - QA Agent: tests, Playwright, CI updates.
  - Integrator: merges transversales, verificación final.
- Ningún rol puede modificar simultáneamente archivos de alto tráfico sin bloqueo común.
- Uso de "locks" declarados en STATE bajo `LOCKED_FILES` o `LOCKED_AREAS`.

## Stop conditions
- Si un archivo/área está bloqueado (locked) por otro rol: detenerse y trabajar en otra zona o esperar re-asignación.
- Si surge un conflicto durante el merge: detenerse; el Integrador resuelve y registra la decisión.

## Required Output
Actualizar `docs/orchestration/STATE.md` con:
- Áreas de propiedad por rol.
- Áreas/archivos bloqueados.
- Orden de merge.

## Verification
- No hay modificaciones solapadas entre roles.
- El Integrador completa el merge con CI limpio y handoffs registrados.
