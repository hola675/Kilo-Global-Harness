---
name: vx-api-contract-design
description: "Usar al crear o cambiar contratos HTTP/API, endpoints, webhooks, OpenAPI, validación y compatibilidad de consumidores; no activar por menciones incidentales de API sin cambios de interfaz."
metadata:
  version: "0.2.1"
  last_modified: "2026-11-22"
  origin: "vx-original"
---

# VX — Diseñar y modificar APIs compatibles

**Activación:** Usar para diseñar y modificar apis compatibles cuando una tarea mencione api, endpoint, webhook, openapi. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-backend-builder`. **Revisor independiente:** `vx-security-reviewer`. **Prerequisitos de conocimiento:** `vx-requirements-acceptance`.

## Ejecución

1. Identificar consumidores actuales.
2. Definir schemas, errores, auth, paginación y límites.
3. Validar webhooks/idempotencia/reintentos.
4. Establecer versionado o expand-migrate-contract.
5. Agregar contract tests.
6. No exponer endpoint productivo por defecto..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://owasp.org/API-Security/editions/2023/en/0x11-t10/
