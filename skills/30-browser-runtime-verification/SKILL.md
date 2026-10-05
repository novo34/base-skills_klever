---
name: browser-runtime-verification
description: Define evidencia de navegador y runtime para verificar comportamiento real, no solo compilación o tests aislados.
---

## Purpose
Demostrar que cambios de UI y flujos integrados funcionan en un entorno ejecutable y detectar fallos visibles únicamente en runtime.

## Non-negotiables
- Cambios visuales o browser-dependent no se verifican solo con build verde.
- Capturar errores de consola y fallos de red relevantes.
- Verificar el flujo de usuario afectado y sus estados críticos.
- La evidencia debe identificar versión/commit y entorno.
- Foundation define el contrato; la ejecución real del browser corresponde a Platform/adaptador autorizado.

## Evidence types
Cuando apliquen:
- page_load
- target_state
- interaction_flow
- responsive_state
- console_errors
- network_failures
- accessibility_signal
- screenshot_or_visual_evidence
- backend_response
- persistence_confirmation

## Required Output
- environment
- commit_or_artifact
- flow_steps[]
- assertions[]
- console_findings[]
- network_findings[]
- visual_evidence[]
- result
- limitations[]

## Stop conditions
- Entorno no corresponde al artefacto revisado.
- Evidencia obsoleta o de commit distinto.
- Error crítico de consola/red relacionado con el cambio.
- Un criterio visual no fue inspeccionado.

## Verification
- Cada criterio browser-dependent tiene una assertion/evidencia.
- Los hallazgos negativos no se ocultan.
- El Verifier puede reproducir o inspeccionar la evidencia.
