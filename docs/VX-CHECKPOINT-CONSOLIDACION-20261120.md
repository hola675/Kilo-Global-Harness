# VX — Punto de control después de la consolidación de ramas (2026-11-20)

**Versión:** 1.0.0 · **Estado:** SOURCE / GITHUB VERIFICADO; RUNTIME LOCAL NO RECERTIFICADO.

## Evidencia de cierre

- `main`: `872980d910af2487e761ab0b98ffe37f10361034` (según GitHub y salida del operador).
- El operador ejecutó `Consolidar-Ramas-Main-V2.ps1` con confirmación y reportó `remoto_eliminadas=1`, `local_eliminadas=0`, `remoto_restantes=0`, `local_restantes=0`; sincronía `main...origin/main = 0 0`.
- La rama `work/capability-handoff-multiagent-v1` se archivó en el tag remoto `archive/remote/work/capability-handoff-multiagent-v1` antes del borrado.
- PR #92 integrado el 2026-11-20 04:40 UTC; workflow de `main`, run #567 (ID 44675943310), `conclusion=success` para ese SHA. Esto es **CI/source PASS**, no certificación runtime.

## Dos inventarios diferentes (NO sumar ni intercambiar)

| Capa | Inventario source | Función | Activación |
| --- | --- | --- | --- |
| Pack VX 0.4.0 | 14 agentes; 32 skills | Builders VX, coordinación y editorial | El nuevo editorial y sus permisos `ask` son **source-only** |
| Dev Team 2.3.0 | 1 líder + 10 especialistas ocultos = 11 agentes; 44 skills en capas de source | Especialistas de lectura; 18 core con allowlist; 26 adicionales no autorizadas | Preflight histórico: 6/11 agentes y 2/18 skills core byte-idénticos; no recertificado para este HEAD |
| MCP | 13 familias | Servidores e integraciones | No modificar conexiones ni ACL por un PASS de source |

El líder `vx-dev-team` es el único modo principal de Dev Team. El subagente `vx-editorial-builder` está en el Pack VX, subordinado al líder, **no es un undécimo especialista de `runtime/dev-team-v2r/agents`**. Los recuentos pueden solaparse por identificadores; nunca interpretarlos como 25 agentes únicos instalados.

## Próxima secuencia segura

1. Capturar snapshot **solo lectura** del HOME del operador: agente seleccionado, herramientas reales, versiones y SHA del source frente a archivos instalados; excluir secretos y contenidos privados.
2. Clasificar cada diferencia: contenido semántico, ACL, orden/alias, BOM/EOL, otro. Conservar backup y registrar evidencia, sin sobreescritura silenciosa.
3. Validar que el líder pueda solicitar `task` al editorial, con consentimiento del host, mientras el editorial conserva `task/bash/agent_manager: deny`. Una declaración YAML no acredita permiso efectivo.
4. Probar en un repositorio de ensayo pequeño un handoff Backend→Frontend/QA y Frontend→Editorial→Frontend. El planificador sigue `PLAN_ONLY`; no ejecutar despacho, borrado de datos ni cambios de producción.
5. Certificar cada modificación contra pruebas focalizadas vivas (`TEST_ACTION=UPDATE` o `REPLACE` justificado); retirar casos obsoletos únicamente después de comprobar cobertura sustituta.
6. Someter cualquier activación runtime, ACL de HOME, watcher, scheduler o dispatcher a autorización explícita independiente. Issues #81, #86 y #91 siguen siendo puntos de control, no autorizaciones implícitas.

## Invariantes

- `main` es la única rama permanente; ramas `work/*` temporales por tarea.
- Integración vía PR, CI, revisión y SHA verificado; limpieza archivada con comprobación de propietario/worktree.
- Una propuesta `CAPABILITY_HANDOFF` no es delegación, permiso, implementación ni prueba humana.
- `SOURCE_PASS != RUNTIME_PASS`; no afirmar instalación ni generación automática de botones.

**Referencias:** [handoffs](VX-TEAM-CAPABILITY-HANDOFF-V1.md) · [Dev Team canónico](VX-DEV-TEAM-CURRENT-PACK-V1.md) · [certificación histórica](VX-DEV-TEAM-230-RUNTIME-CERTIFICATION.md).
