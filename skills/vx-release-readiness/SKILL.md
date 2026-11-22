---
name: vx-release-readiness
description: "Usar para preparar entrega y rollback sin desplegar cuando una tarea mencione release, deploy, staging, rollback. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  last_modified: "2026-11-21"
  origin: "vx-original"
---

# VX — Preparar entrega y rollback sin desplegar

**Activación:** Usar para preparar entrega y rollback sin desplegar cuando una tarea mencione release, deploy, staging, rollback. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-integrador`. **Revisor independiente:** `vx-security-reviewer`. **Prerequisitos de conocimiento:** `vx-git-ci-quality`, `vx-requirements-acceptance`.

## Ejecución

1. Anclar SHA, versión, changelog, pruebas y aprobaciones.
2. Pruebas DEV/STAGING por URL real cuando autorizado.
3. Detallar rollback de código y datos por separado.
4. Producción requiere solicitud concreta.
5. No activar scheduler..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://docs.github.com/en/actions
