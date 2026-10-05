---
name: skill-priority
description: Define el orden de resolución de conflictos entre skills para garantizar seguridad, estabilidad, trazabilidad y adaptación controlada.
---

## Purpose
Establecer una jerarquía de cumplimiento para evitar que autonomía, aprendizaje, optimización o workflows adaptativos anulen seguridad y gobernanza.

## Non-negotiables
- Las políticas de seguridad, autorización, aislamiento de datos, auditoría y aprobación humana prevalecen sobre objetivos de ejecución.
- Decisiones LOCKED y gates obligatorios prevalecen sobre razonamiento de agentes individuales.
- Adaptive workflow, learning y self-improvement nunca pueden reducir un control superior.
- Riesgo puede elevar profundidad/gates; nunca reducirlos.

## Conflict resolution rule
- Si dos skills entran en conflicto, sigue la de mayor prioridad del manifest.
- Las restricciones estructurales del runtime/policy prevalecen sobre instrucciones Markdown.
- Una decisión locked solo puede cambiar mediante el proceso autorizado de reapertura/supersesión.

## Priority families (highest safety intent first)
1. Data/privacy/tenant/auth/request/logging security.
2. Human supervision, audit, risk and protected decisions.
3. Memory/learning/self-improvement governance.
4. Agent lifecycle, budgets, orchestration, handoffs and shared state.
5. Intent/spec/planning/context and adaptive workflow controls.
6. Git/CI/architecture/deployment/rollback.
7. Capability/artifact/document/decision governance.
8. Implementation/review/repository hygiene/reuse.
9. Stack/domain-specific skills.

The exact machine-readable ordering is the unique integer `priority` in `skills-manifest.yaml`.

## Required Output
- Confirmación de que la selección de skills respeta manifest, risk policy y gates estructurales.

## Stop conditions
- Conflicto no resoluble entre dos controles de igual autoridad.
- Una skill intenta rebajar un gate definido por policy/runtime.
- Una mejora intenta modificar un control protegido sin proceso autorizado.

## Verification
- CI valida manifest/agent references.
- Adaptive validators verifican contratos críticos.
- Tests negativos demuestran que bypasses relevantes fallan.
