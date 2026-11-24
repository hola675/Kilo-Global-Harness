---
name: vx-test-regression
description: "Auditar en solo lectura el sistema de pruebas ANTES de ejecutarlo o añadir tests: inventariar volumen, complejidad, duplicación, rutas CI y coste estimado; optimizar UPDATE/REPLACE/ADD y ejecutar solo tras superar los gates. Usar al crear, modificar, revisar o acelerar pruebas."
metadata:
  version: "0.3.0"
  last_modified: "2026-11-22"
---

# VX Test Regression

**Ámbito:** convertir criterios de aceptación en tests de proyecto autorizados; guía para `vx-qa-builder` y el integrador. Skill VX original; no otorga `edit`, `bash` ni acceso a MCP.

## Gate obligatorio AUDIT_FIRST — no ejecutar pruebas antes de evaluar el sistema

**Regla de precedencia:** antes de ejecutar `test`, `pytest`, `vitest`, `playwright`, `build` como sustituto de test, o lanzar un workflow de pruebas, realizar **inventario estático de solo lectura** del sistema existente. La auditoría no invoca el runner, no instala dependencias, no arranca servicios y no crea artefactos. Si el repositorio no puede inspeccionarse, estado `AUDIT_BLOCKED`; no inventar resultados.

1. Localizar manifiestos de paquetes, configuración de runners, workflows, scripts `test:*`, carpetas `tests`/`__tests__`, fixtures, helpers y documentación. Distinguir archivos ejecutables de soporte, capturas, snapshots y nombres con `test` que no son tests.
2. Construir el **mapa real de ejecución**: script → runner → globs → suites → casos → entorno. Detectar rutas inalcanzables, suites repetidas en scripts o CI, pruebas obsoletas, tests que validan únicamente texto o mocks, y E2E que deberían ser unitarios. No confundir cantidad de archivos con cantidad de casos ejecutados.
3. Clasificar cada suite por invariante, capa, riesgo, coste, datos, entorno y gate propietario. Estimar coste por estructura (setup, red, navegador, bases de datos, secuencialidad); **no declarar tiempos reales** sin métricas de CI o ejecución previa verificables.
4. Evaluar los tres presupuestos **antes de correr**: complejidad (mantenibilidad, fragilidad, duplicación y número de oráculos por riesgo), volumen (casos únicos necesarios frente a cobertura duplicada) y rapidez (duración histórica por gate y latencia de feedback). Si no hay baseline, marcar `UNKNOWN`, obtener métricas de CI existentes o definir un presupuesto provisional aprobado; nunca fabricar segundos o límites universales.
5. Clasificar `AUDIT_PASS`, `OPTIMIZATION_REQUIRED` o `AUDIT_BLOCKED` y documentar evidencia por archivo, comando y ruta. Un conteo elevado es **señal de revisión**, no autorización para borrar cobertura.
6. Si `OPTIMIZATION_REQUIRED`, proponer/implementar optimización de tests y CI **sin ejecutar primero la suite completa**: consolidar invariantes duplicadas, parametrizar casos, eliminar wrappers históricos, reducir setups repetidos, mover verificaciones al nivel más barato y ajustar selección por impacto. Preservar casos negativos, seguridad, permisos, migraciones y contratos.
7. Para retirar pruebas, establecer matriz `OLD_CASE → NEW_CASE → INVARIANT → ORACLE → RISK → EQUIVALENCE_EVIDENCE`. Hasta comprobar equivalencia mediante ejecución autorizada focalizada, no borrar ni desactivar cobertura. Ejecutar después el subconjunto focalizado y los gates requeridos por CI; solo entonces certificar.
8. Tras la optimización, registrar métricas `before/after` de archivos, casos, suites, rutas ejecutadas, duplicaciones y duración **solo si existe medición**. Sin baseline de duración, declarar `SPEED_UNVERIFIED`, nunca un porcentaje supuesto.

### Presupuestos adaptativos y umbrales de alerta

