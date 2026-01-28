---
name: i18n-next-intl
description: Internacionalización estricta con next-intl. Cero strings hardcoded. Formateo locale-aware.
---

## Non-negotiables
- Prohibido hardcodear strings visibles al usuario.
- Todas las strings deben ir en messages (keys).
- Formato locale-aware para fechas, números, moneda.

## next-intl rules
- Definir locales soportados y default locale.
- Namespaces por dominio (ej: `common`, `auth`, `billing`).
- Mantener keys consistentes y semánticas (no `text1`).

## Validation
- Si se añade UI nueva:
  - añadir keys en locale default
  - añadir keys en el resto de locales (o fallback documentado)
- Prohibido enviar a producción con keys faltantes.

## Required output
- Keys añadidas/modificadas
- Archivos de locale tocados
- Nota si hay copy pendiente
