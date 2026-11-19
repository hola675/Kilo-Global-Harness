---
name: vx-dev-doc-traceability
description: "Construye trazabilidad entre requisitos, decisiones, código, pruebas y documentación sin editar archivos. Usar cuando una afirmación debe vincularse a evidencia, hay documentación desfasada o faltan relaciones entre cambio y justificación."
compatibility: "Read-only; no reescribe documentación ni sustituye source reconciliation."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "traceability"
---

# VX Dev — Documentation Traceability

## Frontera
`vx-dev-source-reconciliation` decide qué fuente respalda una afirmación; esta skill construye la cadena requisito → decisión → implementación → prueba → documentación.

## Protocolo
1. Elegir el objeto trazado: requisito, decisión, cambio o release.
2. Registrar IDs, rutas, SHAs, ADRs, issues o pruebas existentes.
3. Construir enlaces solo cuando exista evidencia.
4. Marcar referencias huérfanas, rotas o desactualizadas.
5. Distinguir documentación normativa de descriptiva.
6. Señalar cambios de comportamiento sin actualización documental.
7. Evitar inferir que proximidad textual implica relación causal.

## Salida
`TRACE_GRAPH`, `SUPPORTED_LINKS`, `ORPHANS`, `STALE_REFERENCES`, `DOCUMENTATION_GAPS`, `EVIDENCE_REQUIRED`.
