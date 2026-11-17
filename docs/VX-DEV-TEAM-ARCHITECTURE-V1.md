# VX Dev Team V1 — arquitectura del equipo de desarrollo

**Estado:** PROPOSAL / no activa runtime  
**Fecha:** 2026-11-17  
**Objetivo:** definir la estructura humana/lógica del modo global `Dev Team` antes de asignar MCP, permisos o automatizaciones.

## 1. Idea central

`Dev Team` será un **agente primario seleccionable en Kilo** que representa a un equipo de desarrollo de software.

No será un “agente que hace de todo”. Su responsabilidad es actuar como **Team Lead / Technical Lead**, interpretar la solicitud del operador, dividir el trabajo, delegar análisis e implementación especializada, integrar resultados y cerrar la tarea con evidencia.

Kilo permite agentes personalizados con `mode: primary` para mostrarlos en el selector y subagentes con `mode: subagent` para invocarlos mediante `task`. El modo V1 aprovechará ese modelo.

## 2. Principio operativo V1

### Un solo escritor por worktree

La primera versión del equipo mantiene:

- máximo **1 escritor efectivo** por worktree;
- hasta **3 subagentes de lectura/análisis en paralelo**;
- implementación especializada como propuesta/handoff cuando el subagente no pueda obtener aprobación interactiva;
- revisión independiente después de BUILD;
- merge/deploy siempre fuera del alcance automático.

Esto evita conflictos de escritura y mantiene compatibles las reglas actuales del Harness.

## 3. Jerarquía del equipo

```text
Usuario / Operador
      │
      ▼
┌──────────────────────────────┐
│ DEV TEAM                     │
│ Team Lead / Technical Lead   │
│ agente primario              │
└──────────────┬───────────────┘
               │
     ┌─────────┼───────────┐
     │         │           │
     ▼         ▼           ▼
 Analysis   Implementation  Verification
     │         │           │
     │         │           │
     ├─ Research            ├─ QA Analyst
     ├─ Architecture        ├─ QA Builder
     └─ UX/Security         └─ Code Reviewer
               │
               ├─ Frontend Engineer
               ├─ Backend Engineer
               ├─ Data Engineer
               └─ Docs Engineer
```

## 4. Rol principal — Dev Team Lead

### Identidad técnica propuesta

- **ID futuro:** `dev-team`
- **Modo Kilo:** `primary`
- **Base reutilizable:** capacidades actuales de `vx-integrador`
- **Función:** Team Lead + Technical Lead + Integrador

### Responsabilidades

1. recibir la solicitud del usuario;
2. identificar objetivo, alcance, riesgos y criterios de aceptación;
3. elegir el perfil técnico correcto;
4. dividir la tarea en subtareas;
5. asignar especialistas;
6. asegurar que las interfaces entre subtareas estén definidas;
7. mantener un único escritor por worktree;
8. integrar los resultados;
9. pedir revisión independiente;
10. ejecutar o coordinar pruebas autorizadas;
11. preparar commit/PR cuando corresponda;
12. informar lo verificado, pendiente y bloqueado.

### Lo que NO debe hacer

- autoaprobar sus propios cambios;
- ejecutar producción sin autorización;
- conceder permisos a otros agentes;
- instalar MCP o skills silenciosamente;
- crear múltiples escritores sobre el mismo worktree;
- confundir una propuesta de subagente con un cambio realmente aplicado.

## 5. Núcleo del equipo V1

La primera versión no necesita decenas de roles activos. Se propone un **núcleo de siete funciones**.

### 5.1 Software Analyst / Research Engineer

**Base actual:** `vx-researcher`

Responsabilidades:

- investigar el codebase;
- localizar dependencias;
- recuperar documentación técnica;
- identificar archivos y componentes afectados;
- preparar hechos para el Team Lead.

**Escritura:** no.

### 5.2 Frontend Engineer

**Base actual:** `vx-frontend-builder`

Responsabilidades:

- componentes UI;
- frontend web;
- accesibilidad de implementación;
- responsive;
- estados loading/error/empty;
- integración frontend con contratos API.

**Fase principal:** BUILD.

### 5.3 Backend Engineer

**Base actual:** `vx-backend-builder`

Responsabilidades:

- APIs;
- servicios;
- lógica de negocio;
- autenticación de aplicación;
- contratos de datos;
- persistencia de aplicación.

**Fase principal:** BUILD.

### 5.4 Data Engineer

**Base actual:** `vx-data-builder`

Responsabilidades:

- esquemas;
- SQL;
- índices;
- migraciones propuestas;
- contratos de persistencia;
- rollback de cambios de datos.

**Activación:** bajo demanda.

### 5.5 QA / Test Engineer

Se divide conceptualmente en dos funciones ya existentes:

- `vx-test-analyst`: diseña casos y cobertura;
- `vx-qa-builder`: implementa tests y fixtures.

Responsabilidades:

- criterios de aceptación;
- unit/integration/E2E;
- regresión;
- fixtures;
- resultados verificables.

### 5.6 Code Reviewer

**Base actual:** `vx-inspector`

Responsabilidades:

- revisión independiente del diff;
- bugs;
- regresiones;
- calidad;
- coherencia de arquitectura;
- comprobación de pruebas realmente ejecutadas.

**Escritura:** no.

### 5.7 Security Reviewer

**Base actual:** `vx-security-reviewer`

Responsabilidades:

- auth;
- permisos;
- entradas;
- secretos;
- dependencias;
- riesgos de infraestructura;
- revisión previa/posterior cuando el riesgo lo justifique.

**Escritura:** no.

## 6. Roles extendidos bajo demanda

Estos roles forman parte del equipo, pero no tienen que activarse en cada tarea.

### UI/UX Adviser

**Base:** `vx-frontend-adviser`

