---
name: vx-dev-regression-analysis
description: "Analiza superficie de regresión de un cambio y diseña controles focalizados. Usar cuando hay que identificar qué comportamiento existente podría romperse, qué pruebas deben protegerlo o cómo aislar una regresión observada."
compatibility: "Read-only; no ejecuta tests y no duplica la estrategia global de pruebas."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "regression"
---

# VX Dev — Regression Analysis

## Frontera
`vx-dev-test-strategy` diseña cobertura general; esta skill se centra en impacto del cambio sobre comportamiento ya existente.

## Protocolo
1. Identificar contrato o comportamiento previo que debe conservarse.
2. Mapear componentes, consumidores y datos afectados.
3. Revisar cambios de defaults, orden, errores, timeouts y compatibilidad.
4. Priorizar caminos de alto uso o alto costo de fallo.
5. Diseñar controles que fallen con la regresión concreta.
6. Distinguir regresión confirmada de riesgo de regresión.
7. Buscar equivalencia de resultados, no solo ausencia de excepciones.
8. Registrar evidencia before/after cuando exista.

## Salida
`PREVIOUS_BEHAVIOR`, `CHANGE_SURFACE`, `REGRESSION_RISKS`, `FOCUSED_TESTS`, `BEFORE_AFTER_EVIDENCE`, `UNPROTECTED_CONTRACTS`.
