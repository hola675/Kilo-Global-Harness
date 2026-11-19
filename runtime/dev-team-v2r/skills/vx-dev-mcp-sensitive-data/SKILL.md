---
name: vx-dev-mcp-sensitive-data
description: "Minimiza datos sensibles enviados o recibidos por MCP y define qué debe redactarse, resumirse o no consultarse. Usar con repos privados, telemetría, sesiones de navegador, cuentas, logs, código propietario o datos de cliente."
compatibility: "Defensiva; no concede acceso a secretos ni modifica políticas de retención."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "mcp-data-protection"
---

# VX Dev — MCP Sensitive Data

## Reglas
1. Enviar solo campos estrictamente necesarios para responder la pregunta.
2. Nunca incluir tokens, passwords, cookies, Authorization headers, private keys o secretos.
3. Tratar código privado, issues, logs, traces y screenshots autenticados como READ_SENSITIVE.
4. Preferir IDs, hashes, snippets mínimos o datos normalizados frente a payloads completos.
5. Antes de usar servicio externo, identificar qué datos salen del host y con qué propósito.
6. No copiar datos sensibles del output a documentación, handoffs o logs sin necesidad.
7. Redactar PII y valores de negocio cuando no sean esenciales.
8. Si no puede responderse sin exposición desproporcionada, registrar `DATA_BOUNDARY_BLOCK`.

## Salida
`DATA_CLASS`, `MINIMUM_INPUT`, `REDACTIONS`, `EXTERNAL_BOUNDARY`, `SAFE_OUTPUT`, `BLOCK_IF_NEEDED`.
