---
name: vx-incident-diagnosis
description: "Usar al investigar incidentes operativos, degradación o caída en servicio con logs, impacto, mitigación y causa; no activar para errores normales sin incidente."
metadata:
  version: "0.2.2"
  last_modified: "2026-11-22"
  origin: "vx-original"
---

# VX — Investigar incidentes sin efectos destructivos

**Activación:** Usar para investigar incidentes sin efectos destructivos cuando una tarea mencione incidente, error, caida, regresion. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-researcher`. **Revisor independiente:** `vx-security-reviewer`. **Prerequisitos de conocimiento:** `vx-debugging-root-cause`.

## Ejecución

1. Acotar impacto y línea temporal.
2. Buscar cambio causal con evidencia.
3. Preparar contención reversible, no ejecutarla en producción desde rol lector.
4. Reproducir en entorno aislado.
5. Cerrar RCA con pruebas y limitaciones..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://sre.google/workbook/incident-response/
