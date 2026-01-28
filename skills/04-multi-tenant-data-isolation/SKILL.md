---
name: multi-tenant-data-isolation
description: Aislamiento estricto de datos multi-tenant en sistemas con agentes paralelos.
---

## Purpose
Prevenir la fuga de datos entre inquilinos en ejecuciones paralelas y multi-agente.

## Non-negotiables
- El acceso a datos debe estar siempre filtrado por `tenantId` de forma explícita.
- El sistema debe validar el contexto del inquilino en cada capa de la API.

## Stop conditions
- Consultas a base de datos que no incluyan el filtro de inquilino.

## Required Output
- Estrategia de aislamiento inyectada.
- Lista de consultas verificadas.

## Verification
- Pruebas cruzadas: Un usuario del Tenant A no puede acceder a recursos del Tenant B.
