---
name: human-supervision-escalation
description: Escalación humana obligatoria en decisiones de alto impacto y aprendizaje.
---

## Purpose
Asegurar que los humanos permanezcan en control de las decisiones críticas y de la evolución del conocimiento del sistema.

## Non-negotiables
- **Aprobación Humana Mandatoria** para:
  - Eliminación de datos / Cambios destructivos.
  - Despliegues en producción.
  - **Memory Evolution (v6.0)**: Toda promoción de conocimiento persistente.
  - Resoluciones de conflicto de consenso fallidas.
- El agente debe pausarse y esperar la validación.

## Stop conditions
- Decisión de alto impacto ejecutada sin firma de autorización humana.

## Required Output
- Registro de escalación con impacto y decisión final.

## Verification
- Auditoría de logs confirma que no hubo bypass de supervisión.
