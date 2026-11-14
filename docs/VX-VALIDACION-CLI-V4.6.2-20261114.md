# VX Evolution V4.6.2 — Cierre de validación CLI en Windows y puerta de evaluación

**Fecha de evidencia:** 2026-11-14 · **Ámbito:** una PC Windows, Kilo Code global · **Tipo de evidencia:** salida de consola aportada por el operador; no contiene secretos ni datos de proyectos.

## Evidencia ejecutada

El operador invocó manualmente en PowerShell 7:

```powershell
$trial = Join-Path $HOME '.config/kilo/harness/scripts/vx_competency_trials.py'
python -I $trial
python -I $trial --list-cases
```

Ambos comandos finalizaron sin errores según la salida suministrada. El CLI informó:

| Campo | Resultado |
| --- | ---: |
| `planned_cases` | 5 |
| `targets_observed` | 5 |
| `baseline_declared_matches` | 0 |
| `candidate_declared_matches` | 0 |
| `possible_regressions_to_review` | 0 |
| `possible_improvements_to_review` | 0 |
| `real_world_performance` | `NO_MEDIDO` |
| `training_effectiveness` | `NO_VERIFICADO` |
| Motor | solo lectura; sin ejecución de agentes ni escritura SQLite |

`--list-cases` devolvió `vx-kilo-trial-catalog/1`, con cinco casos: `v462-review-unsafe`, `v462-review-guarded`, `v462-precedence`, `v462-skill-observer` y `v462-regression-gap`. Se enlazaron con tres IDs de prueba declarados: `vx-078e9b1c15494653` (tres casos de `vx-inspector`), `vx-c776f60a3c790816` (skill `vx-evolution-core`) y `vx-aa0021484073a921` (`vx-test-analyst`).

**No significa cinco tests de calidad aprobados.** Son cinco escenarios disponibles y cinco destinos presentes en la matriz, sin respuestas.

## Bloqueo de interacción en Kilo Code

En la sesión de Kilo, la política de herramientas bloqueó una invocación de PowerShell incluso después de la solicitud del usuario. El componente global `/vx-ensayos` fue localizado, pero **no hay evidencia de que Kilo ejecutase el CLI desde la propia extensión**, ni de que activase alguno de los especialistas. La ejecución directa desde PowerShell demuestra funcionamiento de CLI local, no permiso de terminal en Kilo.

**Acción recomendada:** no desactivar políticas de herramientas, ampliar AutoApprove, conceder permisos `bash`, ni usar PowerShell como vía alternativa para ejecutar herramientas desde Kilo. El operador puede verificar los fixtures desde su terminal local y realizar una prueba de razonamiento por chat, con consentimiento expreso, sin herramientas ni acceso al proyecto.

## Puerta de primera prueba manual (pendiente, no ejecutada)

1. En una sesión nueva de Kilo, escoger `vx-inspector` si se ofrece como modo. Si solo está disponible como subagente, pedir al coordinador una delegación de **solo texto** mediante el flujo soportado; si la política la impide, anotar `BLOQUEADO_POR_POLITICA` sin alterar permisos.
2. Presentar **un caso por turno**, sin respuesta esperada, sin mostrar código fuente de los fixtures ni `expected_decision`/`expected_reason`. Empezar por `v462-review-unsafe`.
3. Solicitar identificador del caso, una opción enumerada de `decision` y otra de `reason`, más justificación breve. No ejecutar terminal, Git, MCP, scripts o modelos auxiliares.
4. Revisar el transcript con el operador para determinar si respondió el especialista realmente, qué restricciones estuvieron activas y si se conocen fuentes de contaminación; registrar resultado como `DECLARADO_NO_VERIFICADO` hasta contar con evidencia reproducible y evaluación independiente.
5. Antes de comparar antes/después, diseñar casos nuevos ciegos y equivalentes; los cinco fixtures actuales son **públicos y no ciegos**.

### Primera tarea sintética (sin respuesta)

`case_id = v462-review-unsafe`; agente objetivo `vx-inspector`; capacidad declarada `code-review`.

> Diff sintético: un endpoint eliminó la comprobación de autorización antes de editar el recurso de otra persona. ¿Se exige corregir?

Permitir una decisión entre `FLAG_RISK`, `NO_RISK`, `NO_VERIFIED_PRECEDENCE`, `NO_INFER`, `NEEDS_NEGATIVE_TEST`; y una razón entre `AUTH_GUARD_REMOVED`, `GUARD_PRESERVED`, `RUNTIME_NOT_CHECKED`, `OBSERVER_NOT_QUALITY`, `MISSING_NEGATIVE_CASE`. **No** indicar la pareja correcta.

## Estado y cierre

- **Código y CI:** V4.6.2 integrada en `main`, 27 pruebas unitarias Windows y rollback PASS.
- **CLI del Windows del usuario:** validado para resumen y catálogo.
- **Kilo por herramienta:** bloqueado por política, no ejecutado.
- **Especialistas y skills:** `NO_MEDIDO` / `NO_ASIGNADO`.
- **Versiones siguientes:** V4.6.3 y superiores pendientes; no corresponde afirmar capacitación, promoción ni reestructuración.
- **Automatización:** semanal y reunión conjunta mensual mantienen scheduler y notificaciones OFF.
- **Ramas:** actualización documental en rama temporal y merge bajo el procedimiento aprobado; limpiar la rama propia después de verificar integración.
