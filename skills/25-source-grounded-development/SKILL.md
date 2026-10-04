---
name: source-grounded-development
description: Obliga a desarrollar desde evidencia del repositorio, contratos y decisiones existentes antes de crear nuevas superficies.
---

## Purpose
Reducir invención, duplicación, incompatibilidades y refactors innecesarios mediante investigación previa y reutilización consciente.

## Non-negotiables
- Buscar implementación existente antes de crear archivo, función, componente, servicio, endpoint o abstracción.
- Leer los contratos/documentos relevantes antes de modificar comportamiento.
- Preferir extender/reutilizar cuando mantiene claridad y límites correctos.
- Toda nueva superficie significativa debe tener una razón.
- Registrar la procedencia de decisiones que condicionan la implementación.

## Grounding order
1. Requisito/AcceptanceContract.
2. Código y tests existentes.
3. Schemas/interfaces/contratos.
4. ADRs y decisiones vigentes.
5. Documentación operativa.
6. Fuentes externas solo cuando sean necesarias y autorizadas.

## Required Output
Producir SourceGrounding con:
- inspected_sources[]
- existing_candidates[]
- reuse_decision
- creation_decisions[]
- compatibility_constraints[]
- provenance_notes[]
- unknowns[]

Cada creation_decision debe indicar:
- proposed_surface
- searched_equivalents
- rationale
- reuse_rejected_because

## Stop conditions
- No se ha investigado la superficie afectada.
- Existe implementación equivalente y no hay justificación para duplicarla.
- Fuente crítica contradictoria sin resolver.

## Verification
- Los cambios pueden vincularse a fuentes concretas.
- La creación de nuevas superficies está justificada.
- No se confunde ausencia de coincidencia textual con ausencia de funcionalidad equivalente.
