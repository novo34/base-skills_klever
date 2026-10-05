---
name: artifact-conversation-and-review
description: Permite conversar, anotar y revisar artefactos versionados con decisiones explícitas de aprobación.
---

## Purpose
Convertir PRD, SPEC, ROADMAP, ADR, planes, evidencia, UI y propuestas de mejora en superficies revisables sin perder contexto ni historial.

## Non-negotiables
- Todo comentario referencia artefacto, revisión y selector/fragmento concreto cuando aplique.
- Las revisiones previas nunca se sobrescriben.
- El chat puede proponer una nueva revisión, pero no inferir aprobación.
- APPROVE, REQUEST_CHANGES y REJECT son transiciones explícitas.
- Comentarios resueltos permanecen auditables.

## Required Output
Producir ArtifactReview con:
- artifact_id
- revision
- comments[]
- decision
- decided_by
- resulting_revision

## Stop conditions
- Comentario apunta a una revisión inexistente.
- Se intenta aprobar una revisión distinta de la inspeccionada.
- Falta autoridad humana cuando la política exige aprobación.

## Verification
- Cada decisión referencia la revisión exacta.
- Los cambios solicitados generan nueva revisión en vez de mutar la anterior.
- El historial comentario -> cambio -> decisión es reconstruible.
