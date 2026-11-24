# VX Dev Team · Git y conciliación con main

**Vigencia:** Core VX 1.6.0-rc1. Este procedimiento lo aplica el líder mediante Git y herramientas realmente autorizadas; **no hay watchdog, hook, scheduler, listener o módulo de reconciliación automática** en el Core mínimo.

## Contrato

- `main` es la única rama permanente. Crear una rama `work/<tarea>` temporal por objetivo no trivial y eliminarla solo después de constatar el merge.
- Cada worktree tiene **un propietario Git**. Nunca ejecutar checkout, pull, commit, merge, rebase o stash simultáneamente desde dos agentes sobre el mismo directorio.
- Dos builders pueden editar *archivos exactos, literales y disjuntos* bajo `write_scope: EXACT_FILES` en un único workspace **sin operaciones Git concurrentes**, si la herramienta y el líder pueden garantizar esos límites. Los conflictos, lockfiles y migraciones exigen serialización.
- `task(background: true)` no crea una rama ni worktree. `board_post` comunica información y no prueba una actualización Git ni un lock.
- Todos los archivos sin guardar y modificaciones ajenas deben preservarse; prohibidos `reset --hard`, force-push, auto-stash y resolución destructiva de conflictos.

## Cuando main avanza

1. El líder observa el SHA de `origin/main` con herramientas reales. No interpretar cambios de estado sin prueba como un `MAIN_ADVANCED`.
2. Identifica solo ramas activas afectadas y pausa a sus escritores al llegar a una barrera segura.
3. Si hay cambios locales o sesiones de escritura sin cerrar, detener y registrar `BLOCKED`; no sincronizar a la fuerza.
4. El propietario de cada worktree actualiza su base con el `main` verificado, resuelve conflictos con revisión y reejecuta las pruebas correspondientes.
5. El líder verifica el resultado y, si ha cambiado un contrato compartido, emite handoffs dirigidos a consumidores afectados. No recrea tareas idénticas ante mensajes duplicados.
6. Fusionar por PR después de PASS y revisión; comprobar que `main` contiene el cambio y retirar exclusivamente la rama propia.

## Estado y recuperación

El ledger de sesión o `scripts/vx_task_dag.py` registra tareas, dependencias y eventos, **no lanza comandos Git ni modelos**. Una sesión `BLOCKED` con `host_task_id` conserva sus archivos y plaza de concurrencia; `reset` requiere prueba de que el host terminó. La cola SQLite es local y no ofrece un scheduler.

Los prototipos antiguos `tools/vx_team_git_reconciliation.py`, `vx_team_git_queue_store.py` y `vx_team_git_worktrees.py` no pertenecen al Core actual. Sus algoritmos experimentales y casos de prueba permanecen en Git history, no en la instalación vigente.

Ver [handoff](VX-TEAM-CAPABILITY-HANDOFF-V1.md), [Autopilot](VX-DEV-TEAM-AUTOPILOT-V2.md) y [política global](../rules/AGENTS-global-managed.md).

**Regla final:** registrar `SOURCE_PASS`, `INSTALLED_FILES_MATCH` y `HOST_RUNTIME_PASS` por separado; no inventar sincronización automática, autorización o autoría.
