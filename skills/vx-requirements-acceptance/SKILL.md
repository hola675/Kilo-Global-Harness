---
# last_modified: 2026-11-21
name: vx-requirements-acceptance
description: "Usar para convertir objetivos en criterios de aceptación verificables cuando una tarea mencione brief, requisito, aceptacion, alcance. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "1.0.0"
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Convertir objetivos en criterios de aceptación verificables

**Activación:** Usar para convertir objetivos en criterios de aceptación verificables cuando una tarea mencione brief, requisito, aceptacion, alcance. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-integrador`. **Revisor independiente:** `vx-inspector`. **Prerequisitos de conocimiento:** ninguno.

## Ejecución

1. Separar hechos de supuestos.
2. Definir historias con casos de éxito, error, autorización y bordes.
3. Mapear criterios a pruebas.
4. Declarar exclusiones y aprobaciones pendientes..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://agentskills.io/specification
