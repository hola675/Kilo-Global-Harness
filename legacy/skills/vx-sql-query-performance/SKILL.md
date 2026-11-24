---
name: vx-sql-query-performance
description: "Usar al diagnosticar y optimizar consultas SQL, índices y planes de ejecución mediante mediciones y EXPLAIN; no activar por cualquier uso de SQL."
metadata:
  version: "0.2.1"
  last_modified: "2026-11-22"
  origin: "vx-original"
---

# VX — Revisar SQL e índices con mediciones

**Activación:** Usar para revisar sql e índices con mediciones cuando una tarea mencione sql, indice, index, query. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-data-builder`. **Revisor independiente:** `vx-test-analyst`. **Prerequisitos de conocimiento:** `vx-data-contracts`.

## Ejecución

1. Confirmar motor, esquema y volumen.
2. Localizar N+1, scans y bloqueos.
3. Medir EXPLAIN solo en entorno autorizado.
4. Evaluar coste de nuevos índices y rollback.
5. Marcar NO_MEDIDO si no hubo query plan real..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://www.postgresql.org/docs/current/using-explain.html
