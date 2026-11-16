---
name: vx-engineering-harness
description: "Dirigir tareas complejas de desarrollo autónomo de extremo a extremo en Kilo: diagnóstico, arquitectura, implementación, Git work branch, pruebas, revisión, integración a main y cierre verificable; activar para tareas de programación multi-etapa o coordinación de agentes, no para preguntas rápidas."
---

# VX Engineering Harness V4.3 (origen V3)

**Global-only:** nunca crear `.kilo`, `.agents`, `.kilocode`, `AGENTS.md`, MCP o skills de Kilo dentro del repositorio activo.

En tareas complejas, seguir `DISCOVER → PLAN → BUILD → VERIFY → REVIEW → GIT CLOSE → REPORT`.

## Enrutamiento

- Error reproducible: usar skill VX propia `vx-debugging-root-cause`; pruebas nuevas con `vx-test-regression`.
- Arquitectura/contratos: apoyarse en Sofía y usar `vx-implementation-handoff` para comunicar API, archivos y pruebas.
- Revisión: `vx-inspector` y, si hay riesgo autenticación/datos, `vx-security-review` con Valentina; evitar revisar dos veces el mismo diff sin objetivo.
- Backend Cloudflare: Mateo para bindings/DEV; backend builder implementa. No inferir deploy real de documentos.
- UI: Daniela define UX; frontend builder implementa, skill `vx-frontend-quality`.
- Datos: data builder y `vx-data-contracts`, solo fixtures antes de cualquier migración.
- Documentación: docs builder y `vx-docs-traceability`.
- Cierre: pruebas ejecutadas por runner autorizado, CI, revisión, Git y handoff. Skills externas solo si están presentes y permitidas, nunca se autoinstalan.

## Memoria/codebase

1. Verificar que MCP responde, proyecto correcto e índice fresco.
2. Buscar símbolos precisos, dependencias y rutas; cruzar resultados con archivos reales.
3. Registrar decisiones estables solamente; nunca secretos, credenciales ni dumps.
4. Si no hay índice o conexión, seguir con read/glob/grep sin bloquear el trabajo.

## Autonomía y Git

AutoApprove sigue como está. Para cambios normales autorizados, ejecutar sin preguntas repetitivas, respetando permisos de Kilo y protecciones del repositorio. En tarea no trivial: `main` sincronizada → `work/<tarea>` → cambios/probados → PR/merge permitido → comprobar `main` → borrar SOLO rama creada por esta tarea. Nunca `reset --hard`, force push, borrar otras ramas, ni desplegar a producción sin solicitud concreta.

## Evidencia de salida

Registrar alcance, archivos tocados, comandos y resultado verificable, cambios del PR/merge y estado de ramas. Reportar qué quedó sin ejecutar y por qué.


## Equipo V4

- En tareas complejas usa el catalogo global `~/.config/kilo/harness/vx-agent-registry-v4.json` y `/vx-equipo` para elegir roles; no delegar cuestiones triviales.
- En modo estricto: lectores independientes simultaneos (max. 3) -> sintesis -> un unico implementador -> revisores con objetivos distintos. Los agentes read-only no ejecutan pruebas ni alteran Git.
- Perfiles: general, backend, frontend, cloudflare, database, security, refactor, design, docs. Las skills son propuestas condicionadas a disponibilidad, no instalaciones automaticas.
- El selector local solo produce un plan; no garantiza que se haya llamado a `task` ni reporta tokens que no esten medidos.


## Gate de exactitud y procedencia V4.1

Al terminar subagentes revisa sus hallazgos contra el árbol y la revisión Git actuales. Guarda la distinción entre PASS de orquestación, FAIL de código, hipótesis DESCARTADAS y pruebas NO VERIFICADAS. No ejecutes fetch, pull ni build cuando la tarea sea SOLO LECTURA. Una diferencia de Git sin logs no autoriza inferir quién cambió referencias. Para informes contradictorios usa /vx-revalidar sin lanzar agentes redundantes.


## V4.2 — reconciliación sin cambios

- Antes de migrar agentes existentes, usa el comando global `/vx-reconciliar` y el validador de campos JSONC/Markdown en `~/.config/kilo/harness/scripts/Reconciliar-Agentes-V4.2.ps1`.
- Compara identidades, modo, `steps`, permisos básicos y campos solapados. Los prompts, modelos y descripciones nunca se imprimen.
- Un valor distinto no demuestra por sí mismo un fallo: Kilo puede fusionar propiedades por precedencia. No borres agentes ni sustituyas configuraciones privadas sin revisión, copia de seguridad y pruebas reales.
- El auditor no consume modelos ni escribe archivos; cualquier migración futura requiere un plan independiente, pruebas y rollback.


## Observación selectiva V4.3

VX Evolution pertenece exclusivamente a Kilo. No cargar el skill de gobernanza para tareas triviales. Después de una corrección importante o un fallo repetido, ofrecer una observación breve, neutra y verificada mediante /vx-observer, sin copiar detalles de clientes. El historial global se escribe solo tras invocación explícita; ninguna propuesta se aprueba o instala automáticamente. Las reuniones semanales/mensuales no están programadas hasta V4.5.

## Pack VX 0.1 — equipo de desarrollo operativo (candidato, no instalado aún)

- Siete perfiles de asesoría/coordinación existentes con alias confirmados y **cinco implementadores nuevos** (`vx-frontend-builder`, `vx-backend-builder`, `vx-qa-builder`, `vx-data-builder`, `vx-docs-builder`). Nombres de los cinco nuevos pendientes.
- El selector `Seleccionar-Equipo-V4.ps1` propone por defecto `code` nativo; `-UsarBuildersVX` elige especialista únicamente en el plan, sin lanzarlo.
- Para una tarea autorizada se puede elegir un builder `mode: all` directamente en Kilo, con `edit: ask` y `bash: ask/deny`. Una delegación `task` no interactiva que no obtenga aprobación debe devolver un plan, **nunca** autocederse permiso.
- Solo un escritor por worktree, incluso si los lectores usan `background:true`. Agent Manager con dos o más worktrees de escritura requiere autorización explícita y prueba real antes de uso.
- Los nuevos skills VX se cargan **a demanda**, no todos para cada tarea; skills de terceros que aparezcan en rutas compatibles no están administradas por VX.
- Toda mejora del propio agente o skill se formula como propuesta versionada con `vx-self-improvement`; V4.7 sigue sin aprobación criptográfica ni aplicación automática. No mutar HOME, MCP, credenciales, permisos, modelos ni scheduler.
