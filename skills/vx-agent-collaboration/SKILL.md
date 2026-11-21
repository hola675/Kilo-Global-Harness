---
name: vx-agent-collaboration
description: "Usar para coordinar task/swarm y agent manager con evidencia cuando una tarea mencione agentes, delegacion, swarm, agent manager. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Coordinar task/Swarm y Agent Manager con evidencia

**Activación:** Usar para coordinar task/swarm y agent manager con evidencia cuando una tarea mencione agentes, delegacion, swarm, agent manager. Exigir evidencia real y no cambiar permisos.

**Responsable vigente:** `vx-dev-team` (único líder). **Revisor independiente:** `vx-dev-reviewer` cuando el riesgo justifique revisión. Los nombres `vx-integrador` y `vx-inspector` pertenecen a la familia histórica retirada del pack activo. **Prerequisitos de conocimiento:** `vx-task-dependency-graph`, `vx-implementation-handoff`.

## Ejecución

1. **En Kilo Desktop**, usar `task` foreground si el resultado es requisito inmediato; `task(background: true)` si el trabajo independiente permite continuar al padre. El argumento debe existir realmente en la herramienta: no escribirlo como texto de la tarea ni fingir que se inició un hijo.
2. Distinguir `task` (mismo workspace/worktree) de Agent Manager (sesiones/worktrees aislados **solo en la extensión VS Code**, no herramienta disponible aquí) y de Kilo Swarm (mensajes, no despachador). No elevar `agent_manager`, `board_read` ni `board_post` sin autorización explícita.
3. Emitir contratos mínimos con objetivo, workspace, archivos exactos, dependencia y aceptación; inferir ID/SHA/rama reales cuando existan, o `GIT_UNBORN_HEAD` si Git no tiene primer commit.
4. Limitar a cuatro hijos background activos y dos escritores con rutas exclusivas. En workspace compartido exigir contrato explícito `write_scope: EXACT_FILES`, `allowed_paths` sin solapamientos y propietario exclusivo por archivo; con globs, archivos compartidos, commits o dependencias sin verificar, serializar o trabajar en worktrees efectivamente aislados.
5. El líder trabaja en paralelo en contratos, inspecciones, documentación fuera de las rutas reservadas o tareas independientes; no sustituye ni duplica la escritura del hijo.
6. Esperar la finalización real del hijo; si se interrumpe, `HOLD_RECHECK` y reanudar por identificador solo si Kilo lo permite. Integrar cambios y pruebas en una barrera; no dar por VERIFIED el reporte del propio builder.

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://kilo.ai/docs/automate/agent-manager
