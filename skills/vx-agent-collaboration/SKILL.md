---
name: vx-agent-collaboration
description: "Usar para coordinar task/swarm y agent manager con evidencia cuando una tarea mencione agentes, delegacion, swarm, agent manager. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Coordinar task/Swarm y Agent Manager con evidencia

**Activación:** Usar para coordinar task/swarm y agent manager con evidencia cuando una tarea mencione agentes, delegacion, swarm, agent manager. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-integrador`. **Revisor independiente:** `vx-inspector`. **Prerequisitos de conocimiento:** `vx-task-dependency-graph`, `vx-implementation-handoff`.

## Ejecución

1. Distinguir task mismo árbol, Swarm de sesión y Agent Manager sesión independiente.
2. Emitir contratos task_id/base_sha/allowed_paths.
3. Divulgar solo interfaz con dependientes.
4. Prevenir doble escritura.
5. No inventar mensajes cruzando worktrees..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://kilo.ai/docs/automate/agent-manager
