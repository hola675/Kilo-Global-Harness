# Política de pruebas y certificación
Versión del archivo: 0.7.0 | Última modificación: 2026-11-25

## Estrategia
- T0 estática: esquema, YAML/JSONC, nombres, metadatos, referencias, licencias y manifiesto.
- T1 unitarias/contrato: tareas, transiciones, DAG, validación, deduplicación, MCP, scripts y fallos.
- T2 runtime real Desktop: descubrimiento, Code, permisos efectivos, invocación, overlap, Swarm, retorno, cancelación, reanudación y scope de archivos.
- T3 evals skills: routing positivo/negativo/ambiguo, baseline vs candidato, evidencia y fallos. Mantener fixtures comparables y repetir casos no deterministas cuando coste lo permita.
- T4 integración: proyecto web, ERP/local-first, desktop si procede, pruebas de integración y revisión independiente.
- T5 distribución: instalación limpia/repetida, actualización, configuración ajena, fallo parcial, rollback, desinstalación, rutas con espacios y Unicode, enlaces/junctions y sin red cuando proceda.
## Criterios
PASS solo con comando/resultado o evidencia observable en runtime, versión y commit; FAIL, BLOCKED, NOT_RUN explícitos. Un retorno de tool no certifica implementación. Pruebas enfocadas al delta y dependencias; sustituir pruebas redundantes tras demostrar equivalencia, conservar regresiones distintas y seguridad. No repetir toda la suite para todo cambio; ejecutar suite crítica y e2e al liberar. No acumular capturas ni logs con secretos.
## Métricas
Tiempo total, trabajo simultáneo observado (intervalos solapados), llamadas, reintentos, conflictos, criterios satisfechos, regresiones y uso/coste solo si proveedor expone dato válido. Baseline directa vs delegada en tareas equivalentes. No prometer aceleración porcentual antes de medir; bloquear release ante fallo crítico, permisos fuera de alcance, pérdida de datos, instalación no reversible o capacidades centrales sin certificar.

## Casos obligatorios derivados del código
- T2: versión/hash de CLI empaquetado frente a PATH; global vs perfil Desktop; marcador de instrucción efectivo en sesión nueva, shadowing, configuración de checkout principal, duplicados de skills/agentes.
- T2: Task foreground, dos background con solapamiento real y notificación al padre, task_id propio vs ajeno, depth 1 y nesting solo si habilitado; no confundir estado de tool con fin de hijo. Board incremental, alcance por raíz y ausencia de confirmación de lectura.
- T2: permisos por agente y sesión, denies heredados, MCP invocable y negado, estado de sandbox efectivo; no inferir confinamiento de worktree. Usar fixture inocuo, no probar fuera del alcance real autorizado.
- T2: error/cancelación, compactación, reanudación y reinicio separados; no equiparar persistencia de historial a recuperación de tarea activa.
- T3/T4: selección nativa de modelo, detección de skill, Team Learning sin plugin primero, aislamiento multi-root de observaciones.
- T5: proteger perfil administrado y sidecar, configuración ajena, divergencias de versión del host y recertificación. No exponer credenciales.
La referencia estática no acredita PASS de ningún caso.

## Comparación de resiliencia por modelo (F12)
Usar mismos fixtures, contratos, límites de herramientas y criterios de aceptación; registrar modelo/proveedor cuando observable, variante, contexto, operaciones correctas, fallos, reintentos, latencia, coste observable y recuperación. Seleccionar al menos dos modelos representativos autorizados (gratuito y de pago/suscripción si disponibles) sin prometer equivalencia. No ampliar coste sin autorización. Una prueba no ejecutada queda NOT_RUN/BLOCKED, no PASS. Comparar con baseline sin Harness cuando sea viable y proporcional. Revisar divergencias, adaptar granularidad/contexto y repetir solo caso afectado; no bajar criterios de seguridad/calidad ni confundir evaluación de salida con introspección del modelo.

## Núcleo F04
[Matriz focalizada del núcleo](F04-NUCLEO.md): carga y comportamiento del candidato completo; casos nuevos de decisión y aceptación, sin duplicar PoC F03.

## Equipo F05
[Matriz F05](F05-EQUIPO.md): descubrimiento, selección de roles, herramientas y aceptación por rol; recuperar comprobación pendiente de coordinación en F07 sin duplicar F03/F04.

