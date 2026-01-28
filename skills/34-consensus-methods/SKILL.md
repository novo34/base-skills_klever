---
name: consensus-methods
description: Métodos válidos de consenso para swarms de agentes.
---

## Purpose
Proporcionar mecanismos de consenso deterministas y auditables para la inteligencia colectiva.

## Non-negotiables
- Se debe elegir un método de consenso por cada decisión crítica.
- El método debe ser proporcional al riesgo de la decisión.

## Allowed methods
- **Voto Mayoritario**: Riesgo bajo/moderado.
- **Voto Ponderado**: Basado en el nivel de expertise del agente en el dominio afectado.
- **Unanimidad**: Riesgo alto o cambios destructivos.
- **Desempate Humano**: Método por defecto en caso de conflicto persistente.

## Stop conditions
- Si el método elegido no está definido en la constitución.
- Si hay evidencia de que el método no se está aplicando correctamente.

## Required Output
- Método seleccionado y razón de su elección.
- Desglose de la votación/propuesta (Quórum).

## Verification
- El proceso de consenso sigue estrictamente el método declarado.
