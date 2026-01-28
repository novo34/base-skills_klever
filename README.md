# Klever Base Skills Framework 🧠 (v4.0 - Multi-Agent Ready)

Este repositorio contiene el framework de control, comportamiento y **gobernanza** para agentes de IA de Klever. La versión 4.0 introduce el **Protocolo de Orquestación**, diseñado para permitir que múltiples agentes trabajen en paralelo de forma segura y coordinada.

## 🚀 Filosofía

Este framework define una **Constitución Operativa** de grado industrial. No solo guía el comportamiento individual, sino que establece contratos, handoffs y estados compartidos para evitar loops, duplicaciones y conflictos en ejecuciones multi-agente.

## 🏗️ Estructura del Framework (v4.0)

Organización jerárquica por capas de prioridad (Seguridad > Orquestación > Desarrollo).

### 🛡️ Nivel 0: Gobernanza y Control Maestro
- `00-skill-priority`: Resolución de conflictos (Seguridad > Orquestación > Dev).
- `01-preflight-check`: Análisis de riesgos y **Multi-Agent Workplan** mandatorio.
- `02-core-behavior`: Comportamiento base y **Definition of Done (DoD)** multi-agente.

### 🌐 Nivel 1: Protocolos de Orquestación (v4.0)
- `03-orchestration-protocol`: Roles, fases e integración controlada.
- `04-handoff-contracts`: Contratos de traspaso estandarizados.
- `05-shared-state-artifacts`: Fuente de verdad única (`STATE.md`, `DECISIONS.md`).
- `06-parallel-work-conflict-avoidance`: Propiedad de archivos y bloqueos (locks).

### ⚙️ Nivel 2: Estándares y Despliegue
- `07-stack-standards`: Stack fijo (Next.js, Prisma, pnpm, shadcn).
- `08-git-workflow`: Convención de commits y flujos de PR.
- `09-ci-quality-gates`: Puertas de calidad automatizadas.
- `13-deployment-strategy`: Entornos y Health Checks.
- `14-recovery-rollback`: Planes de emergencia.
- `15-env-secrets`: Gestión de secretos.

### 🔒 Nivel 3: Seguridad y Datos
- `10-auth-security`: Autenticación robusta.
- `11-request-security`: Validación de inputs (Zod).
- `12-logging-security`: Redacción de PII.
- `21-data-classification`: Privacidad suiza (nFADP/GDPR).
- `22-retention-dsar`: Retención y derechos ARCO.

### 🛠️ Nivel 4: Desarrollo y Ops
- `16-observability`: Telemetría y logs.
- `17-supply-chain`: Auditoría de dependencias.
- `18-architecture`: ADRs y límites de dominio.
- `19-performance`: Presupuestos de rendimiento.
- `20-runbooks`: Guías operativas.
- `30-db-migrations`: Migraciones seguras.
- `40-backend-api`: OpenAPI y contratos REST.
- `50-frontend-nextjs`: App Router architecture.
- `60-ui-ux-modern`: Sistema de diseño shadcn.
- `70-i18n`: Internacionalización estricta.
- `80-code-review`: Calidad de código.

---

## 🛠️ Orquestación de Agentes
En cada nueva tarea, el sistema debe generar la carpeta de estado:
- `docs/orchestration/WORKPLAN.md`
- `docs/orchestration/STATE.md`
- `docs/orchestration/HANDOFFS.md`
- `docs/orchestration/DECISIONS.md`

---
**Desarrollado por Klever - Senior AI Architecture Team.**
