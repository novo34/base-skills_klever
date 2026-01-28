---
name: architecture-adr-boundaries
description: Arquitectura: Límites de dominio, Separación de Responsabilidades y ADRs.
---

## Purpose
Mantener la integridad estructural del software mediante la definición clara de límites y la documentación de decisiones críticas.

## Non-negotiables
- Toda decisión arquitectónica que afecte a más de un módulo debe documentarse en un ADR.
- Respetar la separación entre UI, Aplicación (casos de uso) e Infraestructura.

## Stop conditions
- Si se detecta lógica de negocio compleja acoplada a componentes de UI.
- Si se intenta acceder a la base de datos directamente desde el cliente.

## Required Output
- Nuevo ADR creado en `docs/adr/` (si aplica).
- Diagrama o descripción breve del flujo de datos entre capas.

## Verification
- Revisión de código confirmando que no hay violaciones de límites (boundaries).
