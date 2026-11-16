---
name: vx-accessibility-review
description: "Usar para evaluar accesibilidad wcag relevante cuando una tarea mencione accesibilidad, wcag, aria, teclado. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Evaluar accesibilidad WCAG relevante

**Activación:** Usar para evaluar accesibilidad wcag relevante cuando una tarea mencione accesibilidad, wcag, aria, teclado. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-frontend-adviser`. **Revisor independiente:** `vx-inspector`. **Prerequisitos de conocimiento:** `vx-frontend-quality`.

## Ejecución

1. Inspeccionar semántica, labels, navegación teclado, orden de foco, errores y movimiento reducido.
2. Pruebas manuales cuando posible.
3. Reportar criterio, elemento y repro.
4. Un scanner no demuestra conformidad total..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://www.w3.org/WAI/WCAG22/quickref/
