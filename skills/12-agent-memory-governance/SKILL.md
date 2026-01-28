---
name: agent-memory-governance
description: Gobernanza estricta de memoria en agentes autónomos (short-term, long-term, frozen).
---

## Purpose
Prevenir la corrupción de memoria, la deriva cognitiva y el aprendizaje no seguro en agentes de larga duración.

## Non-negotiables
- Clasificación obligatoria de la memoria:
  - **Short-term**: Efímera, limitada a la tarea.
  - **Long-term**: Aprobada, reutilizable.
  - **Frozen**: Inmutable, fuente de verdad confiable.
- Los agentes no pueden promocionar memoria a "Long-term" sin validación.
- Las escrituras en memoria deben ser explícitas e intencionadas.

## Stop conditions
- Si la categoría de memoria no está clara, no almacenarla.
- Si la memoria contradice el conocimiento "Frozen", detenerse y escalar.

## Required Output
- Entrada de memoria.
- Categoría.
- Fuente y justificación.
- Estado de validación.

## Verification
- La promoción de memoria sigue las reglas declaradas.
- La memoria "Frozen" permanece inalterada.
