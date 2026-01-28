---
name: agent-memory-governance
description: Gobernanza estricta de memoria en agentes autónomos (short-term, long-term, frozen).
---

## Purpose
Prevenir la corrupción de memoria y el aprendizaje inseguro mediante la clasificación y supervisión del conocimiento.

## Non-negotiables
- Clasificación de memoria: Short-term, Long-term, Frozen.
- **V6.0 - Evolución Supervisada**: La promoción de memoria a "Long-term" requiere obligatoriamente la aprobación de `memory-evolution-supervised`.
- Los agentes deben tratar la memoria "Frozen" como la única fuente de verdad inmutable.

## Stop conditions
- Intento de promoción automática de memoria sin registro de supervisión.

## Required Output
- Registro de memoria con categoría y estado de validación.

## Verification
- El conocimiento promocionado coincide con los registros de aprobación supervisada.
