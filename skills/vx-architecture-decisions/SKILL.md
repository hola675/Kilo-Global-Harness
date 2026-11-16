---
name: vx-architecture-decisions
description: "Usar para redactar decisiones de arquitectura y límites cuando una tarea mencione arquitectura, adr, modular, diseno. Exigir evidencia real y no cambiar permisos."
metadata:
  version: "0.2.0"
  origin: "vx-original"
---

# VX — Redactar decisiones de arquitectura y límites

**Activación:** Usar para redactar decisiones de arquitectura y límites cuando una tarea mencione arquitectura, adr, modular, diseno. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-integrador`. **Revisor independiente:** `vx-inspector`. **Prerequisitos de conocimiento:** `vx-requirements-acceptance`.

## Ejecución

1. Analizar diseño actual y consumidores.
2. Evaluar alternativas, coste, seguridad y compatibilidad.
3. Elegir mínima intervención.
4. Redactar ADR versionado con riesgos y reversión.
5. No convertir diseño en permisos efectivos..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://github.com/addyosmani/agent-skills
