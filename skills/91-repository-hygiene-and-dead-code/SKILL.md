---
name: repository-hygiene-and-dead-code
description: Detecta y clasifica código muerto, archivos huérfanos, artefactos temporales y dependencias sin uso antes de eliminarlos.
---

## Purpose
Evitar acumulación de basura y código obsoleto sin borrar de forma insegura recursos dinámicos o generados.

## Non-negotiables
- Integrar con 09-artifact-lifecycle-and-cleanup; no duplicar su lifecycle.
- Ningún candidato se elimina solo porque no tenga referencias estáticas.
- Clasificar cada candidato como SAFE_TO_DELETE, LIKELY_DEAD, POSSIBLY_DYNAMIC, GENERATED_REQUIRED, TEST_ARTIFACT o UNKNOWN.
- Identificar temporales/debug, huérfanos, dependencias no usadas, generated drift y TODO/FIXME obsoletos.
- Eliminaciones de riesgo respetan aprobación, rollback y verifier independiente.

## Required Output
Producir HygieneReport con:
- dead_code_candidates[]
- orphan_files[]
- temporary_artifacts[]
- unused_dependencies[]
- stale_todos[]
- generated_drift[]
- classifications[]
- cleanup_debt_score

## Stop conditions
- Código usa reflection, configuración, rutas dinámicas, plugins o carga indirecta y no se ha verificado.
- El candidato afecta datos/migraciones/producción sin gate apropiado.
- No existe evidencia suficiente para clasificar SAFE_TO_DELETE.

## Verification
- Cada eliminación está ligada a una clasificación y evidencia.
- El tree final no conserva temporales creados por la tarea salvo promoción explícita.
- El debt delta no aumenta sin justificación.
