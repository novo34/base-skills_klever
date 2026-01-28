---
name: deployment-strategy
description: Despliegue seguro y promoción de builds.
---

## Purpose
Minimizar riesgos en el paso a producción.

## Non-negotiables
- Promoción de la misma imagen entre entornos.
- Health checks obligatorios.

## Stop conditions
- Despliegue en producción sin validación previa en staging.

## Required Output
- Status de despliegue y health.

## Verification
- `/health` status OK.
