---
name: swarm-consensus-protocol
description: Protocolo de consenso para decisiones críticas en sistemas multi-agent swarm.
---

## Purpose
Garantizar la toma de decisiones fiable cuando múltiples agentes operan de forma concurrente sobre el mismo objetivo.

## Non-negotiables
- Las decisiones críticas (cambios de esquema, deploys, borrados) requieren consenso del enjambre (swarm).
- Ningún agente individual tiene autoridad final sobre una decisión etiquetada como "crítica".
- Las reglas de consenso deben ser explícitas antes de la votación.

## Stop conditions
- Si no se alcanza el quórum mínimo definido.
- Si los votos son inconsistentes o contradictorios sin lógica de desempate.

## Required Output
- Tema de la decisión.
- Agentes involucrados en el swarm.
- Propuestas individuales documentadas.
- Método de consenso utilizado.
- Decisión final y justificación técnica.

## Verification
- La decisión adoptada es reproducible bajo las mismas condiciones de entrada.
- Las opiniones disidentes quedan registradas para auditoría.
