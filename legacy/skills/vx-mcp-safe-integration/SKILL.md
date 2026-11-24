---
name: vx-mcp-safe-integration
description: "Usar al conectar, evaluar o cambiar servidores y herramientas MCP, scopes, límites de confianza y permisos; no activar por una consulta normal a un MCP autorizado."
metadata:
  version: "0.2.2"
  last_modified: "2026-11-22"
  origin: "vx-original"
---

# VX — Evaluar MCP sin tocar conexiones activas

**Activación:** Usar para evaluar mcp sin tocar conexiones activas cuando una tarea mencione mcp, serena, context7, github connector. Exigir evidencia real y no cambiar permisos.

**Responsable sugerido:** `vx-researcher`. **Revisor independiente:** `vx-security-reviewer`. **Prerequisitos de conocimiento:** `vx-supply-chain-review`.

## Ejecución

1. Contar solo nombres de MCP configurados.
2. Cotejar proveedor, versión, scopes, OAuth y riesgo.
3. Prueba read-only con autorización explícita.
4. Conservar todos los MCP existentes.
5. Ningún nombre de config acredita conexión.
6. Aprobación individual para nuevos..

## Handoff y seguridad

Entregar `{task_id,base_sha,files_or_symbols,interfaces,tests_executed,tests_not_executed,evidence,risks,reviewer}`. Si los datos no están disponibles, usar `NO_VERIFICADO` o `NO_EJECUTADO`, nunca PASS inventado. No tocar HOME de Kilo, permisos, AutoApprove, credenciales, MCP ni producción por activar esta skill. Usar permisos reales y revisar con una identidad de agente distinta; el propietario no se autoaprueba.

**Fuente de referencia técnica para diseño propio VX:** https://kilo.ai/docs/customize/skills
