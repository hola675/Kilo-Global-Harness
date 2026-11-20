# VX — Reconciliación continua del equipo con main V1

**Fecha:** 2026-11-19 · **Versión:** 1.1.0 · **Estado:** SOURCE / DISEÑO OPERATIVO. No hay daemon, webhook, scheduler, ajuste de ACL ni cambios en HOME activos.

## Contrato de trabajo del equipo

**Una sola rama permanente:** `main`. **Varias ramas `work/*` temporales pueden coexistir** cuando haya tareas realmente independientes y cada una tenga propietario y worktree o sesión de escritura aislados. **Un único escritor por worktree**: si varios agentes comparten el mismo árbol, solo uno escribe. Una rama no tiene dos agentes escritores simultáneos.

Cada tarea registra `task_id`, `owner_agent`, `repo`, `branch`, `base_main_sha`, `last_reconciled_main_sha`, `status`, `allowed_paths` y evidencia de CI. Estos metadatos no son credenciales ni permisos. Las sesiones y tareas se registrarán en un catálogo externo a Git cuando se habilite la orquestación; nunca añadir un registro efímero de equipos privados al repositorio público.

## Evento MAIN_ADVANCED (diseño para ejecución automática)

Cuando se detecta que `origin/main` cambió de SHA **A** a SHA **B** tras un merge confirmado:

1. Validar que **B** existe realmente en el remoto autorizado. No ejecutar sync en auditorías read-only.
2. Publicar un evento idempotente `MAIN_ADVANCED(repo,B)`; si llegan varios eventos, **agrupar por el SHA de main más reciente**.
3. Consultar tareas activas `ACTIVE` / `IN_REVIEW` en ramas `work/*` del mismo repositorio. No incluir `main`, ramas cerradas ni tareas ajenas.
4. Emitir una tarea `RECONCILE_REQUIRED` por rama activa y SHA objetivo. **Enrutar al agente propietario de esa rama**, nunca a todos los agentes indiscriminadamente. Un evento repetido no duplica trabajo.
5. El agente entra en **punto seguro**: termina la escritura actual, pausa nuevas mutaciones y valida worktree, ownership, estado Git, tip remoto y ausencia de merge/rebase previo.
6. Si el worktree está limpio y la rama sigue siendo la suya, concilia **su rama** con el `origin/main` actualizado mediante un merge Git normal, sin rebase de commits compartidos ni force push. No modifica `main` desde la rama activa. Antes de operar, verifica otra vez que B sea el objetivo vigente; si avanzó, replanifica.
7. Si hay cambios sin guardar, conflictos, branch moved, PR incompatible, ownership dudoso, worktrees compartidos o permisos insuficientes, marca `PAUSED_NEEDS_REVIEW`. No hace `stash`, `reset`, `checkout --ours/theirs`, resolución automática de conflictos ni borrados.
8. Tras reconciliar, ejecuta **solo** los tests afectados por cambios en `main` y por su tarea, revisión de diff y contratos; registra SHA conciliado y evidencia antes de `RESUME`. Si `main` vuelve a avanzar, repite el ciclo desde el nuevo SHA; no retiene un objetivo obsoleto.
9. En la integración final: `main` actual → PR → CI real → revisión independiente → merge → verificar el SHA remoto → archivar/eliminar **únicamente** la rama de esa tarea cuando no haya trabajo pendiente. El merge provoca otro evento `MAIN_ADVANCED` para las demás ramas activas.
10. No crear una nueva rama para reconciliar otra rama existente. Un conflicto bloquea esa tarea, no el progreso seguro de tareas independientes.

**Semántica:** la señal es automática cuando exista un detector autorizado; reconciliar puede ser automático **solo** con worktree limpio, propietario autorizado, lease de branch y pruebas de seguridad verificadas. Reanudar trabajo depende del agente y de las evidencias, nunca de un merge a ciegas.

## Máquina de estados

`ACTIVE → RECONCILE_REQUIRED → WAIT_SAFEPOINT → RECONCILING → VERIFYING → ACTIVE`

Ramas de error: `PAUSED_NEEDS_REVIEW`, `CONFLICT_PAUSED`, `BLOCKED_PERMISSION`, `STALE_TARGET_REPLAN`; salida: `IN_REVIEW → MERGED → ARCHIVED → CLOSED`. No anunciar `RECONCILED` cuando `git merge`, tests o revisión fallen.

## Permisos y límites

- Los subagentes **Dev Team 2.3.0** siguen read-only; reciben contexto de `MAIN_ADVANCED` solo para reevaluar, no hacen `git merge`, `bash` ni ediciones.
- `vx-dev-team` y los builders VX tienen `edit/bash: ask` en el source. `ask` **no es** `allow`: no delegar los comandos a un lector ni cambiar ACL para que «no bloquee».
- La futura ejecución automática A2 requiere identidad de agente, autorización por repositorio/rama/comando, permisos efectivos comprobados, separación de worktrees, leases, casos positivos/negativos y rollback. La mutación de ramas remotas y el merge a `main` siguen sujetos a permisos de GitHub y revisiones.
- No usar ramas auxiliares para eludir una denegación. No tocar producción, HOME, credenciales, scheduler, ACL/MCP ni `kilo.jsonc`.
- La detección y la planificación están disponibles como **lógica fuente inerte** en `tools/vx_team_git_reconciliation.py`; no monitoriza ni despacha tareas por sí sola. La integración con watcher, agentes y orquestador queda `NOT_ACTIVATED`.

