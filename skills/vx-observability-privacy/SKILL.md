---
name: vx-observability-privacy
description: "Usar para diseñar observabilidad sin filtrar datos cuando una tarea mencione logs, metricas, trazas, observabilidad. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Diseñar observabilidad sin filtrar datos

**Activación:** Usar para diseñar observabilidad sin filtrar datos cuando una tarea mencione logs, metricas, trazas, observabilidad. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-backend-builder`. **Revisor independiente:** `vx-security-reviewer`. **Prerequisitos de conocimiento:** `vx-requirements-acceptance`.

## Ejecución

1. Definir request/trace ID, latencia, error y señales.
2. Minimizar campos y cardinalidad, retención explícita.
3. Prohibir prompts, tokens y payloads privados.
4. Validar DEV/STAGING si hay permiso.
5. Contadores no prueban calidad de agentes..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://opentelemetry.io/docs/concepts/observability-primer/
