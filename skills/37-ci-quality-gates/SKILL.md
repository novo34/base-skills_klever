---
name: ci-quality-gates
description: Puertas de calidad automatizadas.
---

## Purpose
Automatizar la prevención de errores antes de la integración.

## Non-negotiables
- El CI debe bloquear el merge si falla lint, tests o build.

## Stop conditions
- Desactivación de gates de CI para acelerar entregas.

## Required Output
- Estado del pipeline de CI.

## Verification
- Green build en todas las PRs.
