# VX Dev Team V1 — matriz MCP por rol y permiso

**Estado:** PROPOSAL / no activa ACL  
**Fecha:** 2026-11-17  
**Dependencia:** `docs/VX-DEV-TEAM-ARCHITECTURE-V1.md`  
**Catálogo MCP:** `registry/vx-mcp-catalog-v2.json`

## 1. Objetivo

Asignar los 13 MCP globales al equipo `Dev Team` por **necesidad real y mínimo privilegio**.

Esta matriz no modifica `kilo.jsonc`, no cambia permisos de agentes y no autoriza herramientas. Es el contrato previo a generar ACL concretas.

## 2. Leyenda

- **A** = permitir consultas/lectura normalmente.
- **Q** = preguntar / requiere gate antes de usar.
- **D** = denegar por defecto.
- **C** = condicional al perfil/tarea.
- **A/Q** = lectura permitida; mutaciones requieren aprobación.
- **A/D** = lectura permitida; mutaciones denegadas.
- **C/Q** = solo si la tarea lo necesita y con aprobación.
- **C/D** = solo lectura si se activa el perfil; mutaciones denegadas.

Regla universal V1:

> Un permiso de servidor no convierte automáticamente todas sus herramientas en seguras. Las herramientas mutables se clasifican por separado y nunca heredan un `allow` general.

## 3. Roles

Abreviaturas:

- **LEAD** — Dev Team Lead / Technical Lead.
- **RES** — Research Engineer.
- **FE** — Frontend Engineer.
- **BE** — Backend Engineer.
- **DATA** — Data Engineer.
- **QAA** — QA Analyst.
- **QAE** — QA Engineer.
- **REV** — Code Reviewer.
- **SEC** — Security Reviewer.
- **UX** — UI/UX Adviser.
- **CLOUD** — Cloud/DevOps Adviser.
- **DOCS** — Documentation Engineer.
- **RE** — Reverse Engineering Specialist.

## 4. Matriz global

| MCP | LEAD | RES | FE | BE | DATA | QAA | QAE | REV | SEC | UX | CLOUD | DOCS | RE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Codebase Memory | A/Q | A/D | A/D | A/D | A/D | A/D | A/D | A/D | A/D | C/D | C/D | A/D | A/D |
| Serena | A/Q | A/D | A/D | A/D | A/D | A/D | A/D | A/D | A/D | C/D | C/D | A/D | A/D |
| GitHub | A/Q | A/D | A/D | A/D | C/D | A/D | A/D | A/D | A/D | D | A/D | A/D | C/D |
| Context7 | A | A | A | A | A | A | A | A | A | A | A | A | C |
| Microsoft Learn | A | A | C | C | C | A | A | A | A | C | A | A | C |
| Playwright | C/Q | D | A/Q | C/Q | D | A/Q | A/Q | C/D | C/Q | A/Q | D | D | D |
| Chrome DevTools | C/Q | D | A/Q | C/Q | D | A/Q | A/Q | A/D | A/Q | A/Q | C/Q | D | D |
| Postman | A/Q | C/D | C/D | A/Q | D | A/D | A/Q | C/D | C/D | D | C/D | C/D | D |
| Snyk | C/Q | D | D | C/D | C/D | D | C/D | C/D | A/Q | D | C/D | D | C/D |
| Sentry | A/Q | C/D | C/D | A/D | D | A/D | A/D | A/D | A/D | D | A/D | C/D | D |
| Cloudflare API | C/Q | D | D | C/D | C/D | D | C/D | C/D | A/D | D | A/Q | C/D | D |
| ImageGen | C/Q | D | A/Q | D | D | D | D | D | D | A/Q | D | C/Q | D |
| IDA | C/Q | D | D | D | D | D | D | C/D | C/D | D | D | C/D | A/Q |

## 5. Política por MCP

### 5.1 Codebase Memory

**Uso:** arquitectura, grafo, búsqueda, impacto, cobertura de índice y ADR.

Lecturas:

- LEAD, RES, FE, BE, DATA, QA, REV, SEC y DOCS: permitidas según tarea.
- UX/CLOUD: solo si necesitan comprender dependencias del codebase.
- RE: permitido para correlacionar código fuente con análisis reverse.

Mutaciones:

- indexación/reindexación global: **Q** para LEAD;
- crear/modificar ADR: **Q** para LEAD;
- eliminar proyecto/grafo: **D** en Dev Team V1;
- subagentes: lectura únicamente.

### 5.2 Serena

**Uso:** símbolos, referencias, LSP, navegación semántica y refactor.

Lecturas:

- herramienta central para LEAD y roles de ingeniería;
- RES/REV/SEC/QA pueden usar navegación semántica sin editar.

Mutaciones:

- LEAD: **Q**;
- builders invocados como subagentes no interactivos: **D**;
- builder seleccionado interactivamente en una futura fase puede recibir `ask`, pero no es política V1.

### 5.3 GitHub

Lecturas:

- repos, ramas, commits, PR, Issues, Actions y checks: **A** para roles técnicos pertinentes.

Mutaciones:

- crear/actualizar ramas: **Q** LEAD;
- crear PR: **Q** LEAD;
- push/commit remoto: **Q** LEAD;
- merge: **Q + autorización humana**;
- delete branch: después de merge y verificación, **Q**;
- workflows/actions mutables: **Q + autorización humana**;
- subagentes: **D** para mutaciones.

### 5.4 Context7

Documentación técnica de librerías/frameworks.

- lectura: **A** para prácticamente todo el equipo;
- no se usa como evidencia de que una dependencia esté instalada;
- no introduce permisos de escritura.

