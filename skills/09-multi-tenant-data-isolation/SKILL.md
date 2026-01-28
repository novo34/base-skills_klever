---
name: multi-tenant-data-isolation
description: Aislamiento estricto de datos multi-tenant en sistemas con agentes paralelos.
---

## Purpose
Prevenir el acceso, la mutación o la fuga de datos entre inquilinos (cross-tenant) en ejecuciones paralelas y multi-agente.

## Non-negotiables
- Todo acceso a datos debe estar explícitamente limitado por el identificador de inquilino (tenant identifier).
- Los agentes no deben asumir un contexto de inquilino implícito.
- Los servicios compartidos deben imponer el aislamiento a nivel de consulta y API.

## Stop conditions
- Si el contexto del inquilino no está claro o es implícito, detenerse y pedir aclaración.
- Si un cambio pone en riesgo el impacto cross-tenant, detenerse y escalar.

## Required Output
- Estrategia de limitación por inquilino:
  - Dónde se inyecta el `tenantId`.
  - Cómo se valida.
- Lista de consultas/endpoints afectados por el cambio.

## Verification
- Las consultas no pueden acceder a datos de otro inquilino.
- Pruebas o razonamiento lógico confirman el aislamiento.
