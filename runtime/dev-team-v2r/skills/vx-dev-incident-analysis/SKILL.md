---
name: vx-dev-incident-analysis
description: "Analiza incidentes de software o runtime mediante timeline, impacto, señales y evidencia sin ejecutar mitigaciones. Usar ante caída, degradación, errores intermitentes o postmortem para separar síntoma, contención, causa y prevención."
compatibility: "Read-only; no reinicia servicios, no cambia producción y no declara causa raíz sin evidencia."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "incident"
---

# VX Dev — Incident Analysis

## Frontera
`vx-dev-debug-triage` trabaja hipótesis técnicas locales; esta skill añade timeline, blast radius, impacto, mitigación y aprendizaje operacional.

## Protocolo
1. Construir timeline con timestamps y fuentes.
2. Definir impacto, alcance y componentes afectados.
3. Separar detección, síntoma, factor contribuyente, mitigación y causa.
4. Correlacionar cambios recientes con evidencia, no solo proximidad temporal.
5. Identificar señales ausentes que retrasaron detección o diagnóstico.
6. Registrar acciones de contención como distintas de fixes permanentes.
7. Clasificar unknowns y evidencia contradictoria.
8. Proponer prevención solo después de sostener la cadena causal.

## Salida
`TIMELINE`, `IMPACT`, `BLAST_RADIUS`, `EVIDENCE`, `CONTRIBUTING_FACTORS`, `ROOT_CAUSE_STATUS`, `DETECTION_GAPS`, `PREVENTION_CANDIDATES`.

## Integración de evidencia/MCP
- Sentry, GitHub y observabilidad de plataforma son fuentes típicas si están autorizadas.
- Construir timeline con timestamps/IDs exactos y distinguir cambio reciente de causalidad.
- Minimizar datos sensibles y entregar al líder un handoff con timeline, evidencia y gaps.