Revisión visual, accesibilidad y experiencia de usuario.

### Cloud / DevOps Adviser

**Base:** `vx-workers-adviser`

Cloudflare, Workers, bindings, despliegue y arquitectura cloud.

En V1 permanece asesor/read-only. Una función DevOps escritora se evaluará después de definir permisos MCP.

### Documentation Engineer

**Base:** `vx-docs-builder`

README, ADR, documentación técnica, contratos y changelog.

### Reverse Engineering Specialist

Perfil independiente para tareas IDA/reverse engineering. No se activa para desarrollo ordinario.

## 7. Flujo estándar del Dev Team

```text
INTAKE
  ↓
DISCOVER
  ↓
PLAN
  ↓
DESIGN / CONTRACT
  ↓
BUILD
  ↓
VERIFY
  ↓
REVIEW
  ↓
INTEGRATE
  ↓
RELEASE GATE
  ↓
CLOSE
```

### INTAKE

Team Lead define:

- objetivo;
- restricciones;
- definición de terminado;
- riesgo;
- proyecto/rama.

### DISCOVER

Lectores en paralelo:

- Research Engineer;
- especialista de dominio;
- Security Reviewer si aplica.

Máximo recomendado: 3.

### PLAN

Team Lead genera:

- DAG de tareas;
- responsables;
- dependencias;
- contratos;
- pruebas;
- rutas permitidas.

### DESIGN / CONTRACT

Antes de que dos áreas dependan una de otra se fija interfaz:

- API;
- schema;
- eventos;
- componentes;
- tipos;
- criterios de aceptación.

### BUILD

Se asigna un implementador especializado.

**V1: un solo escritor efectivo por worktree.**

Los otros especialistas pueden preparar análisis, propuestas o handoffs, pero no escribir simultáneamente sobre el mismo árbol.

### VERIFY

QA analiza e implementa tests cuando el entorno lo permite.

Estados válidos:

- PASS;
- FAIL;
- NO_EJECUTADO;
- NO_VERIFICADO.

### REVIEW

Revisión independiente por Inspector y Security cuando corresponda.

El autor del cambio no emite el único veredicto de aceptación.

### INTEGRATE

Team Lead:

- integra;
- resuelve incompatibilidades;
- valida contrato;
- verifica diff final.

### RELEASE GATE

Antes de merge/deploy:

- tests relevantes;
- revisión;
- estado Git;
- riesgos;
- autorización humana cuando corresponda.

### CLOSE

Salida final:

- qué cambió;
- pruebas;
- riesgos;
- pendientes;
- commit/PR;
- estado de rama.

## 8. Contrato mínimo de una tarea

Cada subtarea debería usar:

```text
task_id
parent_task_id
objective
role
base_sha
branch_or_worktree
allowed_paths
dependencies
input_contract
acceptance_criteria
tests_required
risk
writer
reviewer
status
evidence
```

## 9. Modelo de subagentes

### Subagentes de lectura

Pueden ejecutarse mediante `task` en paralelo cuando sus permisos efectivos sean read-only.

Ejemplos:

- researcher;
- inspector;
- security reviewer;
- test analyst;
- frontend adviser;
- workers adviser.

### Subagentes de implementación

Conceptualmente forman parte del Dev Team:

- frontend builder;
- backend builder;
- data builder;
- QA builder;
- docs builder.

Sin embargo, un subagente lanzado mediante `task` es no interactivo. Si su permiso de escritura requiere `ask`, no debe intentar evadir esa aprobación.

Por tanto, V1 adopta este contrato:

1. el builder puede inspeccionar y preparar implementación/handoff;
2. si no puede obtener autorización efectiva de escritura, devuelve `BLOCKED_FOR_WRITE_APPROVAL` o una propuesta de patch;
3. el Team Lead aplica/integrará el cambio como escritor autorizado;
4. escritura autónoma de builders en worktrees separados queda para una fase posterior y requerirá una política explícita.

## 10. Modo visible “Dev Team”

Objetivo de UX:

```text
Code
Plan
Ask
Debug
Dev Team   ← nuevo agente primario
```

El futuro archivo global será conceptualmente:

```text
~/.config/kilo/agent/dev-team.md
```

con:

```yaml
mode: primary
```

No se crea todavía en esta fase.

## 11. Reutilización de agentes VX existentes

| Función Dev Team | Agente actual | Decisión V1 |
|---|---|---|
| Team Lead | vx-integrador | reutilizar/evolucionar |
| Research | vx-researcher | reutilizar |
| Frontend Engineer | vx-frontend-builder | reutilizar |
| Backend Engineer | vx-backend-builder | reutilizar |
| Data Engineer | vx-data-builder | reutilizar |
| QA Analyst | vx-test-analyst | reutilizar |
| QA Engineer | vx-qa-builder | reutilizar |
| Code Reviewer | vx-inspector | reutilizar |
| Security Reviewer | vx-security-reviewer | reutilizar |
| UX Adviser | vx-frontend-adviser | reutilizar |
| Cloud Adviser | vx-workers-adviser | reutilizar |
| Documentation | vx-docs-builder | reutilizar |

No se recomienda crear agentes duplicados solo para cambiar nombres.

## 12. Decisiones para la siguiente fase

Una vez fijada esta arquitectura, la siguiente fase será construir la **matriz MCP → rol/agente → permiso**.

La matriz deberá responder para cada uno de los 13 MCP:

1. qué rol puede usarlo;
2. en qué fase;
3. lectura o escritura;
4. allow / ask / deny;
5. si puede usarlo un subagente;
6. si requiere autorización del Team Lead;
7. si requiere autorización humana;
8. riesgo;
9. fallback cuando el MCP no esté disponible.

No se modificará ningún MCP durante esa fase: solo se diseñará la política.
