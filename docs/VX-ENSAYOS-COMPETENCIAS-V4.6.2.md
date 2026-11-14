# VX Evolution V4.6.2 — Ensayos sintéticos reproducibles y capacitación candidata

**Edición:** 2026-11-14 · **Ámbito:** un único Windows, Kilo Code global, HOME local. **Estado:** implementación y pruebas en revisión. Scheduler, notificaciones, promociones y publicaciones automáticas: **OFF**.

## Punto de partida verificado por el operador

El 2026-11-14 se ejecutaron en el Windows del usuario el instalador V4.6.1 (`Simular`, `Aplicar`, `Verificar`) y los CLI V4.6.0/4.6.1. **El CLI fue validado localmente; todavía no consta prueba interactiva en Kilo después de `/reload`.**

| Métrica real del CLI global | Resultado |
| --- | ---: |
| Agentes: fuentes / nombres únicos | 39 / 28 |
| Skills: fuentes / nombres únicos | 40 / 40 |
| Agentes JSONC/Markdown superpuestos | 11 |
| Agentes con `steps > 400` | 19 |
| Filas de matriz V4.6.1 | 76 |
| Capacidades declaradas desde el router | 15 |
| Filas sin evidencia real | 76 |
| Rendimiento/seniority | `NO_MEDIDO` / `NO_ASIGNADO` |

La instalación conservó `kilo.jsonc`, AutoApprove, permisos, MCP, los datos SQLite y el scheduler; el operador eliminó la rama remota temporal V4.6.1 y comprobó solo `origin/main`. Estas cifras no describen fuentes efectivas en el runtime ni calidad de ninguna skill.

## Objetivo deliberadamente acotado

`scripts/vx_competency_trials.py` construye **cinco escenarios sintéticos, públicos y no ciegos**, enlazados a la matriz local de V4.6.1:

| ID | Objetivo declarado | Categoría | Qué busca comprobar en un ensayo manual |
| --- | --- | --- | --- |
| `v462-review-unsafe` | `vx-inspector / code-review` | Capacidad existente | Detectar eliminación de protección de autorización |
| `v462-review-guarded` | `vx-inspector / code-review` | Control de falsos positivos | No inventar un problema cuando se conserva la protección |
| `v462-precedence` | `vx-inspector / code-review` | Brecha de evidencia | No afirmar prioridad JSONC/Markdown sin prueba runtime |
| `v462-skill-observer` | `vx-evolution-core` (skill global) | Skill existente | No convertir un contador `session_error` en nota de calidad |
| `v462-regression-gap` | `vx-test-analyst / regression-analysis` | Posible necesidad de capacitación | Identificar falta de prueba negativa, sin declarar incompetencia |

**Importante:** Estos ensayos contienen respuestas esperadas visibles en el código (no son evaluación ciega). El motor no invoca Kilo ni agentes: únicamente enseña preguntas y contrasta respuestas enumeradas de dos archivos locales *declarados*. No se puede derivar un nivel profesional ni una mejora real de este ensayo sin ejecución independiente y revisión humana posterior.

## Uso manual desde PowerShell 7

Después de integrar, instalar y verificar la versión, ejecutar:

```powershell
$trial = Join-Path $HOME '.config/kilo/harness/scripts/vx_competency_trials.py'
python -I $trial
python -I $trial --list-cases    # escenarios sintéticos y respuestas permitidas
python -I $trial --json          # informe sin entrada (SIN_RESPUESTA)
```

El comando global Kilo es `/vx-ensayos`. Para una futura prueba en Kilo, el operador seleccionará voluntariamente el agente/skill, presentará **solo el escenario sintético** y recogerá una respuesta con `decision` y `reason` enumeradas; no enviar el par esperado, datos de cliente, código de proyectos o secretos.

Para comparar declaración `antes/después`, crear **manualmente** dentro de HOME dos archivos JSON sin comentarios, sin rutas ni texto libre. Ejemplo de formato (los valores indicados son ilustrativos, no ejecución real):

```json
{
  "schema": "vx-kilo-trial-responses/1",
  "cases": [
    {
      "case_id": "v462-review-unsafe",
      "decision": "FLAG_RISK",
      "reason": "AUTH_GUARD_REMOVED"
    }
  ]
}
```

```powershell
python -I $trial --baseline-file (Join-Path $HOME 'vx-trials-before.json') --candidate-file (Join-Path $HOME 'vx-trials-after.json') --json
```

Archivo máximo **32 KiB**; hasta 32 respuestas; casos, decisiones y razones estrictamente enumerados; sin campos adicionales, rutas fuera de HOME ni symlinks. El comparador es **solo lectura**. Si no se ha probado una etapa, omitir el argumento de esa etapa; **no fabricar datos de ensayo**.

### Semántica de resultados

- `SIN_RESPUESTA`: ningún archivo aportó una respuesta para ese caso.
- `COMPONENTE_NO_OBSERVADO`: objetivo no encontrado en la matriz del HOME; no prueba que sea inexistente en tiempo de ejecución.
- `COINCIDE_FIXTURE_DECLARADO` / `DIFIERE_FIXTURE_DECLARADO`: comparación de valores de un JSON suministrado, **no resultado de ejecución autenticado**.
- `possible_improvements_to_review` / `possible_regressions_to_review`: cambios en coincidencia de fixtures declarados; NO prueba de efectividad de capacitación.
- `NO_MEDIDO`, `NO_ASIGNADO`, `NO_VERIFICADO` continúan siendo las conclusiones de rendimiento, competencia y formación.
- Costes/tokens/latencia quedan `NO_MEDIDO`; `review_source` independiente no se certifica a partir de un archivo.

## Capacitación candidata sin cambios activos

**Hipótesis H1 — falsos positivos en revisión:** si el especialista declara riesgo de autorización en el caso protegido, revisar primero instrucciones y pruebas negativas de la skill existente. No editar agente ni añadir skill basándose en un único ensayo.

**Hipótesis H2 — confundir configuración con runtime:** si se afirma precedencia de JSONC/Markdown sin verificación en Kilo, priorizar formación en lectura de metadatos frente a suposición de comportamiento. En caso de duda, mantener `NO_VERIFICADO`.

**Hipótesis H3 — pruebas de regresión incompletas:** si no se detecta la ausencia de un caso negativo, diseñar una capacitación candidata en cobertura positiva/negativa y repetir manualmente con escenarios equivalentes nuevos, idealmente ciegos y revisados por otra persona.

Para todas las hipótesis: definir línea base real, prueba repetible con criterio anterior/posterior, revisión de efectos adversos, evaluador externo, costes solo si se miden, consentimiento para cualquier archivo o registro. La generación local del reporte NO crea propuestas, cambios de skills, nuevas jerarquías ni contratos de seniority.

## Validación y próximos hitos

1. Unit tests de clasificación, regresiones aparentes, control de falsos positivos, campos prohibidos, rutas fuera de HOME, symlinks y no escritura.
2. CI Windows: instalación/rollback sobre un HOME aislado, ejecución sin respuestas, auditorías V4.6.0 y V4.6.1 coherentes, base SQLite inexistente antes y después.
3. Validación en Windows del usuario: ejecución CLI y **prueba opcional explícita en Kilo** después de `/reload`.
4. Evaluación real futura con casos ciegos, registro de ejecución verificable y revisión independiente; **V4.6.3 no podrá considerar estos fixtures como ascensos demostrados**.

No ejecutar autónomamente un modelo, no abrir el proyecto activo, no programar tareas Windows, no crear backups ni archivos de evidencias sin orden expresa. Un solo escritor máximo, hasta tres lectores. Mantener una sola rama temporal y `main`.
