---
name: ui-ux-modern-system
description: UI moderna, elegante y consistente usando shadcn/ui + Tailwind. UX con estados completos y accesibilidad básica.
---

## Non-negotiables (UI)
- Usar componentes shadcn/ui para patrones comunes (Button, Input, Dialog, Table, Dropdown, Toast).
- Consistencia visual: spacing scale, typography scale, radius consistente.
- Responsive: layouts deben adaptarse a móvil/desktop.
- Nada de “pantalla vacía”: siempre empty/loading/error.

## Non-negotiables (UX)
- Formularios:
  - label, placeholder útil, validación inline, mensajes claros, estado success/fail.
- Feedback:
  - toasts/alerts coherentes
  - disabled states mientras carga
- Navegación:
  - el usuario siempre entiende “qué sigue”.

## Accessibility basics
- Focus visible
- Labels asociados
- `aria-*` cuando sea necesario (dialogs, menus)
- Keyboard nav básico (tab/enter/esc en modales)

## Visual quality gates
- Tipografía jerárquica (H1/H2/body)
- Alineación y grid primero
- No más de 2–3 variantes de card/surface
- Iconos consistentes (lucide)

## Required output for UI changes
- Screenshot o descripción de estados (loading/error/empty)
- Lista de componentes shadcn usados
