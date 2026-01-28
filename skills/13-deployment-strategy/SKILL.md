---
name: deployment-strategy
description: Estrategias de Despliegue Seguro, Entornos y Health Checks.
---

## Purpose
Garantizar despliegues reproducibles y seguros mediante la validación post-despliegue y la promoción de builds.

## Non-negotiables
- Despliegue reproducible basado en la misma build para todos los entornos.
- Validación obligatoria mediante Health Checks post-despliegue.

## Stop conditions
- Si el Health Check falla en staging, bloquear promoción a producción.
- Si hay inconsistencias en las variables de entorno detectadas al arranque.

## Required Output
- Estado del despliegue en cada entorno.
- Resultados de los Health Checks.
- Confirmación de integridad de variables `env`.

## Verification
- Endpoint `/health` responde satisfactoriamente.
- Homepage y APIs críticas verificadas manualmente o vía smoke tests.
