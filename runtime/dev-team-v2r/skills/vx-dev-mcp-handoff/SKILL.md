---
name: vx-dev-mcp-handoff
description: "Empaqueta resultados MCP para transferirlos entre subagentes y líder sin repetir consultas ni perder procedencia. Usar cuando un especialista obtuvo evidencia que otro rol necesita para continuar."
compatibility: "Respeta depth=1: los subagentes no delegan; producen un handoff para el líder."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "mcp-handoff"
---

# VX Dev — MCP Handoff

## Formato
`QUESTION → TOOL_USED → EVIDENCE → DECISION_RELEVANCE → GAPS → REUSE_KEYS`

1. Resumir la pregunta que motivó la llamada.
2. Indicar servidor/tool exacta y si fue realmente ejecutada.
3. Incluir solo hallazgos que cambian una decisión o siguiente paso.
4. Añadir URL/ID/SHA/ruta necesarios para reutilizar la evidencia.
5. Marcar datos sensibles; no retransmitir payloads completos si no hacen falta.
6. Indicar qué NO fue verificado.
7. El siguiente agente debe reutilizar el handoff antes de volver a consultar.
8. Si necesita otra fuente, explicar el gap que justifica la nueva llamada.

## Salida
`MCP_HANDOFF` compacto, normalmente menor que el resultado original.
