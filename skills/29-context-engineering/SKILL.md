---
name: context-engineering
description: Construye paquetes de contexto mínimos, relevantes, trazables y adecuados a cada tarea/agente.
---

## Purpose
Evitar tanto el contexto insuficiente como la carga masiva de información irrelevante que degrada coste, precisión y capacidad de razonamiento.

## Non-negotiables
- No cargar el repositorio completo por defecto.
- Clasificar contexto como REQUIRED, USEFUL, OPTIONAL o EXCLUDED.
- Mantener procedencia de cada elemento incluido.
- Las exclusiones críticas deben quedar registradas.
- La falta de contexto REQUIRED bloquea la ejecución.

## Context selection
Priorizar:
1. objetivo y AcceptanceContract;
2. políticas aplicables;
3. interfaces/contratos afectados;
4. archivos relevantes;
5. decisiones vigentes;
6. evidencia previa;
7. memoria validada y acotada.

## Required Output
Producir ContextPack con:
- task_id
- required[]
- useful[]
- optional[]
- excluded[]
- provenance[]
- token_or_size_budget
- missing_required[]
- truncation_decisions[]
- freshness

## Stop conditions
- Falta contexto REQUIRED.
- Fuente requerida está obsoleta o contradictoria.
- El paquete excede el presupuesto sin estrategia de reducción/recuperación.

## Verification
- Cada elemento del pack tiene razón de inclusión.
- Información sensible respeta scope/permisos.
- El handoff puede reconstruir la procedencia.
