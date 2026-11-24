---
name: vx-cloudflare-worker-runtime
description: "Usar al implementar o diagnosticar código ejecutado en Cloudflare Workers, Wrangler, bindings y restricciones del runtime edge; no activar por usar Cloudflare DNS, Pages o dominio sin Workers."
metadata:
  version: "0.2.1"
  last_modified: "2026-11-22"
  origin: "vx-original"
---

# VX — Programar Workers con compatibilidad real

**Activación:** Usar para programar workers con compatibilidad real cuando una tarea mencione cloudflare, workers, worker, wrangler. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-backend-builder`. **Revisor independiente:** `vx-workers-adviser`. **Prerequisitos de conocimiento:** `vx-implementation-handoff`.

## Ejecución

1. Leer compatibility_date y bindings actuales.
2. Contrastar límites y firmas con documentación vigente.
3. Evitar estado mutable global por request.
4. Usar ctx.waitUntil y Durable Objects apropiadamente.
5. Tests aislados y DEV por URL.
6. Producción solo con autorización..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://github.com/cloudflare/skills
