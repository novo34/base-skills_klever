---
name: architecture-adr-boundaries
description: Arquitectura: Límites de dominio, Separación de Responsabilidades y ADRs.
---

## Rules
- Decisiones críticas se registran en `docs/adr/`.
- Separación de responsabilidades: UI, App (casos de uso), Infra (DB/External).
- Prohibido acceso directo a DB desde componentes UI.

## Required Artifacts
- `docs/adr/README.md`
