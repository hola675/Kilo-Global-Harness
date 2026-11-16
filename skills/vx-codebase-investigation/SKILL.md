---
name: vx-codebase-investigation
description: "Usar para inspeccionar código y dependencias con procedencia cuando una tarea mencione explorar, investigar, simbolo, rastrear. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Inspeccionar código y dependencias con procedencia

**Activación:** Usar para inspeccionar código y dependencias con procedencia cuando una tarea mencione explorar, investigar, simbolo, rastrear. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-researcher`. **Revisor independiente:** `vx-inspector`. **Prerequisitos de conocimiento:** ninguno.

## Ejecución

1. Registrar commit/árbol.
2. Buscar símbolos concretos, consumidores y tests.
3. Corroborar rutas/lineas actuales.
4. Usar índice/LSP si verificable o read/grep.
5. Clasificar hipótesis/no verificado.
6. No copiar sesiones ni secretos..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://kilo.ai/docs/customize/custom-subagents
