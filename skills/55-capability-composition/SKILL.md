---
name: capability-composition
description: Compone capacidades técnicas sobre roles de autoridad estables sin crear agentes especializados redundantes.
---

## Purpose
Mantener pocos roles de autoridad y añadir únicamente las capacidades necesarias para cada tarea.

## Non-negotiables
- Rol y capacidad son conceptos separados.
- Una capacidad nunca amplía permisos por encima del rol o política.
- No crear nuevos roles solo por lenguaje, framework o proveedor.
- Las capacidades deben estar declaradas y disponibles en el harness seleccionado.
- La composición debe ser mínima y trazable.

## Required Output
Producir CapabilityComposition con:
- task_id
- role
- requested_capabilities[]
- granted_capabilities[]
- denied_capabilities[]
- permission_ceiling[]
- rationale[]

## Stop conditions
- Una capacidad solicita permisos no concedidos al rol.
- La capacidad requerida no está disponible.
- La composición depende de un proveedor/harness sin capability contract.

## Verification
- granted_capabilities es subconjunto de capacidades disponibles y autorizadas.
- Ningún permiso efectivo excede permission_ceiling.
- La misma necesidad técnica no requiere proliferar roles.
