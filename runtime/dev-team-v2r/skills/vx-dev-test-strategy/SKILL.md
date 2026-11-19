---
name: vx-dev-test-strategy
description: "Diseña estrategia de pruebas y evidencia de aceptación sin ejecutar tests. Usar para convertir requisitos/cambios en invariantes, matriz de casos, oráculos, superficie de regresión y gates de CI."
compatibility: "Read-only; Quality no ejecuta tests ni convierte tests escritos en PASS."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "quality"
---

# VX Dev — Test Strategy

## Protocolo
1. Extraer comportamiento observable e invariantes.
2. Separar casos positivos, negativos, límites, autorización y regresión.
3. Elegir nivel mínimo eficaz: unit, integration, contract, E2E o manual.
4. Definir oráculo independiente; evitar tests que solo validan mocks.
5. Priorizar por riesgo y superficie modificada.
6. Mantener fixtures sintéticos y deterministas.
7. Para bugs, incluir caso que capture la regresión.
8. Distinguir test existente, test propuesto y test ejecutado.

## Estados de evidencia
`PASS`/`FAIL` solo con ejecución real identificada. En otro caso `NO_EJECUTADO` o `NO_VERIFICADO`.

## Salida
`INVARIANTS`, `TEST_MATRIX`, `TEST_ORACLES`, `REGRESSION_SURFACE`, `ACCEPTANCE_GAPS`, `VERIFICATION_PLAN`, `EXECUTION_EVIDENCE`.
