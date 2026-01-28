---
name: autonomy-limits-and-budgets
description: Límites duros de tiempo, coste, acciones y alcance para agentes autónomos.
---

## Purpose
Prevenir que los agentes autónomos consuman recursos de forma incontrolada o superen el tiempo previsto de ejecución.

## Non-negotiables
- Cada ejecución autónoma debe declarar:
  - Tiempo máximo de ejecución.
  - Número máximo de acciones/herramientas.
  - Número máximo de reintentos por tarea.
  - Presupuesto de coste/cómputo (si aplica).
- Los límites no pueden ser modificados por el propio agente.

## Stop conditions
- Si se alcanza cualquier límite, el agente debe pausarse o terminar.
- Si los límites no están definidos, no iniciar la ejecución autónoma.

## Required Output
- Límites declarados.
- Uso actual.
- Presupuesto restante.

## Verification
- El agente se detiene automáticamente al alcanzar los límites pre-establecidos.
