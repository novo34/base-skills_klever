# Klever Base Skills Framework 🧠

Este repositorio contiene el framework de control y comportamiento para agentes de IA de Klever. Está diseñado bajo los más altos estándares de seguridad, privacidad y excelencia técnica, siguiendo principios de "IA Constitucional" y control determinista.

## 🚀 Filosofía

No nos limitamos a "dar instrucciones". Este repositorio define una **Constitución Operativa** que obliga a los agentes a actuar con seguridad, transparencia y rigor técnico.

## 🏗️ Estructura del Framework (25 Módulos)

El sistema está organizado jerárquicamente para garantizar que las reglas de seguridad y legalidad siempre tengan prioridad sobre la implementación funcional.

### 🛡️ Nivel 0: Control y Seguridad Base
- `00-skill-priority`: Resolución de conflictos (Jerarquía Maestra).
- `01-preflight-check`: Análisis mandatorio de riesgos antes de ejecutar.
- `02-core-behavior`: Reglas de comportamiento incremental y claridad.

### ⚙️ Nivel 1: Estándares y Despliegue
- `03-stack-standards`: Stack fijo (Next.js, Prisma, pnpm, shadcn).
- `04-git-workflow`: Convenciones de Git y SemVer.
- `05-ci-quality-gates`: Puertas de calidad en CI (Lint, Test, Build).
- `06-deployment-strategy`: Entornos y Health Checks.
- `07-recovery-rollback`: Planes de emergencia y restauración.
- `08-env-secrets`: Gestión segura de variables y secretos.

### 🔒 Nivel 2: Seguridad y Protección de Datos
- `10-auth-security`: Autenticación y Sesiones robustas.
- `11-request-security`: Validación de inputs (Zod) y mitigación de ataques.
- `12-logging-security`: Redacción de PII y trazabilidad segura.
- `20-data-classification`: Clasificación P0-P3 (nFADP/GDPR).
- `21-retention-dsar`: Retención y derechos de datos.

### 🛠️ Nivel 3: Desarrollo y Operaciones
- `13-observability`: Logs estructurados y métricas.
- `14-supply-chain`: Auditoría de dependencias.
- `15-architecture`: ADRs y límites de dominio.
- `16-performance`: Presupuestos de rendimiento.
- `30-db-migrations`: Migraciones seguras (Expand/Contract).
- `40-backend-api`: Contratos OpenAPI y consistencia.
- `50-frontend-nextjs`: Arquitectura App Router.
- `60-ui-ux-modern`: Sistema de diseño shadcn.
- `70-i18n`: Internacionalización estricta.
- `80-code-review`: Puertas de calidad para PRs.
- `17-runbooks`: Guías operativas paso a paso.

---

## 🛠️ Cómo usar este repo
Este repositorio debe estar disponible para el agente en su contexto de trabajo. El agente debe consultar `00-skill-priority` y `01-preflight-check` como primer paso en cada tarea.

---
**Desarrollado por Klever - Senior AI Architecture Team.**
