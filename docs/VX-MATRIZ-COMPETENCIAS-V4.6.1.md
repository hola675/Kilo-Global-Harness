# VX Evolution V4.6.1 — Matriz de competencias y evidencias Kilo

**Versión:** 4.6.1 · **Fecha:** 2026-11-14 · **Alcance:** una sola PC Windows, exclusivamente Kilo Code, HOME global. **Estado:** CI Windows PASS (20 pruebas y smoke/rollback); CLI audit/matriz validado en Windows del usuario 14-11-2026; ejecución interactiva en Kilo después de /reload pendiente. No activa automatizaciones.

## Contrato de solo lectura

`scripts/vx_competency_matrix.py` reutiliza la línea base de `vx_capability_audit.py` V4.6.0 y genera `vx-kilo-competency-matrix/1`. No ejecuta agentes, prompts, modelos, MCP, evaluaciones de calidad, tests de tareas ni hooks. No abre ni escribe SQLite; no altera permisos, jerarquías, skills, modelos, configuraciones o scheduler.

La matriz transforma cada `agent + router_capability` declarada en una fila; los agentes sin declaración reciben `SIN_DATOS` y **no se les inventa competencia**. Cada nombre de skill encontrado representa una presencia de fuente, no una habilidad demostrada. Una skill con varias fuentes se mantiene como una única fila de nombre, sin declarar precedencia efectiva; para analizar fuentes conservar el informe V4.6.0. Los IDs `test_id` son estables, derivados de tipo, nombre y capacidad, y **no significan que se haya ejecutado prueba alguna**.

El contrato dispone de `baseline_status`, `test_status`, `assessment_status`, `evidence`, `score = NO_MEDIDO`, `competence_level = NO_ASIGNADO`, `effective_runtime_verified = false`. No existe graduación ni promoción automática.

## Uso manual en PowerShell 7 (después de instalar desde main)

```powershell
$matriz = Join-Path $HOME '.config/kilo/harness/scripts/vx_competency_matrix.py'
python -I $matriz
# Inspección estructurada LOCAL; no publicar el JSON íntegro sin revisión:
python -I $matriz --json
```

El comando Kilo correspondiente es `/vx-matriz`. La ejecución inicial debe devolver todos los componentes con evidencia ausente. **V4.6.0 y V4.6.1 ya se ejecutaron mediante CLI en el Windows real:** 28 agentes, 40 skills, 76 filas y 0 evidencias. Falta validar invocación interactiva del comando en Kilo tras /reload.

### Evidencias opcionales declaradas (nunca pruebas verificadas)

La V4.6.1 admite exclusivamente **un archivo JSON existente dentro de HOME**, tamaño máximo 128 KiB y hasta 200 casos. No crea ese archivo. El operador obtiene `test_id` y `component` de su matriz local, y puede preparar manualmente:

```json
{
  "schema": "vx-kilo-competency-evidence/1",
  "cases": [
    {
      "case_id": "revisar-pr-001",
      "test_id": "vx-ID-EXTRAIDO-DE-LA-MATRIZ",
      "component_type": "agent",
      "component": "vx-reader",
      "capability": "code-review",
      "outcome": "PASS",
      "difficulty": "intermediate",
      "review_source": "other",
      "reproducible": true
    }
  ]
}
```

**Ejemplo ilustrativo, no un resultado de producción.** El ID de ejemplo debe sustituirse por un ID real. Opcional `artifact_digest` exige SHA-256 hexadecimal y no demuestra por sí solo que el artefacto sea correcto. No incluir prompts, outputs, secretos, datos de clientes ni rutas de proyectos.

```powershell
python -I $matriz --evidence-file (Join-Path $HOME 'vx-evidence.json') --json
```

Un `PASS`, `FAIL` o `BLOCKED` suministrado en un archivo se cuenta solo como **resultado declarado**: `EVIDENCIA_DECLARADA_NO_VERIFICADA`. Incluso `review_source = other` es una afirmación suministrada, NO prueba de independencia. `test_id` desconocidos o referencias que no coinciden se contabilizan sin inferir relaciones por parecido. `case_id` repetidos y esquemas inválidos se rechazan; no se imprime contenido confidencial de errores ni archivos privados.

## Rúbrica propuesta: NUNCA aplicada automáticamente

| Nivel candidato | Condición preliminar para una futura revisión humana |
| --- | --- |
| Aprendiz | Reproduce tareas básicas con instrucciones acotadas, criterios de aceptación y revisión externa. |
| Especialista | Resuelve distintos escenarios intermedios de la misma competencia; tests positivos y negativos repetibles. |
| Senior | Evidencia avanzada con prevención de regresiones, diagnóstico de fallos, alternativas y evaluación independiente. |
| Líder | Acredita coordinación, calidad de delegación, gestión de riesgos y revisión cruzada, además de competencia técnica. |
| Principal | Acredita resultados expertos, complejidad transversal, diseño duradero, transferencia de conocimientos y revisión externa múltiple. |

Estas categorías son **un diseño para futuras evaluaciones**. V4.6.1 no asigna niveles, umbrales cuantitativos, puntuaciones, liderazgos ni permisos; un único test positivo jamás concede un nivel. V4.6.2 definirá fixtures reales con entradas/salidas, casos negativos, dificultad verificable y ejecución reproducible. V4.6.3 propondrá ajustes organizativos solo después de esos resultados y aprobación explícita.

## Criterios de aceptación y límites

- 20 pruebas unitarias de matriz, evidencia, seguridad y falsos positivos; CI en Windows y prueba de instalación/rollback.
- Sin diffs en `kilo.jsonc`, agentes, skills, permisos, MCP, modelos, base SQLite y política de reuniones.
- Informes estables y deterministas. No serializa textos de evidencias ni rutas privadas.
- `NO_MEDIDO` y `NO_ASIGNADO` permanecen en todos los componentes aunque se suministren PASS de terceros.
- El informe real no debe compartirse públicamente sin revisar nombres de componentes.
- Un solo ordenador Windows, sin sincronización entre equipos, sin tareas residentes o programadas.

**Continuación:** [V4.6.2 — ensayos sintéticos manuales](VX-ENSAYOS-COMPETENCIAS-V4.6.2.md); aún no equivalen a pruebas reales de agentes, que requerirán ejecución y evaluación independiente. Sin ascensos ni autopublicación.
