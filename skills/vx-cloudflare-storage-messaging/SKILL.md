---
name: vx-cloudflare-storage-messaging
description: "Usar para diseñar almacenamiento y mensajería cloudflare cuando una tarea mencione d1, kv, r2, queue. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Diseñar almacenamiento y mensajería Cloudflare

**Activación:** Usar para diseñar almacenamiento y mensajería cloudflare cuando una tarea mencione d1, kv, r2, queue. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-data-builder`. **Revisor independiente:** `vx-workers-adviser`. **Prerequisitos de conocimiento:** `vx-data-contracts`, `vx-cloudflare-worker-runtime`.

## Ejecución

1. Elegir D1/KV/R2/Queues según consistencia y patrones.
2. TTL, IDs de idempotencia y reintentos.
3. Semántica at-least-once/DLQ y fallos parciales.
4. Pruebas sintéticas.
5. Sin borrar buckets ni ejecutar migración productiva..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://github.com/cloudflare/skills
