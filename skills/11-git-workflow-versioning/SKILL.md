---
name: git-workflow-versioning
description: Workflow profesional Git: branches, conventional commits, PR template, semver y releases.
---

## Purpose
Asegurar un flujo de trabajo de Git consistente, auditable y con cambios trazables mediante lanzamientos estructurados.

## Non-negotiables
- Rama `main` siempre debe estar en estado desplegable.
- Uso obligatorio de ramas de feature/fix/chore.
- Mensajes de commit siguiendo `Conventional Commits`.

## Stop conditions
- Si falta `.github/pull_request_template.md`, detenerse y crear uno mínimo.
- Si los commits no siguen la convención, no proceder sin corregirlos.
- No introducir flujos alternativos (GitFlow, etc.) sin solicitud explícita.

## Required Output
- Nombre de la rama utilizada.
- Mensajes de commit creados o revisados.
- Confirmación del uso de la plantilla de PR.
- Impacto en el versionado (si aplica).

## Verification
- PR creada contra `main`.
- Historial de commits sigue los estándares definidos.
