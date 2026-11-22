---
name: vx-dev-test-strategy
description: "Auditar en solo lectura el volumen, complejidad, duplicaciones, cobertura y coste de las pruebas existentes ANTES de ejecutar suites; diseñar optimización, oráculos y matriz UPDATE/REPLACE/ADD sin ejecutar tests. Usar para estrategia, auditoría de suites y presupuestos de CI."
compatibility: "Read-only; Quality no ejecuta tests ni convierte tests escritos en PASS."
metadata:
  version: "1.3.0"
  last_modified: "2026-11-22"
  origin: "vx-dev-original"
  category: "quality"
---

# VX Dev — Test Strategy

## Cobertura de Skills por contexto (source)

Al cambiar una Skill o su enrutamiento, usar la **suite viva** para probar `SHOULD_TRIGGER`, `SHOULD_NOT_TRIGGER`, permiso denegado y fallo de dependencia. Asegurar que un bug PySide6 no activa Tauri/Android, que una web no activa desktop y que ninguna Skill cargada crea un privilegio nuevo. Diseñar oráculos separados para `SOURCE`, `CI`, `ACL` y `RUNTIME`; no llamar PASS de runtime a una lectura de archivos. La opción `test_action` sigue siendo UPDATE, REPLACE o ADD: no construir una suite por release.

## Diagnóstico estático previo a cualquier ejecución

- Inventariar runners, scripts, globs, CI, fixtures y pruebas sin ejecutar código del proyecto. Separar archivos de pruebas, casos efectivos y rutas ejecutadas; registrar la incertidumbre.
- Clasificar `COMPLEXITY`, `VOLUME`, `SPEED` como `PASS`, `ALERT` o `UNKNOWN`. No inventar duraciones, ratios de cobertura ni presupuestos; recuperar históricos de CI si existen.
- Proponer `KEEP`, `UPDATE`, `REPLACE`, `MERGE`, `REMOVE_AFTER_EQUIVALENCE` por invariante, con coste esperado, riesgos y dependencia de validación focalizada.
- No recomendar eliminar tests por su antigüedad, cantidad o nombre. Exigir equivalencia verificable, especialmente en autorización, datos, seguridad y regresiones.
- Entregar `STATIC_AUDIT`, `EXECUTION_GRAPH`, `RISK_COVERAGE_MAP`, `BUDGET_STATUS`, `OPTIMIZATION_PLAN` y `UNVERIFIED_ASSUMPTIONS`; ninguna de estas salidas equivale a PASS de runtime.

## Protocolo
1. Extraer comportamiento observable e invariantes.
2. Separar casos positivos, negativos, límites, autorización y regresión.
3. Elegir nivel mínimo eficaz: unit, integration, contract, E2E o manual.
4. Definir oráculo independiente; evitar tests que solo validan mocks.
5. Priorizar por riesgo y superficie modificada.
6. Mantener fixtures sintéticos y deterministas.
7. Para bugs, incluir caso que capture la regresión.
8. Distinguir test existente, test propuesto y test ejecutado.
9. Clasificar la acción de testing como `UPDATE`, `REPLACE` o `ADD`.
   - `UPDATE`: el oráculo vigente sigue siendo correcto y se actualiza.
   - `REPLACE`: un nuevo test sustituye completamente al anterior; retirar el supersedido solo tras PASS real.
   - `ADD`: solo si existe una invariante o riesgo diferencial.
10. Diseñar para la verdad actual, no para conservar topologías/versiones supersedidas.
11. Antes de añadir un test, comprobar si debe actualizar o reemplazar uno existente.
12. Si el nuevo test reemplaza completamente el oráculo anterior, marcar el viejo como supersedido y retirarlo del CI tras PASS del reemplazo.
13. Mantener un regression guard solo si el riesgo sigue siendo plausible y distinto.
14. No convertir historia de certificación en una suite activa permanente; la historia vive en Git/evidencia.

## Priorización y coste de verificación

- Matriz por riesgo: `CHANGE_SURFACE`, `INVARIANT`, `EXISTING_TEST`, `TEST_ACTION`, `ORACLE`, `RISK`, `EXECUTION_LEVEL` y `ESTIMATED_COST`.
- Elegir el nivel más barato que observe la invariante real. Contratos y permisos necesitan casos negativos; concurrencia necesita intercalaciones controladas; UI crítica puede necesitar E2E.
- Distinguir una prueba de texto/metadatos válida de un falso sustituto de prueba funcional. No atar tests a formulaciones editoriales salvo que el texto sea el contrato.
- Evitar duplicar pruebas entre unit, integration y E2E salvo que protejan fallos diferentes. Los smoke de runtime solo se exigen donde la funcionalidad depende del host.
- La estrategia read-only propone qué ejecutar; el ejecutor autorizado recoge exit code y evidencia, y el revisor evalúa cobertura.

## Estados de evidencia
`PASS`/`FAIL` solo con ejecución real identificada. En otro caso `NO_EJECUTADO` o `NO_VERIFICADO`.

## Salida
`INVARIANTS`, `TEST_MATRIX`, `TEST_ORACLES`, `REGRESSION_SURFACE`, `ACCEPTANCE_GAPS`, `VERIFICATION_PLAN`, `EXECUTION_EVIDENCE`.

## Integración de evidencia/MCP
- MCP puede aportar evidencia existente (CI, browser, logs, source remoto), pero esta skill no convierte esa evidencia en PASS sin ejecución identificable.
- Usar GitHub/Playwright/Sentry solo cuando cubran el oráculo del caso propuesto y estén autorizados.
- Registrar `NO_EJECUTADO` cuando solo exista diseño de prueba.
