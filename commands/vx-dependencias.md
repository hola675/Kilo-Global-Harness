---
# component_version: 1.0.0
# last_modified: 2026-11-21
description: "Valida un DAG de tareas del Core unificado sin lanzar agentes ni cambiar el sistema."
agent: vx-dev-team
---

# /vx-dependencias — validar planificación

Plan JSON autorizado: $ARGUMENTS

Utiliza la skill `vx-task-dependency-graph` si está disponible. Antes de ejecutar, comprueba que el plan es un archivo JSON local bajo el proyecto encargado, sin secretos y con propietario/revisor diferentes. No construyas comandos a partir de texto libre ni cambies el estado de las tareas.

El Pack Dev Team Core unificado instala **juntos**:

- Validador de solo lectura: `~/.config/kilo/harness/scripts/vx_task_dag.py`
- Registro de agentes único: `~/.config/kilo/harness/vx-unified-pack-v1.json`

Con una ruta de plan explícita y segura, ejecuta mediante Python la operación siguiente (rutas individuales como argumentos, nunca concatenar shell con contenido del plan):

```powershell
python -I "$HOME/.config/kilo/harness/scripts/vx_task_dag.py" --registry "$HOME/.config/kilo/harness/vx-unified-pack-v1.json" --plan "<RUTA_LOCAL_JSON>"
```

Si el registro, script o plan no existe o no se puede leer, informa `TOOL_UNAVAILABLE` o `NO_VERIFICADO` con causa; no recurras al selector V4 ni al registro de agentes retirados. El modo `STRICT` conserva su comportamiento histórico. `PARALLEL_SAFE` añade propuestas de `background_candidates`, `parallel_deferred` y `file_lease_proposals`: máximo cuatro tareas en background (dos writers), con un escritor por worktree por defecto. Para planear dos escritores sobre el mismo checkout hay que declarar `allow_shared_worktree_exact_files: true` en el plan, `write_scope: EXACT_FILES` en cada tarea y archivos literales sin solapamiento. **Son propuestas, no locks, worktrees ni ejecuciones reales.** El líder usa `task(background: true)` si el host dispone del argumento y respeta la barrera de integración. El planificador nunca inicia `task`, cambia archivos, aprueba herramientas, confirma una revisión real o autoriza permisos.

**Enrutamiento válido:** dueño/escritor `vx-dev-team` o uno de los seis builders; revisión separada por `vx-dev-reviewer`, `vx-dev-quality`, `vx-dev-security` u otro analista pertinente, siempre según permiso y contexto efectivos. No asignar escritura a especialistas read-only.
