---
description: Crear matriz de competencias declaradas y evidencias locales de Kilo, sin ejecutar pruebas ni cambiar configuración
agent: plan
---

VX Matriz V4.6.1: $ARGUMENTS.

**Ámbito: únicamente Kilo Code, instalado globalmente en HOME de esta PC Windows.** Consulta primero `/vx-capacidades` como base V4.6.0. Ejecuta bajo solicitud explícita:

```powershell
$matriz = Join-Path $HOME '.config/kilo/harness/scripts/vx_competency_matrix.py'
python -I $matriz
# JSON detallado solo para revisión LOCAL:
python -I $matriz --json
```

Interpreta `DECLARADA_NO_PROBADA`, `PRESENCIA_NO_DEMUESTRA_COMPETENCIA`, `SIN_DATOS`, `NO_MEDIDO` y `NO_ASIGNADO` literalmente. La existencia de un `test_id` es un identificador de plan, no una prueba realizada. Aunque exista un fichero `--evidence-file` con PASS y `review_source=other`, es **declaración no verificada**: nunca calificar seniority, ascender, contratar, crear agentes, reordenar equipos o autopublicar. Para un plan de prueba reproducible, diferir a V4.6.2.

No escribir SQLite; no ejecutar Kilo CLI por cuenta propia, test de tareas, hooks, git, MCP o modelos; no modificar AutoApprove, prompts, permisos, fuentes, skills ni archivos del proyecto activo. No crear programador, reunión o notificaciones. Consultar `docs/VX-MATRIZ-COMPETENCIAS-V4.6.1.md`.
