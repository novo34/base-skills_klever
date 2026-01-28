---
name: preflight-check
description: Fase de análisis mandatorio antes de cualquier implementación para detectar riesgos y coordinar autonomía.
---

## Purpose
Garantizar que no se inicie ninguna implementación sin haber analizado riesgos y, en entornos autónomos, haber definido límites, presupuestos y puntos de control.

## Non-negotiables
- Prohibido empezar a escribir código sin presentar el Preflight Report.
- **V5.0 - Autonomous Run Declaration**: Mandatorio si el agente va a operar de forma autónoma por periodos prolongados.

## Stop conditions
- Si los límites de autonomía (tiempo/coste/acciones) no están definidos.
- Si no hay puntos de aprobación humana para acciones de alto impacto.

## Required Output (Mandatory Template)
### Missing Info
- ...

### Data / Legal Risks
- (Incluir riesgos multi-tenant y de privacidad)

### Autonomous Run Declaration (v5.0)
- **¿Es una ejecución autónoma larga?**: (Yes/No)
- **Límites Declarados**: (Tiempo / Acciones / Presupuesto)
- **Frecuencia de Checkpoints**:
- **Categorías de Memoria a usar**:
- **Puntos de Aprobación Humana**:

### Multi-Agent Workplan (v4.0)
- **Roles**:
- **Locks**:

### Plan
1. ...

### Ask / Confirm
- ...

## Verification
- Confirmación de los límites de autonomía por parte del Supervisor antes de iniciar.
