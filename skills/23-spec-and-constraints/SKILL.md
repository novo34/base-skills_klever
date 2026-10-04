---
name: spec-and-constraints
description: Convierte una intención refinada en criterios de aceptación, restricciones y límites verificables.
---

## Purpose
Crear un contrato de aceptación suficiente para que planificación, desarrollo y verificación compartan la misma definición del resultado esperado.

## Non-negotiables
- Los criterios deben ser observables o comprobables.
- No usar frases vagas como "funciona bien", "mejor" o "correcto" sin evidencia definida.
- Registrar restricciones técnicas, de seguridad, compatibilidad, datos, UX, rendimiento y operación cuando apliquen.
- Separar requisitos de no-objetivos y preferencias.
- No inventar requisitos ausentes para rellenar una plantilla.

## Specification depth
- L0: resultado esperado y prueba mínima.
- L1: criterios de aceptación + no-regresión.
- L2: contrato de tarea + restricciones + superficies afectadas.
- L3: requisitos/contratos/ADR afectados.
- L4: PRD/SPEC/ADR/ROADMAP impactados.

## Required Output
Producir un AcceptanceContract con:
- intent_id
- acceptance_criteria[]
- constraints[]
- assumptions[]
- non_goals[]
- affected_requirements[]
- compatibility_requirements[]
- required_evidence[]
- unresolved_decisions[]
- specification_depth

## Stop conditions
- Un criterio crítico no puede verificarse.
- Una restricción contradice políticas superiores.
- Existen decisiones de producto/arquitectura sin resolver que cambian el resultado.

## Verification
- Cada criterio tiene método de verificación.
- Requisitos y no-objetivos no se contradicen.
- La especificación no excede innecesariamente la intención.
