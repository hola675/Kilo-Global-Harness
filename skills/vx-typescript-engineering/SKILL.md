---
name: vx-typescript-engineering
description: "Usar para implementar typescript y node mantenibles cuando una tarea mencione typescript, tsconfig, tsc, node. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Implementar TypeScript y Node mantenibles

**Activación:** Usar para implementar typescript y node mantenibles cuando una tarea mencione typescript, tsconfig, tsc, node. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-backend-builder`. **Revisor independiente:** `vx-test-analyst`. **Prerequisitos de conocimiento:** `vx-implementation-handoff`.

## Ejecución

1. Leer versiones reales y tsconfig.
2. Validar entradas externas en runtime.
3. Prohibir any y casts para ocultar fallos.
4. Controlar async, AbortSignal y timeouts.
5. Ejecutar scripts de proyecto y tests si autorizados.
6. Reportar compilación real..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://www.typescriptlang.org/docs/
