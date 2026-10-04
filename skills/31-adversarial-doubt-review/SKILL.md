---
name: adversarial-doubt-review
description: Revisa activamente una entrega intentando encontrar contraejemplos, requisitos omitidos y evidencia insuficiente.
---

## Purpose
Combatir confirmación prematura: el Verifier debe intentar demostrar que la solución está incompleta o equivocada antes de aceptarla.

## Non-negotiables
- Separar PROVEN, SUPPORTED, ASSUMED y UNKNOWN.
- Buscar al menos contraejemplos razonables para requisitos críticos.
- Revisar requisitos no tocados que puedan sufrir regresión por el cambio.
- No convertir ausencia de fallo observado en prueba de corrección.
- Duda crítica sin resolver bloquea aprobación.

## Adversarial checks
- ¿Qué caso límite invalida la implementación?
- ¿Qué requisito quedó sin evidencia?
- ¿Qué supuesto podría ser falso?
- ¿Qué código viejo sigue activo?
- ¿Qué camino de error no fue probado?
- ¿Qué dependencia/contexto podría estar obsoleto?
- ¿Qué comportamiento cambia accidentalmente?

## Required Output
- claims[]
- evidence_strength[]
- counterexamples_tested[]
- missing_evidence[]
- hidden_regressions[]
- unresolved_doubts[]
- verdict

verdict debe ser uno de:
- VERIFIED
- FAILED
- BLOCKED

## Stop conditions
- Evidencia crítica inexistente.
- Contradicción entre implementación y AcceptanceContract.
- Incertidumbre material imposible de resolver dentro del scope autorizado.

## Verification
- Todo VERIFIED crítico está respaldado por evidencia.
- Los contraejemplos significativos fueron evaluados.
- La revisión es independiente del implementador cuando la política lo exige.
