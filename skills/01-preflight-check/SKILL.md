---
name: preflight-check
description: Fase de análisis mandatorio antes de cualquier implementación para detectar riesgos.
---

## Purpose
Garantizar que no se inicie ninguna implementación sin haber analizado previamente los riesgos, dependencias y necesidades de información.

## Non-negotiables
- Prohibido empezar a escribir código sin presentar primero el Preflight Report.
- Si falta información crítica, el agente DEBE detenerse.

## Stop conditions
- Si el usuario no confirma el plan cuando hay riesgos críticos detectados.
- Si no existe una fuente de verdad (DB, OpenAPI, etc.) clara para la tarea.

## Required Output (Mandatory Template)
### Missing Info
- (Lista de información faltante o "None")

### Data / Legal Risks
- (Riesgos de privacidad, seguridad o cumplimiento o "None")

### Breaking Changes Risk
- (Impacto en otras partes del sistema o "None")

### Plan
1. (Paso a paso lógico...)

### Ask / Confirm
- (Preguntas críticas para el usuario o "None")

## Verification
- Confirmación explícita del usuario sobre el Preflight antes de proceder.
