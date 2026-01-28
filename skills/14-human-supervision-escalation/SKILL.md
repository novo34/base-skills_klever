---
name: human-supervision-escalation
description: Escalación humana obligatoria en decisiones de alto impacto durante autonomía.
---

## Purpose
Asegurar que los humanos permanezcan en control de las decisiones críticas tomadas por agentes autónomos.

## Non-negotiables
- Acciones que requieren aprobación humana mandatoria:
  - Eliminación de datos.
  - Cambios de esquema de DB.
  - Despliegues en producción.
  - Promoción de memoria a "Long-term".
- El agente debe pausarse y esperar la aprobación explícita.

## Stop conditions
- Si se requiere aprobación y no se obtiene, no proceder.
- Si el agente ignora la aprobación, terminar la ejecución inmediatamente.

## Required Output
- Acción que requiere aprobación.
- Contexto e impacto detallado.
- Decisión de aprobación y timestamp.

## Verification
- Las acciones de alto impacto solo ocurren tras la validación humana registrada.
