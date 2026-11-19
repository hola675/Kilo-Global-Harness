---
name: vx-dev-mcp-evidence-ledger
description: "Registra procedencia y estado de evidencia obtenida por MCP para que líder y subagentes puedan reutilizarla sin repetir llamadas. Usar en investigación, arquitectura, revisión, debugging o decisiones apoyadas por herramientas externas."
compatibility: "No convierte outputs MCP en verdad; exige distinguir observado, documentado, inferido y desconocido."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "mcp-evidence"
---

# VX Dev — MCP Evidence Ledger

## Registro mínimo por hallazgo
- servidor y tool exacta;
- consulta/inputs relevantes;
- fuente, URL, repo, SHA, issue, trace o identificador;
- versión/fecha cuando importe;
- dato observado;
- clasificación: OBSERVED / DOCUMENTED / CORROBORATED / INFERRED / UNKNOWN;
- confianza;
- limitaciones.

## Reglas
1. Un output de tool demuestra solo lo que realmente contiene.
2. No mezclar evidencia de versiones distintas sin marcarlo.
3. Si dos MCP discrepan, registrar contradicción en vez de elegir silenciosamente.
4. Reutilizar identificadores estables en llamadas posteriores.
5. En handoff, transmitir hechos destilados y referencias, no blobs completos.
6. Diferenciar “tool ejecutada” de “resultado validado”.
7. No registrar secretos ni tokens en el ledger.

## Salida
`EVIDENCE_LEDGER`, `CONTRADICTIONS`, `REUSABLE_IDS`, `UNKNOWNS`.
