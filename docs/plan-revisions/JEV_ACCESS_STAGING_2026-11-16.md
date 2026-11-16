# PlanRevision · Acceso a JEV Staging

Estado propuesto. Las tareas quedan TODO para revisión del operador.

## Evidencia

Durante la aceptación de PLT-010 hubo que restablecer manualmente la contraseña del administrador. La interfaz pierde la sesión al recargar o volver desde GitHub. El formulario carece del flujo de recuperación por correo. La [PR de aceptación](https://github.com/novo34/SaSS_Workee/pull/4) quedó fusionada en el repositorio de prueba.

## Cambios propuestos

- INSERT `PLT-050` antes de `PLT-011` para corregir la persistencia de sesión.
- INSERT `PLT-051` después de `PLT-050` para habilitar recuperación por correo.
- Mantener las dependencias existentes de `PLT-011`. Si se integra esta propuesta, el orden canónico sitúa primero las dos tareas de acceso. Cada inicio se rige por NEXT_TASK.

La recuperación depende de identificar y configurar un proveedor de envío para staging. La entrega real y los casos de caducidad, reutilización y aislamiento son parte de la aceptación. La revisión de esta propuesta solo cambia planificación.

## Metadatos e impacto de la revisión

- `actor`: Codex, autor de la propuesta en nombre del operador de JEV.
- `dependency_impact`: PLT-050 depende de PLT-004 y PLT-010. PLT-051 depende de PLT-004 y PLT-050. PLT-011 conserva sus dependencias PLT-006 y PLT-010. Su posición en NEXT_TASK cambia por el orden de declaración.
- `risk_impact`: R2 por modificar el plan. Los cambios de autenticación se evaluarán como R3 al implementarse.
- `budget_impact`: Se añade el esfuerzo de dos tareas. El coste de implementación y de envío de correo queda por estimar. Esta propuesta no asigna presupuesto ni contrata servicios.
