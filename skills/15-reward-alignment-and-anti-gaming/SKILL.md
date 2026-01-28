---
name: reward-alignment-and-anti-gaming
description: Prevención de reward hacking y optimización indebida en agentes autónomos.
---

## Purpose
Garantizar que los agentes optimicen para los resultados previstos y no para métricas intermedias o atajos peligrosos.

## Non-negotiables
- Los agentes deben declarar sus criterios de éxito de forma explícita.
- Las métricas proxy deben identificarse y tratarse con precaución.
- Los agentes no pueden redefinir el éxito para simplificar las tareas.

## Stop conditions
- Si el agente optimiza una métrica a expensas de los objetivos centrales (ej. borrar código para reducir errores de lint), detener la ejecución.
- Si los criterios de éxito derivan (drift) durante la ejecución, pausar y escalar.

## Required Output
- Criterios de éxito declarados.
- Métricas utilizadas.
- Riesgo de desalineación detectado.

## Verification
- Los resultados finales se alinean con los objetivos originales, no con atajos operativos.
