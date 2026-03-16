---
name: dokploy-deploy-guardrails
description: Crear o actualizar artefactos de despliegue para Dokploy con foco en seguridad operativa, control de disco, separación entre servicios ligeros y pesados, mapeo explícito de dominios, separación estricta entre URLs internas y públicas, y guías de limpieza y validación. Usar cuando Codex genere o modifique docker-compose.dokploy.yml, dokploy.env.example, plantillas .env para Dokploy, DEPLOY_Dokploy*.md, Dockerfiles usados por servicios desplegados en Dokploy, o documentación técnica de despliegue Dokploy como PRD, SPEC, ADR o checklists.
---

## Purpose
Diseñar despliegues Dokploy listos para producción en VPS con disco limitado, evitando rebuilds costosos, crecimiento innecesario de imágenes y errores de configuración entre dominios públicos, puertos internos y servicios reales.

## Non-negotiables
- Tratar Dokploy como un entorno productivo con disco limitado, típicamente 80-100 GB.
- Minimizar rebuilds y tamaño de imagen cuando Dokploy redeploya servicios.
- Separar explícitamente servicios ligeros y servicios pesados.
- Mantener separadas las URLs internas de Docker/Compose y las URLs públicas.
- Mapear cada dominio público al servicio correcto, con puerto interno y expectativa HTTPS explícitos.
- Incluir siempre guía de `.dockerignore` para `node_modules`, `.git`, `.env*`, artefactos de build, cachés, temporales y media generada no necesaria en la imagen.
- Preferir instalaciones deterministas: `npm ci`, versiones fijadas cuando aplique y `pip --no-cache-dir`.
- Incluir política de limpieza de build cache e imágenes en toda guía Dokploy.

## Heavy vs Light Services
- Tratar como light services: frontend, dashboard, API Node, app web y servicios sencillos.
- Tratar como heavy services: Torch, Diffusers, Transformers, Accelerate, FFmpeg-heavy, OCR, CV, TTS, runtimes Python de media y generación de imagen/video.
- Optimizar para que cambios en servicios ligeros no obliguen a reconstruir servicios pesados salvo necesidad real.

## Build Strategy
- Para servicios pesados, preferir una base prebuild con dependencias pesadas ya instaladas.
- Como alternativa, preferir `image:` con una imagen remota fijada si evita rebuilds repetidos en Dokploy.
- Si el usuario pide un único stack, mantener el stack único pero aislar la lógica de imagen pesada y advertir el coste de redeploy.
- Para Node, preferir `npm ci --omit=dev` en imágenes de producción.
- Para Python, preferir capas separadas, `venv` dedicada cuando ayude y `pip install --no-cache-dir`.

## Runtime and Readiness
- Evaluar si `preload at startup` debe quedar desactivado por defecto en servicios ML locales pesados.
- Evitar readiness estricta basada en carga completa de modelo si el despliegue es CPU-only o puede colgarse.
- Explicar explícitamente las limitaciones de CPU-only para FLUX, Diffusers u otros modelos similares.

## Required Output
Incluir siempre, cuando sea relevante:
- Resumen de arquitectura con lista de servicios.
- Tabla de domain mapping con `service name`, `public domain`, `internal port` y `HTTPS expected`.
- Separación de variables de entorno: URLs públicas, URLs internas, secretos, storage, credenciales AI y credenciales de base de datos.
- Estrategia de almacenamiento para media generada, priorizando R2/S3 u object storage externo sobre disco persistente local.
- Sección de disk protection con capas grandes, puntos probables de crecimiento, comandos de cleanup y estrategia preventiva.
- Sección de redeploy behavior explicando qué servicios reconstruyen a menudo y cuáles no deberían hacerlo.
- Sección de validation con checks de env, health, readiness y conectividad entre servicios.

## Required Commands
Incluir como comandos recomendados de mantenimiento:

```bash
docker builder prune -a -f
docker image prune -a -f
```

- No recomendar `docker system prune -a -f --volumes` como acción inicial.
- Si se menciona limpieza más agresiva, advertir explícitamente del riesgo sobre volúmenes activos.
- Mencionar cron o systemd timer cuando una limpieza programada tenga sentido.

## Stop Conditions
Detenerse y corregir la salida si ocurre cualquiera de estos casos:
- Un dominio público apunta al servicio incorrecto.
- Se mezclan URLs internas `http://service:port` con URLs públicas `https://domain`.
- Se ignoran los rebuilds pesados de ML/media.
- Se almacena media generada a largo plazo en el VPS sin justificación explícita.
- Falta la política de cleanup.
- No está identificado cuál servicio es la app o frontend de cara al usuario.
- La estrategia de readiness es poco realista para un VPS CPU-only.

## Final Check
Antes de finalizar, verificar:
- Las URLs internas y públicas están separadas correctamente.
- Los dominios públicos coinciden con el servicio y puerto correctos.
- Los servicios pesados están optimizados para disco y rebuild.
- La media durable no se acumula en el VPS si existe object storage.
- El coste de rebuild y crecimiento de disco está documentado.
- Existe un plan de limpieza y mantenimiento.
- Se explican honestamente las limitaciones CPU-only.

## Reusable Instruction
Aplicar esta regla en cualquier tarea Dokploy:

> Tratar Dokploy como un VPS productivo con disco limitado. Separar capas pesadas del código cambiante, minimizar rebuilds, mantener separadas las URLs internas y públicas, mapear dominios explícitamente, evitar almacenar media durable en el VPS cuando haya object storage y añadir siempre estrategia de limpieza y mantenimiento.
