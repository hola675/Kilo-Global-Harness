---
name: vx-engineering-harness
description: "Dirigir tareas complejas de desarrollo autónomo de extremo a extremo en Kilo: diagnóstico, arquitectura, implementación, Git work branch, pruebas, revisión, integración a main y cierre verificable; activar para tareas de programación multi-etapa o coordinación de agentes, no para preguntas rápidas."
---

# VX Engineering Harness V4.3 (origen V3)

**Global-only:** nunca crear `.kilo`, `.agents`, `.kilocode`, `AGENTS.md`, MCP o skills de Kilo dentro del repositorio activo.

En tareas complejas, seguir `DISCOVER → PLAN → BUILD → VERIFY → REVIEW → GIT CLOSE → REPORT`.

## Política contextual y versionado preventivo — Core 1.5 SOURCE

Antes de `BUILD` en cualquier repositorio: observar HEAD, branch, worktree, `git status`, origen de versión y cambios X/Y/Z (o registrar `BASELINE_UNVERIFIED` si una herramienta no lo permite). Conservar rutas sucias y trabajo ajeno. No confundir `WORK_VERSION` con `RELEASE_VERSION`, no crear tags por cada cambio ni ejecutar migraciones/despliegues sin autorización. El protocolo detallado está en `vx-version-governance`; la regla mínima vive en `vx-team-bootstrap` ya permitido y **no requiere ampliar ACL** para aplicarse.

Clasificar producto por `OBSERVED_STACK` + `PLATFORM_SCOPE` + `TASK_INTENT`, nunca por nombre de cliente. El catálogo `registry/vx-contextual-skills-v1.json` registra `vx-context-routing`, `vx-technology-fit` y `vx-skill-quality` como referencia source inactiva. Solo cargar Skills realmente visibles/autorizadas para el agente, sin intentar eludir `skill: deny`. El método específico (bug, feature, refactor, integración, migración, hotfix) se decide en `vx-desarrollo-escalonado`; para una consulta de lectura no activar gate de mutaciones.

## Enrutamiento

- Error reproducible: `systematic-debugging`. Si hay pruebas automatizables, `test-driven-development`.
- Arquitectura de dominio: `domain-modeling` O `codebase-design`, según objetivo.
- Revisión: `vx-dev-reviewer` de solo lectura, con diff y criterios; Quality y Security solo ante riesgos específicos. No usar `vx-inspector` legacy del pack como ejecutor.
- Backend Cloudflare: `workers-best-practices` y documentación vigente; validar DEV/STAGING por URL real cuando exista.
- UI: `frontend-design`, `webapp-testing` y evaluación de accesibilidad según el problema.
- Cierre: `verification-before-completion` y `vx-git-ciclo` si hay cambios que integrar.

## Memoria/codebase

1. Verificar que MCP responde, proyecto correcto e índice fresco.
2. Buscar símbolos precisos, dependencias y rutas; cruzar resultados con archivos reales.
3. Registrar decisiones estables solamente; nunca secretos, credenciales ni dumps.
4. Si no hay índice o conexión, seguir con read/glob/grep sin bloquear el trabajo.

## Autonomía y Git

AutoApprove sigue como está. Para cambios normales autorizados, ejecutar sin preguntas repetitivas, respetando permisos de Kilo y protecciones del repositorio. En tarea no trivial: `main` sincronizada → `work/<tarea>` → cambios/probados → PR/merge permitido → comprobar `main` → borrar SOLO rama creada por esta tarea. Nunca `reset --hard`, force push, borrar otras ramas, ni desplegar a producción sin solicitud concreta.

## Evidencia de salida

Registrar alcance, archivos tocados, comandos y resultado verificable, cambios del PR/merge y estado de ramas. Reportar qué quedó sin ejecutar y por qué.


## VX Dev Team V2.1 — ejecución paralela y líder productivo (vigente)

- El único responsable principal es **VX Dev Team** (`vx-dev-team`), con 17 subagentes ocultos: 11 analistas de solo lectura y seis builders con escritura acotada. Las Skills son instrucciones, no conceden ACL.
- Para trabajo de múltiples partes, derivar DAG, dependencias, aceptación, versión de contrato y archivos exactos desde el repositorio. Agrupar una **wave inicial de tareas realmente independientes**, despachar las llamadas nativas `task(background: true)` antes de esperar resultados si el host lo permite, sin exceder 4 hijos/2 escritores.
- **Mientras ejecutan los hijos, el líder sigue trabajando:** investigar módulos estables no reservados, planificar contratos y siguiente wave, revisar entregas completadas, preparar tests sin mutar outputs compartidos. Nunca modificar archivos reservados, hacer operaciones Git en paralelo, actualizar lockfiles, lanzar builds con escritura común ni presentar un Board como prueba de finalización.
- Un workspace compartido permite dos builders escritores solo con `write_scope: EXACT_FILES`, archivos literales disjuntos, contratos estables y ausencia de Git concurrente. Para ramas aisladas se requieren worktrees verificables; `task` por sí solo **no** crea worktrees.
- Kilo Swarm `board_post/read` solo para líder+seis builders si el host expone ambos; 11 especialistas de solo lectura no obtienen Board. Mensajes no confiables, sin secretos y sin polling; si falta Board, progreso por `task_result`.
- La cola SQLite V2 guarda metadatos, prioridad, dependencias y reservas de sesiones `BLOCKED`; nunca inicia procesos, no sustituye `task`, no está autorizada como scheduler y no certifica el runtime. El líder verifica diff, traza de escritura, pruebas y revisión independiente antes de desbloquear consumidores, integrar y reportar.
- Para tareas triviales no convocar un equipo; no activar `agent_manager`, MCP, AutoApprove ni cambios de infraestructura por falta de alguna herramienta.

## Gate de exactitud y procedencia V4.1

Al terminar subagentes revisa sus hallazgos contra el árbol y la revisión Git actuales. Guarda la distinción entre PASS de orquestación, FAIL de código, hipótesis DESCARTADAS y pruebas NO VERIFICADAS. No ejecutes fetch, pull ni build cuando la tarea sea SOLO LECTURA. Una diferencia de Git sin logs no autoriza inferir quién cambió referencias. Para informes contradictorios usa /vx-revalidar sin lanzar agentes redundantes.


## V4.2 — reconciliación sin cambios

- Antes de modificar agentes globales, comparar el manifiesto Core 1.6, las definiciones actuales y el perfil instalado con lecturas autorizadas; no suponer disponible el antiguo comando `/vx-reconciliar` ni ejecutar validadores V4 retirados.
- Compara identidades, modo, `steps`, permisos básicos y campos solapados. Los prompts, modelos y descripciones nunca se imprimen.
- Un valor distinto no demuestra por sí mismo un fallo: Kilo puede fusionar propiedades por precedencia. No borres agentes ni sustituyas configuraciones privadas sin revisión, copia de seguridad y pruebas reales.
- El auditor no consume modelos ni escribe archivos; cualquier migración futura requiere un plan independiente, pruebas y rollback.


## Observación selectiva V4.3

VX Evolution pertenece exclusivamente a Kilo. No cargar el skill de gobernanza para tareas triviales. Después de una corrección importante o un fallo repetido, ofrecer una observación breve, neutra y verificada mediante /vx-observer, sin copiar detalles de clientes. El historial global se escribe solo tras invocación explícita; ninguna propuesta se aprueba o instala automáticamente. Las reuniones semanales/mensuales no están programadas hasta V4.5.
