---
name: vx-dev-observability-privacy
description: "Revisa logs, métricas, traces y señales operativas con foco en utilidad diagnóstica y minimización de datos. Usar cuando faltan señales, correlación, retención, redacción de secretos o límites de privacidad en observabilidad."
compatibility: "Read-only; no conecta backends de observabilidad ni cambia retención."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "observability"
---

# VX Dev — Observability Privacy

## Protocolo
1. Mapear eventos críticos, fallos y preguntas operativas que deben poder responderse.
2. Revisar señales: logs, métricas y traces; evitar duplicación sin propósito.
3. Exigir correlación entre componentes cuando exista flujo distribuido.
4. Revisar cardinalidad, volumen, retención y costo potencial.
5. Detectar secretos, tokens, PII y payloads innecesarios.
6. Preferir identificadores mínimos, datos normalizados y redacción.
7. Distinguir señal para debugging de señal para auditoría.
8. Identificar gaps de alertabilidad sin inventar umbrales no definidos.

## Salida
`OBSERVABILITY_QUESTIONS`, `SIGNAL_MAP`, `CORRELATION_GAPS`, `PRIVACY_RISKS`, `RETENTION_RISKS`, `ALERTABILITY_GAPS`.

## Integración de evidencia/MCP
- Sentry/Chrome DevTools/browser pueden contener telemetría, headers, sesiones o PII; aplicar `vx-dev-mcp-sensitive-data`.
- Preferir métricas/IDs normalizados sobre payloads completos.
- No copiar logs sensibles a handoffs si basta con un resumen y un identificador reusable.