## Operación evolutiva y selección de pruebas (F05.2-R)
T0–T5 clasifican capacidades, no una secuencia obligatoria. Para cada cambio:
1. Identificar criterio, delta semántico, consumidores, invariantes y riesgo. Buscar prueba existente y evidencia vigente; no crear otro script por cambio.
2. Ejecutar la comprobación más barata suficiente: parser/lint/tipos para garantías estáticas; unidad/contrato para lógica; integración/runtime para fronteras reales; E2E/distribución solo donde la garantía lo requiere.
3. Seleccionar caso/archivo/dependencias con el runner del proyecto. Fail-fast para diagnóstico, pero no declara suite completa; ampliar al conjunto afectado tras corrección. Configuración común, lockfile, contratos transversales, selección incierta o release exigen ampliar según impacto y ejecutar puertas críticas.
4. Mantener un dueño y prueba canónica por garantía; parametrizar casos equivalentes. Una prueba de regresión nueva debe cubrir un fallo distinto; red/green en fixture seguro si viable, sin revertir trabajo ajeno. Eliminar/sustituir solo con equivalencia de garantías demostrada o retiro aprobado de funcionalidad; preservar negativos, seguridad y regresiones distintas. No reducir aserciones para ocultar fallos. Constructor mantiene pruebas; Veritas evalúa independientemente.
5. Reutilizar evidencia con criterio, revisión del objeto/dependencias, herramienta/configuración, fixture y entorno material vigentes (o delta demostrado irrelevante). Conservar referencia; invalidar solo lo afectado. No implementar caché/orquestador propio por defecto. Reintentos acotados con hipótesis, registrar flaky y no convertirlo en PASS. Cero selección, skips/xfail obligatorios o timeout no certifican.
6. Reporte mínimo: criterio/estado, revisión, comando/runner y versión, alcance y casos ejecutados/omitidos, código de salida, evidencia o referencia reutilizada, tiempo y bloqueo. No almacenar logs completos/secretos ni generar reportes por cada intento; conservar evidencia suficiente de fallos y cambios. Paralelismo solo con aislamiento de fixtures y recursos, sin escrituras compartidas.

## Motores candidatos: reutilizar antes de instalar
Investigación documental selectiva 2026-11-24, sin benchmark local, instalación ni auditoría de licencia completa. Herramientas no intercambiables; comprobar versión, licencia, soporte de host y permisos antes de adopción. Los comandos son ejemplos de selección, no recetas ejecutadas ni dependencias globales.
| Ecosistema | Primera opción si ya disponible | Alternativa condicionada / límites |
|---|---|---|
| PowerShell del Harness | Parser nativo [ParseFile](https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.language.parser.parsefile), sin ejecutar script; pwsh -NoProfile -File con modo de laboratorio autorizado para conducta | [PSScriptAnalyzer](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview?view=ps-modules) estática, [Pester](https://pester.dev/docs/usage/configuration) funcional/mock/etiquetas y reporte; no agregar ambos hasta justificar brecha. Pester no reemplaza pruebas Desktop reales. |
| Bash | bash -n para sintaxis, ejecución autorizada del script | [ShellCheck](https://github.com/koalaman/shellcheck) estática, [Bats](https://bats-core.readthedocs.io/en/stable/usage.html) prueba filtrada de CLI. No usar Bash para verificar sintaxis PowerShell. |
| JS/TS | Runner declarado y lockfile (p. ej. [node --test](https://nodejs.org/api/test.html) si apropiado) | [Vitest](https://vitest.dev/guide/cli.html) para ecosistema compatible y selección changed/related según versión; [Bun test](https://bun.sh/docs/test) solo si equivalencia con runtime objetivo demostrada. No cambiar Jest existente por promesa de velocidad. |
| Python | unittest si basta o [pytest](https://docs.pytest.org/en/stable/reference/reference.html) existente (filtros, last-failed) | [Ruff](https://docs.astral.sh/ruff/) lint/format check, [uv](https://docs.astral.sh/uv/guides/projects/) entorno/ejecución bloqueada según lockfile; uv puede sincronizar/instalar dependencias: no ejecutar sin revisar efectos/autorización. Ruff no es runner. |
| Rust / Tauri solicitado | cargo test con filtro, cargo check si pertinente | [cargo-nextest](https://nexte.st/docs/running/) selección/paralelismo cuando compile/runtime equivalentes; mantener cargo test --doc para doctests no cubiertos por nextest. No imponer Tauri. |
| Web/UI | Prueba de componente/contrato existente | [Playwright](https://playwright.dev/docs/ci) E2E y selección preliminar only-changed, workers según aislamiento; selección heurística no sustituye suite pertinente ni prueba accesibilidad completa. |
| Medición / ejecución de comandos | Measure-Command, reloj monotónico, scripts/package scripts existentes | [Hyperfine](https://github.com/sharkdp/hyperfine) benchmark CLI repetido con warmups; [just](https://just.systems/man/en/) command runner solo si hay fricción real. No son validadores de comportamiento ni requieren instalación global. |

Adopción: Forja inventaría versiones/capacidades locales y propone dependencia solo ante brecha; Faro confirma fuentes y compatibilidad; Veritas compara y Code decide. Primero ejecutar parser/validación focalizada y un caso de comportamiento existente sobre fixture; F05 runtime requiere Kilo real. No fijar ganadores por publicidad. Para candidatos, medir mismos criterios y casos (incluidos fallos conocidos), mismo host y revisión, caché fría/caliente por separado, compilación/preparación/ejecución total, al menos varias repeticiones si coste permite, mediana y dispersión, estabilidad/omisiones, recursos si observables, dependencias y mantenimiento. Cualquier pérdida de cobertura/compatibilidad descarta reemplazo; si no hay medición suficiente, NOT_RUN. No crear nuevos runners, servicios, suites duplicadas ni instalar herramientas en esta ronda.

## Skills F06
[Matriz de evaluación F06](F06-SKILLS.md): descubrimiento, activación positiva/negativa y contraste con/sin skill; reutilizar pruebas existentes, mantener regresión de dependencias F05.
