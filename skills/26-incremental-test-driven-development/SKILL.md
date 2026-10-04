---
name: incremental-test-driven-development
description: Implementa cambios en incrementos pequeños guiados por evidencia de fallo y de éxito.
---

## Purpose
Reducir regresiones y falsos positivos obligando a demostrar el comportamiento antes y después del cambio cuando sea técnicamente aplicable.

## Non-negotiables
- Un cambio de comportamiento debe tener evidencia de regresión apropiada al riesgo.
- Preferir ciclo: failing evidence -> minimal change -> passing evidence -> refactor.
- No alterar tests únicamente para hacerlos pasar si contradicen el contrato de aceptación.
- No marcar éxito por build verde cuando el comportamiento requerido no está cubierto.
- Cada incremento debe mantener el repositorio en estado recuperable.

## Workflow
1. Identificar comportamiento objetivo.
2. Capturar prueba/evidencia que falle o demuestre la brecha.
3. Implementar el cambio mínimo coherente.
4. Ejecutar evidencia focalizada.
5. Ejecutar regresión relevante.
6. Simplificar sin cambiar comportamiento.
7. Registrar evidencia.

## Required Output
- failing_evidence
- implementation_increment
- passing_evidence
- regression_evidence
- refactor_summary
- uncovered_risks

## Stop conditions
- No existe forma válida de verificar un requisito crítico.
- Los tests contradicen el contrato de aceptación.
- El incremento requiere ampliar alcance sin replanning.

## Verification
- La evidencia anterior y posterior corresponde al mismo comportamiento.
- Las regresiones relevantes permanecen verdes.
- El refactor posterior no elimina cobertura requerida.
