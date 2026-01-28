---
name: data-classification
description: Clasificación de Datos y Principios de Minimización (Suiza nFADP / revFADP + GDPR).
---

## Data classification (Mandatory)
- **P0: Secretos** (Keys, tokens, passwords). Acceso ultra-restringido.
- **P1: PII** (Nombre, email, IDs). Almacenamiento cifrado y acceso por necesidad.
- **P2: Datos financieros/sensibles**. Máxima restricción.
- **P3: Telemetría**. Datos no identificables.

## Rules
- Minimización: Guardar solo lo estrictamente necesario para el propósito definido.
- Separación: Mantener PII separado de datos operativos si la arquitectura lo permite.
- Cross-tenant leakage: Cualquier fuga entre inquilinos es un bug bloqueante.

## Required Artifacts
- `DATA_MAP.md`: Registro de qué datos se procesan y por qué.
