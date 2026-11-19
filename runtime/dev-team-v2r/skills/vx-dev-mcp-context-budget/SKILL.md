---
name: vx-dev-mcp-context-budget
description: "Reduce contexto y llamadas MCP mediante descubrimiento progresivo, reutilización de resultados y selección mínima de tools. Usar cuando hay muchos servidores/tools, respuestas grandes o cadenas MCP que consumen contexto."
compatibility: "Advisory-only; no cambia configuración del host ni activa servidores."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "mcp-context"
---

# VX Dev — MCP Context Budget

## Patrón
`CATALOG → INSPECT → EXECUTE → DISTILL → REUSE`

1. Cargar solo nombres/descripciones suficientes para descubrir candidatos.
2. Inspeccionar schema completo únicamente de la tool elegida.
3. Ejecutar la menor cantidad de llamadas que responda la pregunta.
4. Destilar resultados grandes a hechos, IDs, rutas y evidencia útil.
5. Reutilizar IDs/URLs/SHAs ya obtenidos; no repetir búsquedas.
6. Mantener resultados intermedios fuera del handoff cuando no aporten decisión.
7. Agrupar por servidor para evitar confusión entre tools homónimas.
8. Si el host soporta cache/list_changed, tratar catálogo stale al cambiar la lista.
9. No sacrificar seguridad por ahorrar tokens.

## Señales de sobreuso
- repetir `tools/list` sin cambio;
- buscar lo mismo en varias fuentes;
- pasar blobs completos entre agentes;
- llamar tool de detalle antes de saber si es candidata;
- usar navegador para datos disponibles por API/docs.

## Salida
`CONTEXT_PLAN`, `MINIMUM_TOOLSET`, `REUSE_KEYS`, `DISTILLED_EVIDENCE`, `AVOIDED_CALLS`.
