---
name: skill-priority
description: Define el orden de resolución de conflictos entre skills para garantizar seguridad, estabilidad y consenso.
---

## Purpose
Establecer una jerarquía clara de cumplimiento para evitar ambigüedades, loops e inestabilidad en ejecuciones autónomas y en swarms de agentes.

## Non-negotiables
- **Regla Maestra v6.0**: El Consenso del Swarm y las decisiones bloqueadas (locked) siempre superan el razonamiento o los objetivos de un agente individual.
- Ningún objetivo de autonomía, orquestación o rendimiento puede anular las reglas de seguridad, aprendizaje supervisado o consenso.

## Conflict resolution rule
- Si dos skills entran en conflicto, sigue la de mayor prioridad.
- Las decisiones bloqueadas por consenso son inmutables para agentes individuales.

## Priority order (highest wins)
1. data-classification (02)
2. retention-dsar (03)
3. multi-tenant-data-isolation (04)
4. auth-security (05)
5. request-security (06)
6. logging-security (07)
7. memory-evolution-supervised (32)
8. swarm-consensus-protocol (33)
9. consensus-methods (34)
10. decision-finalization-and-locking (35)
11. human-supervision-escalation (14)
12. agent-lifecycle-control (10)
13. checkpointing-and-state-snapshots (11)
14. agent-memory-governance (12)
15. autonomy-limits-and-budgets (13)
16. reward-alignment-and-anti-gaming (15)
17. orchestration-protocol (16)
18. handoff-contracts (17)
19. shared-state-artifacts (18)
20. parallel-work-conflict-avoidance (19)
21. core-behavior (20)
22. db-migrations-safety (40)
...

## Required Output
- Confirmación de cumplimiento de jerarquía v6.0.

## Verification
- Auditoría de decisiones para asegurar que el consenso prevalece sobre la autonomía individual.
