---
name: vx-dev-backend-contracts
description: "Analiza contratos backend y comportamiento de servicios/APIs: validación, auth, errores, idempotencia, concurrencia e integraciones. Usar al revisar endpoints, handlers, servicios, jobs o cambios de comportamiento del dominio."
compatibility: "Read-only; no modifica código, schema físico ni producción."
metadata:
  version: "1.0.0"
  last_modified: "2026-11-21"
  origin: "vx-dev-original"
  category: "backend"
---

# VX Dev — Backend Contracts

## Protocolo
1. Reconstruir flujo request/event → handler → servicio → integración → respuesta.
2. Identificar validación, autenticación/autorización y trust boundaries.
3. Enumerar contratos de entrada/salida y errores observables.
4. Revisar idempotencia, retries, timeouts y efectos parciales cuando apliquen.
5. Distinguir reglas de dominio de detalles de persistencia.
6. Señalar failure modes con precondición y evidencia.
7. Marcar contratos asumidos o ausentes; no inventarlos.

## Salida
`SERVICE_FLOW`, `API_CONTRACTS`, `DOMAIN_RULES`, `FAILURE_MODES`, evidencia, riesgos y handoff.

Schema/índices/migraciones pertenecen a Data; amenazas transversales a Security.

## Integración de evidencia/MCP
- Para contratos en source, preferir navegación local; usar Serena/Codebase Memory si aportan relaciones semánticas necesarias.
- Para colecciones/API remota, Postman puede ser fuente contextual solo si la tool exacta está autorizada.
- Para fallos runtime, Sentry puede aportar evidencia sensible; aplicar `vx-dev-mcp-sensitive-data`.
