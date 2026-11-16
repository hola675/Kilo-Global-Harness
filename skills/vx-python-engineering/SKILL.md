---
name: vx-python-engineering
description: "Usar para implementar python reproducible cuando una tarea mencione python, pytest, unittest, typing. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Implementar Python reproducible

**Activación:** Usar para implementar python reproducible cuando una tarea mencione python, pytest, unittest, typing. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-backend-builder`. **Revisor independiente:** `vx-test-analyst`. **Prerequisitos de conocimiento:** `vx-implementation-handoff`.

## Ejecución

1. Detectar Python/dependencias existentes.
2. Aislar disco/red con fixtures.
3. Validar rutas y encoding.
4. Tipar contratos, manejar errores.
5. Ejecutar compileall, pruebas y linters si instalados.
6. No ejecutar pip ni scripts externos silenciosamente..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://docs.python.org/3/
