---
name: vx-dev-mcp-capability-routing
description: "Selecciona el MCP y la tool adecuada según la intención, evidencia requerida, coste y riesgo. Usar cuando hay varias herramientas posibles o cuando líder/subagente necesita decidir si usar MCP, una tool nativa o ninguna."
compatibility: "Advisory-only; no concede acceso a servidores ni tools no visibles para el agente actual."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "mcp-routing"
---

# VX Dev — MCP Capability Routing

## Regla principal
Disponibilidad no implica necesidad ni autorización. Elegir la herramienta mínima que produzca evidencia suficiente.

## Secuencia
1. Definir la pregunta exacta y el artefacto esperado.
2. Preferir evidencia local/nativa cuando cubra la necesidad con menor riesgo.
3. Si hace falta MCP, clasificar la intención:
   - documentación/estándares;
   - navegación de código;
   - repositorio/PR/CI;
   - navegador/runtime UI;
   - observabilidad/producción;
   - seguridad/dependencias;
   - API/workspaces;
   - infraestructura;
   - reverse engineering;
   - generación visual.
4. Consultar solo servidores/tools visibles para el rol actual.
5. Elegir una tool exacta, no un wildcard de servidor.
6. Evitar llamadas paralelas redundantes a varias fuentes equivalentes.
7. Escalar a una segunda fuente solo para corroborar, resolver contradicción o cubrir un gap.
8. Si ninguna tool autorizada cubre la necesidad, registrar `CAPABILITY_GAP`; no improvisar bypass.

## Salida
`INTENT`, `EVIDENCE_NEEDED`, `CANDIDATE_TOOLS`, `SELECTED_TOOL`, `WHY`, `RISK_CLASS`, `FALLBACK`.
