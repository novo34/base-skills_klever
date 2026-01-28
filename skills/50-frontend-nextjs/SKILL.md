---
name: frontend-nextjs-architecture
description: Frontend pro con Next.js App Router: server/client boundaries, data-fetching, estados, performance.
---

## Purpose
Optimizar el rendimiento y la mantenibilidad del frontend utilizando las capacidades avanzadas de Next.js App Router y TypeScript.

## Non-negotiables
- Uso preferente de Server Components para la carga de datos.
- Gestión de estados de carga (loading) y error mediante archivos `loading.tsx` y `error.tsx`.

## Stop conditions
- Si se detecta prop-drilling excesivo que podría resolverse con composición o contextos controlados.
- Si se exponen secretos o PII innecesaria en el bundle del cliente.

## Required Output
- Definición de componentes de servidor vs cliente y justificación.
- Flujo de interacción del usuario documentado.

## Verification
- Verificación visual de los estados de carga y error.
- Revisión de la red de red (network tab) para asegurar que no hay waterfalls excesivos.
