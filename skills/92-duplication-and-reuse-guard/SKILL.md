---
name: duplication-and-reuse-guard
description: Impide crear superficies duplicadas sin buscar antes equivalentes reutilizables o extensibles.
---

## Purpose
Prevenir duplicación antes de que entre al repositorio.

## Non-negotiables
- Antes de crear función, clase, componente, servicio, endpoint o archivo buscar equivalentes.
- Evaluar coincidencia por responsabilidad y comportamiento, no solo por nombre.
- Preferir REUSE o EXTEND cuando preserve límites y claridad.
- CREATE_NEW necesita rationale y evidencia de por qué los candidatos no sirven.
- Duplicación injustificada bloquea completion.

## Required Output
Producir ReuseDecision con:
- proposed_surface
- candidates[]
- similarity_evidence[]
- decision
- selected_candidate
- rationale

decision:
- REUSE
- EXTEND
- CREATE_NEW
- BLOCK_DUPLICATE

## Stop conditions
- Existe equivalente fuerte sin rationale para crear otro.
- No se realizó búsqueda source-grounded.
- La nueva superficie solo replica código legacy con otro nombre.

## Verification
- CreationDecision referencia búsqueda previa.
- BLOCK_DUPLICATE impide crear el archivo/símbolo.
- Reuse no fuerza acoplamiento incorrecto: si límites son distintos, CREATE_NEW puede justificarse.
