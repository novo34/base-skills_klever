---
name: preflight-check
description: Fase de análisis mandatorio antes de cualquier implementación para detectar riesgos y coordinar agentes.
---

## Purpose
Garantizar que no se inicie ninguna implementación sin haber analizado riesgos y, en entornos multi-agente, haber definido un plan de orquestación y estabilidad.

## Non-negotiables
- Prohibido empezar a escribir código sin presentar el Preflight Report.
- **V4.1 - Stability Check**: Es mandatorio analizar la idempotencia y el ciclo de vida de los artefactos antes de ejecutar.

## Stop conditions
- Si falta información crítica o contexto multi-tenant.
- Si no hay un plan de idempotencia definido para tareas que mutan estado.

## Required Output (Mandatory Template)
### Missing Info
- ...

### Data / Legal Risks
- (Incluir riesgos multi-tenant si aplica)

### Breaking Changes Risk
- ...

### Idempotency & Lifecycle Check (v4.1)
- **¿Qué pasos son idempotentes?**:
- **¿Qué artefactos se generarán?**:
- **¿Hay pasos reintentables?**:
- **¿Es explícito el contexto del inquilino (tenant)?**:

### Multi-Agent Workplan (v4.0)
- **Roles**:
- **Entregables**:
- **Orden de integración**:
- **Locks**:

### Plan
1. ...

### Ask / Confirm
- ...

## Verification
- El Integrador confirma el Workplan y las estrategias de estabilidad antes de proceder.
