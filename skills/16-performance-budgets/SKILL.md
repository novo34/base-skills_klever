---
name: performance-budgets
description: Rendimiento: Evitar Waterfalls, Bundles pesados y mala gestión de Caché.
---

## Purpose
Asegurar una experiencia de usuario fluida mediante el control riguroso del tiempo de carga y el uso eficiente de recursos.

## Non-negotiables
- Minimizar el uso de Client Components para mantener el bundle principal ligero.
- Evitar cascadas (waterfalls) de peticiones fetch en el servidor.

## Stop conditions
- Si el tamaño del bundle de una página aumenta drásticamente sin una justificación de interactividad crítica.

## Required Output
- Análisis de impacto en el rendimiento (ej. lighthouse scores previos/posteriores si hay entorno de staging).

## Verification
- `pnpm build` finaliza sin advertencias de tamaño excesivo.
- Verificación manual de que no hay saltos visuales (layout shift) excesivos.
