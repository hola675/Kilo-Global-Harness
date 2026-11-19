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
9. Diseñar para la verdad actual, no para conservar topologías/versiones supersedidas.
10. Antes de añadir un test, comprobar si debe actualizar o reemplazar uno existente.
11. Si el nuevo test reemplaza completamente el oráculo anterior, marcar el viejo como supersedido y retirarlo del CI tras PASS del reemplazo.
12. Mantener un regression guard solo si el riesgo sigue siendo plausible y distinto.
13. No convertir historia de certificación en una suite activa permanente; la historia vive en Git/evidencia.

## Estados de evidencia
`PASS`/`FAIL` solo con ejecución real identificada. En otro caso `NO_EJECUTADO` o `NO_VERIFICADO`.

## Salida
`INVARIANTS`, `TEST_MATRIX`, `TEST_ORACLES`, `REGRESSION_SURFACE`, `ACCEPTANCE_GAPS`, `VERIFICATION_PLAN`, `EXECUTION_EVIDENCE`.

## Integración de evidencia/MCP
- MCP puede aportar evidencia existente (CI, browser, logs, source remoto), pero esta skill no convierte esa evidencia en PASS sin ejecución identificable.
- Usar GitHub/Playwright/Sentry solo cuando cubran el oráculo del caso propuesto y estén autorizados.
- Registrar `NO_EJECUTADO` cuando solo exista diseño de prueba.
