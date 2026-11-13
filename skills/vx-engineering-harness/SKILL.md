---
name: vx-engineering-harness
description: "Dirigir tareas complejas de desarrollo autónomo de extremo a extremo en Kilo: diagnóstico, arquitectura, implementación, Git work branch, pruebas, revisión, integración a main y cierre verificable; activar para tareas de programación multi-etapa o coordinación de agentes, no para preguntas rápidas."
---

# VX Engineering Harness V3

**Global-only:** nunca crear `.kilo`, `.agents`, `.kilocode`, `AGENTS.md`, MCP o skills de Kilo dentro del repositorio activo.

En tareas complejas, seguir `DISCOVER → PLAN → BUILD → VERIFY → REVIEW → GIT CLOSE → REPORT`.

## Enrutamiento

- Error reproducible: `systematic-debugging`. Si hay pruebas automatizables, `test-driven-development`.
- Arquitectura de dominio: `domain-modeling` O `codebase-design`, según objetivo.
- Revisión: usar `vx-inspector` o `code-reviewer` en tareas realmente importantes, no ambos en el mismo diff sin necesidad.
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


## Equipo V4

- En tareas complejas usa el catalogo global `~/.config/kilo/harness/vx-agent-registry-v4.json` y `/vx-equipo` para elegir roles; no delegar cuestiones triviales.
- En modo estricto: lectores independientes simultaneos (max. 3) -> sintesis -> un unico implementador -> revisores con objetivos distintos. Los agentes read-only no ejecutan pruebas ni alteran Git.
- Perfiles: general, backend, frontend, cloudflare, database, security, refactor, design, docs. Las skills son propuestas condicionadas a disponibilidad, no instalaciones automaticas.
- El selector local solo produce un plan; no garantiza que se haya llamado a `task` ni reporta tokens que no esten medidos.
