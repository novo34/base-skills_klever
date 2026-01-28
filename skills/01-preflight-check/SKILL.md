---
name: preflight-check
description: Fase de análisis mandatorio antes de cualquier implementación para detectar riesgos y coordinar agentes.
---

## Purpose
Garantizar que no se inicie ninguna implementación sin haber analizado riesgos y, en entornos multi-agente, haber definido un plan de orquestación.

## Non-negotiables
- Prohibido empezar a escribir código sin presentar el Preflight Report.
- **V4.0 - Multi-Agent Plan**: Es mandatorio definir roles y entregables si más de un agente está involucrado.

## Stop conditions
- Si falta información crítica del backend/base de datos.
- Si no hay un Integrador asignado para tareas transversales.

## Required Output (Mandatory Template)
### Missing Info
- ...

### Data / Legal Risks
- ...

### Breaking Changes Risk
- ...

### Multi-Agent Workplan (v4.0)
- **Roles**: (Ej. DB Agent, Backend Agent, Integrator)
- **Entregables por rol**:
- **Orden de integración**:
- **Locks (Archivos bloqueados)**:

### Plan
1. ...

### Ask / Confirm
- ...

## Verification
- El Integrador confirma el Workplan antes de que cualquier agente ejecute cambios.
