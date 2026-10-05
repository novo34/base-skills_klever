---
name: code-simplification
description: Reduce complejidad, duplicación y deuda manteniendo el comportamiento demostrado.
---

## Purpose
Asegurar que refactors y nuevas implementaciones dejan una base más simple en lugar de acumular soluciones paralelas y legado abandonado.

## Non-negotiables
- Preservar comportamiento requerido mediante tests/evidencia.
- Eliminar código sustituido o justificar explícitamente compatibilidad/transición.
- No crear abstracciones sin al menos una necesidad concreta.
- No mezclar simplificación con cambios funcionales no autorizados.
- La complejidad o duplicación no puede aumentar sin justificación aprobada.

## Cleanup accounting
Todo refactor debe declarar:
- added[]
- replaced[]
- removed[]
- retained_for_compatibility[]
- follow_up_cleanup[]

Si existe replaced sin removed ni justificación válida, el resultado es INCOMPLETE_CLEANUP.

## Required Output
- behavior_preserved_evidence
- complexity_before_after
- duplication_before_after
- cleanup_accounting
- compatibility_justifications[]
- residual_debt[]

## Stop conditions
- No hay cobertura suficiente para demostrar preservación.
- Código aparentemente muerto puede ser dinámico/reflection/config-driven y no ha sido analizado.
- La simplificación rompe un contrato público.

## Verification
- Tests/evidencia antes y después.
- No quedan implementaciones antiguas "por si acaso".
- El diff final es más simple o la excepción está justificada.
