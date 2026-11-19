---
name: vx-dev-mcp-tool-contract
description: "Inspecciona el contrato efectivo de una tool MCP antes de usarla: schema, efectos, auth, sensibilidad y límites. Usar ante tools nuevas, ambiguas, dinámicas o cuando un nombre read-like podría ocultar mutación."
compatibility: "Read-only analysis; annotations como readOnlyHint son hints, no enforcement."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "mcp-contract"
---

# VX Dev — MCP Tool Contract

## Checklist
1. Identificar servidor, tool, versión/snapshot y namespace efectivo.
2. Leer descripción, inputSchema, outputSchema y annotations.
3. Clasificar efecto: READ_SAFE, READ_SENSITIVE, EXTERNAL_PROCESSING, MUTABLE, DESTRUCTIVE, MIXED o UNKNOWN.
4. Identificar filesystem, network, browser, account o remote-state side effects.
5. Revisar auth/scopes y si requiere consentimiento adicional.
6. Enumerar datos enviados y datos potencialmente devueltos.
7. Validar parámetros obligatorios y defaults peligrosos.
8. No confiar solo en nombre, descripción o `readOnlyHint`.
9. Si schema/superficie cambió respecto al snapshot revisado, volver a evaluar.

## Salida
`TOOL_CONTRACT`, `RISK_CLASS`, `DATA_BOUNDARY`, `AUTH_SCOPE`, `SIDE_EFFECTS`, `SAFE_CALL_SHAPE`, `DECISION`.
