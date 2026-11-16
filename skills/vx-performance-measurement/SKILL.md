---
name: vx-performance-measurement
description: "Usar para medir rendimiento con línea base verificable cuando una tarea mencione rendimiento, latencia, performance, lighthouse. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Medir rendimiento con línea base verificable

**Activación:** Usar para medir rendimiento con línea base verificable cuando una tarea mencione rendimiento, latencia, performance, lighthouse. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-test-analyst`. **Revisor independiente:** `vx-inspector`. **Prerequisitos de conocimiento:** `vx-test-regression`.

## Ejecución

1. Definir métrica y equipo/entorno.
2. Medir baseline y resultado en condiciones comparables.
3. Analizar waterfalls, bundle o N+1.
4. No inventar p95/LCP.
5. No realizar stress de producción sin autorización..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://web.dev/vitals/