### 5.5 Microsoft Learn

- **A** para documentación oficial Microsoft;
- especialmente RES, QA, SEC, CLOUD, DOCS y LEAD;
- FE/BE/DATA condicional a stack Microsoft.

### 5.6 Playwright

Puede navegar y realizar acciones en navegador.

- FE/QAE/QAA: **A/Q**;
- LEAD: condicional;
- UX: **A/Q** para flujos visuales;
- SEC: solo pruebas seguras autorizadas;
- acciones contra servicios reales, compras, deletes, cuentas o producción: **D** sin autorización humana explícita.

### 5.7 Chrome DevTools

- FE/QA/UX: inspección de consola, red, performance y Lighthouse;
- REV/SEC: lectura/debugging dirigido;
- JavaScript evaluation o acciones que alteren sesión: **Q**;
- no usar sesiones autenticadas sensibles sin alcance explícito.

### 5.8 Postman

- BE: MCP principal para contratos y activos API;
- QA: colecciones/requests de prueba;
- LEAD: coordinación;
- RES/DOCS/REV: consulta condicional.

Mutaciones de workspaces, colecciones, environments o APIs: **Q** para LEAD/BE interactivo; **D** para subagentes V1.

### 5.9 Snyk

Toda ejecución remota puede depender de política/plan de la organización.

- SEC: **A/Q** para análisis;
- LEAD: condicional;
- otros roles reciben resultados, no necesitan ejecutar scans por defecto;
- fixes automáticos, configuración de organización o activación de features: **D** sin autorización humana;
- jamás interpretar timeout/no cobertura como “sin vulnerabilidades”.

### 5.10 Sentry

- BE/QA/REV/SEC/CLOUD: lectura de eventos, issues y trazas;
- LEAD: coordinación;
- mutar issues, releases, equipos o configuración: **Q**;
- cambios de proyecto/organización: autorización humana.

### 5.11 Cloudflare API

- CLOUD: propietario funcional del MCP;
- SEC: lectura de riesgo/configuración;
- LEAD: coordinación;
- BE/DATA/QA/REV: lectura solo si la tarea Cloudflare lo exige.

Mutaciones:

- Workers/DNS/R2/D1/KV/Zero Trust/producción: **Q + autorización humana**;
- deploy y delete nunca automáticos;
- subagentes V1: lectura solamente.

### 5.12 ImageGen

- UX/FE: generación de mockups/assets cuando la tarea lo requiera;
- LEAD/DOCS: condicional;
- consume cuota y puede escribir archivos, por tanto siempre **Q**;
- no disponible al resto por defecto.

### 5.13 IDA

- RE: propietario funcional;
- LEAD: solo cuando el perfil reverse-engineering esté activo;
- REV/SEC/DOCS: consulta condicionada a hallazgos suministrados.

Mutaciones de IDB, Python en IDA o acciones que cambien análisis: **Q** para RE/LEAD; resto **D**.

## 6. Matriz por fase

| Fase | MCP prioritarios |
|---|---|
| INTAKE | ninguno obligatorio |
| DISCOVER | Codebase Memory, Serena, Context7, Microsoft Learn, GitHub |
| PLAN | Codebase Memory, Serena, GitHub, Context7 |
| DESIGN/CONTRACT | Serena, Codebase Memory, Postman, Context7 |
| BUILD | Serena, Codebase Memory; Postman/Cloudflare según perfil |
| VERIFY | Playwright, Chrome DevTools, Postman, GitHub Actions, Sentry |
| REVIEW | Serena, Codebase Memory, GitHub, Snyk, Chrome DevTools |
| INTEGRATE | GitHub, Serena, Codebase Memory |
| RELEASE GATE | GitHub, Snyk, Sentry, Cloudflare según proyecto |
| CLOSE | GitHub + documentación/evidencia |

## 7. Regla de subagentes V1

Un subagente vía `task` es no interactivo.

Por eso:

- MCP de documentación/lectura pueden ser `allow` para subagentes;
- MCP con herramientas mutables se reducen a lectura o se deniegan;
- si una herramienta exige `ask`, el subagente debe devolver `BLOCKED_FOR_APPROVAL`;
- nunca convertir `ask` en `allow` global solo para que una tarea hija pueda continuar.

## 8. Regla de nombres de herramientas MCP

La implementación de ACL no debe asumir que una regla genérica `mcp: deny` bloquea todas las herramientas.

Las tools MCP aparecen namespaced/prefijadas por servidor. La fase de implementación deberá:

1. enumerar los nombres efectivos de tools por MCP;
2. clasificarlos read / mutation / destructive;
3. generar reglas explícitas;
4. validar precedencia;
5. probar cada agente con una acción permitida y otra denegada.

## 9. Gates humanos obligatorios

Siempre requieren autorización humana explícita:

- merge a `main`;
- deploy a producción;
- DNS;
- crear/eliminar infraestructura;
- cambiar auth/roles/IAM;
- acciones irreversibles en bases de datos;
- modificar configuración de una organización Snyk/Sentry/Postman/Cloudflare;
- ejecutar herramientas IDA con efectos persistentes sensibles;
- uso de browser automation sobre operaciones económicas o destructivas.

## 10. Próxima fase

Después de aprobar esta matriz:

1. crear agente global `dev-team.md` como `mode: primary`;
2. reconciliar `vx-integrador` con el nuevo Team Lead sin duplicar lógica;
3. convertir los roles necesarios a subagentes efectivos;
4. generar ACL concretas por tool MCP;
5. crear pruebas de allow/deny/ask;
6. activar el modo solo después de CI + smoke test en Kilo Desktop.