- **Complejidad:** un test debe proteger una invariante identificable con oráculo independiente; señalar tests con múltiples responsabilidades, mocks que replican implementación, fixtures globales mutables o lógica de harness mayor que el código protegido. No exigir un test por función ni por versión.
- **Volumen:** inventariar conteo por dominio y capa; revisar concentraciones inusuales, series `v1/v2/v3`, duplicados semánticos, suites sin propietario y múltiples runners sobre los mismos casos. No establecer máximo fijo de tests para todos los proyectos.
- **Rapidez:** definir presupuesto por feedback de PR (focalizado), gate de integración y certificación de release; usar duraciones históricas de CI cuando existan. Si no existen, marcar `UNKNOWN` y medir tras el inventario, nunca ejecutar una suite gigante solo para estimar su coste.
- **Prioridad:** seguridad e integridad > contratos y regresiones críticas > comportamiento nuevo > redundancias editoriales. Reducir coste **sin reducir riesgos cubiertos**.
- **Escalado:** el análisis estático puede sugerir optimización, pero un cambio destructivo de suite requiere equivalencia probada y autorización acorde al alcance.

### Ejemplo de alerta: Vecidya (inventario estático, no certificación)

El repositorio `hola675/Vecidya` mostró el 2026-11-22 un inventario orientativo de **324 archivos** con patrones de test/check en carpetas de pruebas, de ellos **202** bajo `vecidya-platform/tests/unit/diagnostic`. Es un indicador de concentración que exige examinar suites, globs y oráculos; **no demuestra por sí solo redundancia, lentitud ni que todos se ejecuten**. No ejecutar ni modificar Vecidya al auditar la Skill del Harness. Antes de consolidar ese proyecto, analizar sus scripts de `package.json`, CI, invariantes únicas y equivalencia.

## Preparación

Identificar el framework de tests y sus dependencias ya presentes. Recibir alcance de cambios, rutas permitidas, línea base, escenario, oráculos verificables y restricciones. Evitar tests contra producción, bases de datos reales, endpoints que incurran en cargos o credenciales.

## Certificación viva

Antes de escribir o proponer un test:

1. Identificar la invariante actual.
2. Clasificar la acción como `UPDATE`, `REPLACE` o `ADD`.
3. `ADD` solo cuando exista riesgo diferencial.
4. Si `REPLACE`, mantener temporalmente el test anterior únicamente hasta obtener PASS real del reemplazo.
5. Tras PASS, retirar el supersedido del CI activo si el alcance autorizado lo permite.
6. No crear suites nuevas solo porque cambió la versión del componente.
7. La historia queda en Git/PR/registry, no en tests activos duplicados.

## Selección y optimización de pruebas

1. Identificar el cambio observable y el **oráculo independiente**: no basta comprobar que existe una frase, archivo o mock si el riesgo es funcional.
2. Buscar la prueba existente más cercana y decidir `UPDATE`, `REPLACE` o `ADD` antes de escribir. `ADD` requiere nueva invariante o riesgo que ninguna prueba cubra.
3. Ejecutar primero la prueba focalizada. Ampliar a contrato, integración, smoke o E2E cuando cambien interfaces, dependencias, instalación, concurrencia o seguridad.
4. Mantener temporalmente el test antiguo durante `REPLACE`; retirar solo cuando el reemplazo haya pasado y cubra los mismos riesgos. Si no puede demostrarse equivalencia, conservar ambos y explicar la diferencia.
5. Evitar suites por versión, nombres históricos y reejecución completa de gates anteriores sin motivo. CI mantiene la cobertura vigente y la historia queda en Git.
6. Medir coste cuando resulte relevante: duración, repetición, flakiness y mantenimiento. Optimizar sin reducir las invariantes verificadas.
7. Separar `SOURCE_PASS`, `CI_PASS` y `HOST_RUNTIME_PASS`. Un test local o CI nunca certifica herramientas reales del host ni instalación.

## Casos mínimos por cambio

- **Positivos:** resultado esperado para entrada permitida.
- **Negativos:** error ante entrada inválida, autorización insuficiente y estados límite.
- **Regresión:** caso vinculado a comportamiento anterior que debe mantenerse.
- **Idempotencia/concurrencia:** solo si aplica al código bajo prueba.
- **Aislamiento:** fixtures desechables, no datos del cliente ni secretos.

## Salida objetiva

Para cada test: `case_id`, propósito, entrada sintética, aserción, ruta, comando de ejecución y estado `NO_EJECUTADO|PASS|FAIL|SKIP`. Solo declarar PASS/FAIL si hay ejecución real y exit code. Si el agente no puede usar terminal, remitir comandos al ejecutor autorizado y mantener `NO_EJECUTADO`.

Una suite ejecutada no certifica automáticamente competencia, enseñanza ni promoción. El revisor independiente analiza calidad del oráculo y falsos positivos. No modificar herramientas, permisos, HOME ni MCP por una skill.
