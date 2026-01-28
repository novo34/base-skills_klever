---
name: architecture-adr-boundaries
description: Gestión de decisiones arquitectónicas y límites.
---

## Purpose
Mantener la salud arquitectónica mediante documentación y separación de capas.

## Non-negotiables
- Decisiones críticas en `/docs/adr/`.
- Separación estricta UI/App/Infra.

## Stop conditions
- Lógica de negocio en componentes de cliente o acceso directo a DB desde UI.

## Required Output
- ADR actualizado o creado.

## Verification
- Revisión de límites de dominio.
