---
name: orchestration-protocol
description: Protocolo determinista para coordinar múltiples agentes con roles, fases, gates y orden de integración.
---

## Purpose
Habilitar la ejecución multi-agente fiable mediante la imposición de separación de roles, trabajo por fases e integración controlada.

## Non-negotiables
- Ejecutar siempre el preflight primero y generar un `docs/orchestration/WORKPLAN.md` antes de la implementación.
- El trabajo debe dividirse en roles con límites (boundaries) y entregables claros.
- Solo un agente (Integrator) puede realizar el merge de cambios transversales.
- Las skills de Seguridad/Privacidad siempre anulan los objetivos de orquestación.

## Stop conditions
- Si el alcance o los criterios de aceptación no están claros: detenerse y pedir aclaración.
- Si no existe la carpeta de artefactos compartidos: detenerse y crearla (`docs/orchestration/*`).
- Si dos roles proponen cambios conflictivos en los mismos archivos: detenerse y requerir decisión del Integrador.

## Required Output
Generar o actualizar `docs/orchestration/WORKPLAN.md` conteniendo:
- Objetivo y criterios de aceptación.
- Agentes/roles asignados.
- Entregables por rol.
- Orden de integración.
- Lista de riesgos y gates de calidad.
Generar esqueleto de `docs/orchestration/HANDOFFS.md` para los traspasos de rol.

## Verification
- El Workplan existe y los roles están asignados antes de cambios de código.
- La integración ocurre en el orden especificado.
- Los gates de CI pasan tras la integración.
