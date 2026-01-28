# Klever Base Skills Framework 🧠 (v4.1 - Self-Stabilizing Constitution)

Este repositorio contiene el framework de control, comportamiento y **gobernanza auto-estabilizada** para agentes de IA de Klever. La versión 4.1 introduce controles críticos de **idempotencia**, **ciclo de vida de artefactos** y **aislamiento de datos**, asegurando que el sistema sea resistente a fallos, reintentos y paralelismo masivo.

## 🚀 Filosofía: Constitución Auto-Estabilizada

No solo coordinamos agentes; garantizamos que el entorno de desarrollo permanezca limpio, los datos aislados y las ejecuciones sean predecibles (idempotentes), incluso cuando múltiples IAs trabajan en paralelo sobre sistemas multi-tenant complejos.

## 🏗️ Estructura del Framework (v4.1)

Organización jerárquica por capas de prioridad (Seguridad > Estabilidad > Orquestación > Desarrollo).

### 🛡️ Nivel 0: Gobernanza y Estabilidad Maestra
- `00-skill-priority`: Jerarquía absoluta (Seguridad/Datos > Estabilidad > Orquestación).
- `01-preflight-check`: Análisis de riesgos, **Idempotencia** y **Multi-Agent Workplan**.
- `02-core-behavior`: Comportamiento base y **DoD** ultra-estricto.

### 🏛️ Nivel 1: Estabilidad Operativa y Ciclo de Vida (v4.1)
- `07-idempotency-and-retry-control`: Prevención de loops y duplicación de efectos.
- `08-artifact-lifecycle-and-cleanup`: Gestión propietaria y limpieza de archivos.
- `09-multi-tenant-data-isolation`: Aislamiento estricto de datos entre inquilinos.

### 🌐 Nivel 2: Protocolos de Orquestación (v4.0)
- `03-orchestration-protocol`: Roles, fases e integración controlada.
- `04-handoff-contracts`: Contratos de traspaso estandarizados.
- `05-shared-state-artifacts`: Fuente de verdad única (`STATE.md`, `DECISIONS.md`).
- `06-parallel-work-conflict-avoidance`: Propiedad de archivos y bloques (locks).

### ⚙️ Nivel 3: Estándares y Despliegue
- `10-stack-standards`: Stack fijo (Next.js, Prisma, pnpm, shadcn).
- `11-git-workflow`: Convención de commits y flujos de PR.
- `12-ci-quality-gates`: Puertas de calidad automatizadas.
- `16-deployment-strategy`: Entornos y Health Checks.
- `17-recovery-rollback`: Planes de emergencia.
- `18-env-secrets`: Gestión de secretos.

### 🔒 Nivel 4: Seguridad y Datos
- `13-auth-security`: Autenticación robusta.
- `14-request-security`: Validación de inputs (Zod).
- `15-logging-security`: Redacción de PII.
- `24-data-classification`: Privacidad suiza (nFADP/GDPR).
- `25-retention-dsar`: Retención y derechos ARCO.

---

## 🛠️ Cómo operar la v4.1
Cada tarea multi-agente requiere:
1. **Análisis de Idempotencia** en el Preflight.
2. **Definición de Lifecycle** para cada archivo generado.
3. **Escopado explícito de Tenant** en cada acceso a datos.

---
**Desarrollado por Klever - Senior AI Architecture Team.**
