---
name: vx-dev-mcp-failure-recovery
description: "Gestiona errores, timeouts, auth, rate limits, tool-not-found y resultados parciales de MCP sin caer en loops ni bypasses. Usar cuando una llamada falla o devuelve evidencia insuficiente."
compatibility: "No reautentica, cambia scopes ni usa tools mutables como fallback sin autorización."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "mcp-recovery"
---

# VX Dev — MCP Failure Recovery

## Protocolo
1. Clasificar fallo: input/schema, auth, permiso, timeout, rate-limit, server unavailable, stale catalog, partial/empty result.
2. Corregir una vez los argumentos si el error es determinista y claro.
3. No repetir ciegamente la misma llamada.
4. Ante auth/scope: detener y pedir acción/consentimiento; no buscar bypass.
5. Ante rate-limit: reducir consultas y reutilizar cache/evidencia existente.
6. Ante tool-not-found: refrescar catálogo solo si hay señal de cambio.
7. Usar fallback únicamente si produce evidencia equivalente con igual o menor riesgo.
8. Si el fallback cambia de fuente o semántica, declararlo.
9. Tras dos fallos equivalentes sin nueva información, registrar `BLOCKED_MCP`.

## Salida
`FAILURE_CLASS`, `RETRY_DECISION`, `FALLBACK`, `EVIDENCE_LOSS`, `BLOCKER`.
