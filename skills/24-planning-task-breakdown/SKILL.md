---
name: planning-task-breakdown
description: Descompone un contrato de aceptación en pasos ejecutables, dependencias, paralelismo y evidencia.
---

## Purpose
Transformar requisitos aprobados en un plan que pueda ejecutar un agente nuevo sin depender de contexto implícito de sesiones anteriores.

## Non-negotiables
- Cada paso debe tener objetivo, entradas, salidas, dependencias y criterio de salida.
- No crear tareas abiertas como "terminar backend" o "arreglar lo necesario".
- Toda dependencia debe ser explícita.
- Detectar ciclos antes de ejecutar.
- El plan debe incluir verificación y rollback cuando el riesgo lo requiera.

## Planning rules
- Dividir por unidades coherentes de comportamiento, no por cantidad arbitraria de archivos.
- Identificar grupos paralelizables solo cuando no compartan recursos en conflicto.
- Asociar capacidades requeridas, no inventar nuevos roles de autoridad.
- Preparar un contexto mínimo suficiente para cada paso.

## Required Output
Producir un borrador de ExecutionBlueprint con:
- objective
- source_requirements[]
- constraints[]
- assumptions[]
- steps[]
- dependencies[]
- parallel_groups[]
- required_capabilities[]
- required_evidence[]
- rollback_strategy
- completion_criteria

Cada step debe incluir:
- step_id
- objective
- inputs
- outputs
- dependencies
- affected_resources
- capabilities
- evidence_required
- exit_criteria

## Stop conditions
- Dependencias cíclicas.
- Paso sin criterio de salida.
- Recurso compartido conflictivo sin coordinación.
- Requisito crítico no cubierto por ningún paso.

## Verification
- Cobertura requisito -> paso -> evidencia.
- El DAG es acíclico.
- Un agente nuevo puede entender cada asignación desde su handoff.
