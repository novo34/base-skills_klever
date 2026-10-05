---
name: living-document-governance
description: Mantiene documentación canónica alineada con requisitos, decisiones, backlog, código, tests y evidencia.
---

## Purpose
Evitar drift entre PRD, SPEC, ADR, ROADMAP, backlog y estado real del sistema.

## Non-negotiables
- Un cambio material calcula primero qué artefactos canónicos afecta.
- Documentación no se actualiza como texto aislado sin trazabilidad al requisito/decisión.
- Un release se bloquea si existe drift que invalida requisitos vigentes.
- Cambios triviales sin impacto documental no fuerzan documentación innecesaria.
- Cada actualización documental es versionada y evidence-linked.

## Required Output
Producir DocumentationImpact con:
- change_id
- affected_artifacts[]
- required_updates[]
- optional_updates[]
- no_change_rationale[]
- trace_links[]
- drift_findings[]

## Stop conditions
- Requisito vigente contradice documentación canónica.
- Un artefacto obligatorio afectado queda sin actualización o justificación.
- No puede determinarse cuál es la versión canónica.

## Verification
- PRD/SPEC/ADR/ROADMAP/backlog relevantes describen el mismo comportamiento.
- La ausencia de actualización está justificada cuando no existe impacto.
- CI puede detectar drift estructural verificable.
