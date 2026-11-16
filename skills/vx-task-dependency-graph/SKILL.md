---
name: vx-task-dependency-graph
description: "Usar para construir dag acíclico de tareas y orden de integración cuando una tarea mencione dependencia, dag, paralelo, worktree. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Construir DAG acíclico de tareas y orden de integración

**Activación:** Usar para construir dag acíclico de tareas y orden de integración cuando una tarea mencione dependencia, dag, paralelo, worktree. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-integrador`. **Revisor independiente:** `vx-inspector`. **Prerequisitos de conocimiento:** `vx-requirements-acceptance`.

## Ejecución

1. Definir task_id, dueño, revisor, base SHA y contratos de entrada/salida.
2. Crear edges solo si existen dependencias.
3. Detectar ciclos.
4. Marcar READY/BLOCKED.
5. Coordinar un escritor por worktree.
6. Integrar en orden topológico..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://kilo.ai/docs/automate/agent-manager-workflows
