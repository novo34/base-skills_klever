---
name: i18n-next-intl
description: Internacionalización estricta con next-intl. Cero strings hardcoded. Formateo locale-aware.
---

## Purpose
Hacer la aplicación accesible globalmente mediante una internacionalización rigurosa y correcta gestión de locales.

## Non-negotiables
- Prohibición de cadenas de texto (strings) visibles al usuario directamente en el código.
- Uso de formateadores locale-aware para fechas, números y monedas.

## Stop conditions
- Si se añade una nueva funcionalidad de UI sin sus correspondientes traducciones en los locales soportados.

## Required Output
- Lista de nuevas llaves (keys) añadidas a los archivos de mensajes JSON.
- Confirmación de los locales actualizados.

## Verification
- Cambio de idioma verificado manualmente en la aplicación.
- `pnpm lint` para asegurar que no hay strings hardcoded (si hay reglas de lint configuradas para ello).
