---
name: vx-task-dependency-graph
description: "Usar para construir dag acíclico de tareas y orden de integración cuando una tarea mencione dependencia, dag, paralelo, worktree. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  last_modified: "2026-11-21"
  origin: "vx-original"
---

# VX — Construir DAG acíclico de tareas y orden de integración

**Activación:** Usar para construir dag acíclico de tareas y orden de integración cuando una tarea mencione dependencia, dag, paralelo, worktree. Exigir evidencia real y no cambiar permisos.

**Responsable vigente:** `vx-dev-team`. **Revisor independiente:** `vx-dev-reviewer` cuando aporte valor. Los nombres VX anteriores son históricos. **Prerequisitos de conocimiento:** `vx-requirements-acceptance`.

## Ejecución

1. Identificar tarea, dueño, revisor y contratos mínimos; obtener SHA real si Git dispone de HEAD, o registrar `GIT_UNBORN_HEAD` / `GIT_NOT_APPLICABLE` según el caso.
2. Crear dependencias únicamente si un agente necesita realmente la salida estable de otro.
3. Detectar ciclos y estado PENDING/RUNNING/VERIFIED; un retorno de hijo sin verificación independiente no equivale a VERIFIED.
4. Proponer `mode: PARALLEL_SAFE` en `vx_task_dag.py` si existe trabajo independiente: hasta cuatro background activos, máximo dos escritores, sin ejecutar tareas automáticamente.
5. Para escritores en worktrees diferentes, comprobar **externamente** que el host realmente los aísla. Para un workspace compartido, el valor por defecto es un escritor; admitir dos solo si `allow_shared_worktree_exact_files: true`, `write_scope: EXACT_FILES` en cada tarea y `allowed_paths` literales sin solapamiento, sin commits ni cambios de rama concurrentes.
6. Lanzar cada hijo con `task(background: true)` **cuando Kilo Desktop exponga el argumento real**; si no existe, foreground. El padre continúa con otras tareas independientes mientras los hijos escriben sus archivos exclusivos.
7. No leer ni editar archivos inestables; esperar la barrera de integración para revisar diff, imports, pruebas y PR. No hacer polling repetitivo.
8. Las salidas `background_candidates`, `parallel_deferred` y `file_lease_proposals` son propuestas, no locks ni procesos activos; `PROPOSED_NOT_DISPATCHED` es el estado correcto.

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://kilo.ai/docs/automate/agent-manager-workflows