## Oráculos y certificación

| Invariante | Prueba obligatoria al habilitar ejecutor |
| --- | --- |
| `MAIN_ADVANCED` con dos ramas activas | exactamente una tarea por rama y SHA; excluir cerradas |
| Evento repetido | cero tareas duplicadas |
| `main` avanza dos veces | reconciliar con la última revisión y descartar la anterior |
| Worktree sucio o uso por otro agente | pausa sin mutaciones |
| Conflicto real | no auto-resolver ni reanudar |
| SHA remoto cambió durante ejecución | no escribir a un tip obsoleto; replanificar |
| Permiso `deny` / `ask` no satisfecho | jamás concederse permiso o cambiar herramienta |
| PR fusionada | borrar solo la rama propia, tras verificar integración y archivar si hace falta |
| CI / smoke runtime | evidencia diferenciada; SOURCE PASS no certifica agente instalado |

**Estado actual:** PLAN_ONLY. La suite existente `tests/test_vx_dev_team_consolidation_v1.py` prueba el planificador sin crear un gate o una suite histórica adicional. El futuro ejecutor se prueba en un repositorio Git sintético antes de cualquier activación real.

## A0/A1 — Observación bajo demanda y cola simulada V1.1

El código fuente incorpora un **observador Git ejecutable una sola vez** y un **modelo de cola idempotente en memoria**, sin habilitar ningún watcher, daemon ni ejecutor de merges.

- `observe_origin_main`: lee `origin`, consulta `refs/heads/main` con `git ls-remote`, comprueba existencia local de ambos commits y valida `git merge-base --is-ancestor`. No ejecuta `fetch`, `merge`, `push` ni modifica refs.
- La diferencia de SHA se clasifica como `MAIN_ADVANCED_VERIFIED` solo cuando está demostrada la relación de ancestro. Si el commit remoto aún no existe localmente, devuelve `MAIN_CHANGED_ANCESTRY_UNVERIFIED`; si hubo divergencia, `MAIN_DIVERGED_BLOCKED`. **Ninguno permite crear trabajo de reconciliación**.
- `coalesce_pending_queue`: conserva una sola entrada pendiente por `(repo, branch)`, admite varios agentes en ramas independientes y descarta duplicados. Solo reemplaza planes pendientes cuando el SHA anterior de la cola coincide con `previous_main_sha` del evento; si las notificaciones llegan desordenadas, devuelve `MAIN_EVENT_ORDER_UNVERIFIED` en vez de retroceder a un SHA viejo. **No sustituye** una tarea `RECONCILING` o `VERIFYING`, y bloquea cambios de propietario.
- Cuando una tarea deja de aparecer activa, su entrada pendiente pasa a `HOLD_RECHECK`. Si reaparece, podrá obtener un nuevo plan, pero sigue sin autorizar ningún comando Git.
- El sistema no persiste cola ni recupera sesiones tras cortes eléctricos: **la cola durable, identidad de agente, watcher y despacho siguen pendientes** en la issue #86.

### Ejecución de solo lectura en Windows

El siguiente ejemplo consulta Git de manera explícita, una vez, sin modificar ramas ni estados:

```powershell
Set-Location D:\Proyectos\Kilo-Global-Harness
python .\tools\vx_team_git_reconciliation.py --observe-main `
  --repo hola675/Kilo-Global-Harness `
  --repo-dir . `
  --previous-main <SHA_DE_MAIN_OBSERVADO_ANTES>
```

Opcionalmente pasar `--tasks <archivo-json-local>` para planificar ramas activas y `--queue <archivo-json-local>` para calcular una nueva propuesta de cola. El primer archivo debe contener `{"tasks": [...]}` y el segundo `{"queue": [...]}`. Ambos deben permanecer **fuera del repositorio público** porque pueden describir tareas y agentes del operador. El comando solo imprime JSON; **no crea, escribe, notifica, programa ni ejecuta nada**.

Para una observación con SHA nuevo que el Git local todavía no tiene, no se ejecutará el plan: una fase de sincronización Git autorizada debe traer el objeto y repetir la comprobación de ascendencia. Nunca deducir que un SHA de mayor valor hexadecimal es más reciente.

**Certificación:** los tests focalizados pertenecen a la suite existente `tests/test_vx_dev_team_consolidation_v1.py` (`UPDATE`). Las pruebas de contrato no acreditan el funcionamiento real del detector bajo proxy Windows, de la futura cola persistente o de las ACL de Kilo.

## Pendientes para activación posterior

1. Terminar reconciliación source↔runtime (agentes 6/11; skills CORE 2/18 coincidían en último preflight).
2. Capturar permisos reales de Kilo, herramientas de Git/Agent Manager, ownership de ramas y callbacks de finalización.
3. Desarrollar detector de cambios de `main`, cola idempotente de tareas por rama y mecanismo de pausa/reanudación, sin acceso a producción.
4. Probar eventos concurrentes, conflictos, power loss y recuperación en Windows.
5. Presentar el diff de ACL y solicitar aprobación independiente explícita del operador para habilitar automatización.
