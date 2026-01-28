---
name: artifact-lifecycle-and-cleanup
description: Propiedad y limpieza de artefactos generados.
---

## Purpose
Mantener la higiene del repositorio y evitar confusiones por archivos obsoletos o huérfanos.

## Non-negotiables
- Todo archivo generado debe tener un dueño (Rol) y un ciclo de vida definido.
- Los archivos temporales se eliminan tras el éxito de la tarea.

## Stop conditions
- Generación de archivos sin registro en el `STATE.md`.

## Required Output
- Lista de artefactos creados y su destino.
- Confirmación de limpieza.

## Verification
- El árbol de archivos tras la ejecución es mínimo y justificado.
