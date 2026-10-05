---
name: adaptive-workflow-compilation
description: Compila un workflow proporcional a la intención, riesgo, radio de cambio, capacidades, evidencia y presupuesto.
---

## Purpose
Evitar workflows rígidos o sobredimensionados y construir un proceso seguro específico para cada tarea.

## Non-negotiables
- La compilación nunca reduce gates mínimos definidos por riesgo o política.
- Intent depth, risk y change radius deben influir en la profundidad del workflow.
- Las capacidades se seleccionan por necesidad, no por proliferación de agentes.
- Evidencia y presupuesto son parte del workflow antes de ejecutar.
- Un workflow compilado no puede modificar políticas superiores.

## Required Output
Producir AdaptiveWorkflow con:
- workflow_id
- task_id
- intent_depth
- risk
- change_radius
- capabilities[]
- steps[]
- gates[]
- evidence_requirements[]
- budget_class

## Compilation rules
- L0/R0 local: LIGHT.
- L1-L2 o R1-R2: STANDARD.
- L3 o R3: DEEP.
- L4 o R4: CRITICAL.
- Riesgo siempre puede elevar la profundidad; nunca reducirla.
- Cambios UI/browser incluyen browser verification.
- Cambios de comportamiento incluyen regression evidence.
- Cambios arquitectónicos incluyen Architect y ADR/plan evidence.

## Stop conditions
- Falta AcceptanceContract.
- Riesgo o change radius no pueden determinarse.
- Una capacidad requerida no existe o no está autorizada.
- El workflow propuesto omite un gate obligatorio.

## Verification
- La profundidad resultante es al menos la exigida por riesgo.
- Cada criterio crítico tiene evidencia prevista.
- No se añaden pasos sin relación con el objetivo.
