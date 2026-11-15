# VX Evolution V4.6.3 — Auditoría organizativa declarativa y revisión de procedencia

**Edición:** 2026-11-14 · **Alcance:** un solo equipo Windows, Kilo Code global en HOME · **Estado:** 26 pruebas unitarias y smoke/rollback CI Windows PASS; instalador y CLI en el PC del usuario PASS (2026-11-14); evaluación del runtime y procedencia de subagentes pendientes. [Acta de validación](VX-VALIDACION-LOCAL-V4.6.3-20261114.md). **No modifica runtime ni activa scheduler**.

## Punto de partida confirmado

La V4.6.2 finalizó con cinco respuestas conversacionales que coincidieron con los fixtures sintéticos **públicos y no ciegos**. La identidad efectiva de los subagentes y el uso de skills permanecen **NO_VERIFICADOS**; los identificadores de sesión transmitidos por el usuario no sustituyen trazas originales ni se publican. [Informe de cierre V4.6.2](VX-CIERRE-BATERIA-V4.6.2-20261114.md).

El auditor V4.6.0 del Windows real informó 39 definiciones de agente en 28 nombres, 40 skills de nombre único, **11 solapamientos de nombre JSONC/Markdown** y **19 entradas steps mayores de 400**. Son conteos de metadatos; no son 11 fallos ni 19 riesgos demostrados. La precedencia de Kilo sigue `NO_VERIFICADO`.

## Herramienta V4.6.3

`scripts/vx_organizational_audit.py` consume exclusivamente la línea base V4.6.0 mediante la interfaz de V4.6.1, para generar el contrato `vx-kilo-organizational-audit/1`. No ejecuta agentes, modelos, MCP, Git ni pruebas de Kilo; no abre SQLite ni guarda resultados. Los datos utilizados son nombres seguros y metadatos de fuente sin prompts, credenciales, rutas del proyecto ni IDs de sesión.

| Categoría de hallazgo | Qué significa | Qué NO demuestra |
| --- | --- | --- |
| `AGENT_SOURCE_OVERLAP` | Un mismo nombre en JSONC y Markdown; posibles diferencias declaradas en mode, steps y permisos simples | Qué definición tiene prioridad en el runtime, colisión funcional, error de autorización |
| `AGENT_STEPS_REVIEW` | Valor declarado steps superior al umbral elegido (400 por defecto) | Riesgo, vulnerabilidad, coste, consumo o mala calidad |
| `SKILL_SOURCE_OVERLAP` | Nombre de skill presente en varias raíces globales | Qué copia se carga realmente |
| `PROFILE_SKILL_UNOBSERVED` | Skill de perfil no encontrada en rutas globales inspeccionadas | Que la skill esté ausente en todo Kilo |
| `ROUTER_AGENT_UNOBSERVED` | Agente declarado en router no observado en inventario | Que la delegación sea imposible o que el agente no exista |

Las diferencias explícitas identificadas se limitan a `mode`, `steps`, `permission.edit`, `permission.bash` y `permission.task`. La ausencia de diferencias **no** garantiza equivalencia semántica o igualdad de prompts; la extracción intencionalmente NO compara el contenido del prompt.

Todos los hallazgos reciben `finding_id` determinista y acción **manual sugerida**, sin prioridad calculada, sin calificación de rendimiento ni ejecución automática. El informe incluye `delegation_provenance_verified=false`, `effective_source_verified=false`, `competence=NO_MEDIDO`, `seniority=NO_ASIGNADO`, `organizational_change_authorized=false`.

## Operación manual en el Windows del usuario

Después de integrar la PR, actualizar `main`, simular/aplicar/verificar el instalador reversible sobre HOME y ejecutar desde PowerShell 7:

```powershell
$org = Join-Path $HOME '.config/kilo/harness/scripts/vx_organizational_audit.py'
python -I $org
# Informe estructurado para revisión LOCAL exclusivamente:
python -I $org --json
```

Comando Kilo: `/vx-organizacion`. Si la política bloquea PowerShell dentro de Kilo, **no ampliarla para realizar esta auditoría**: es válido ejecutar la herramienta desde PowerShell local como operador. Ver el resumen y revisar los datos antes de copiar cualquier informe; no subir el JSON completo del HOME a GitHub.

**Ejecutado localmente:** 11 hallazgos de `AGENT_SOURCE_OVERLAP`, 19 de `AGENT_STEPS_REVIEW` y **0 diferencias explícitas comparables**; skill repetidas, skills de perfil no observadas y router sin coincidencia = 0. Total **30** hallazgos para revisión, no 30 errores. Esta observación corresponde a una foto del equipo y puede cambiar con la configuración global.

## Cómo verificar procedencia de subagentes

La primera batería V4.6.2 registra respuestas **declaradas** de `Kilo`, `vx-inspector`, `vx-test-analyst`, y `vx-evolution-core`, pero no ha inspeccionado los metadatos de ejecución. V4.6.3 **no importa** IDs `ses_*`, mensajes, tokens, logs ni transcripciones. Para verificar una delegación concreta posteriormente:

1. Con permiso expreso, consultar únicamente la ficha de tarea de Kilo que el operador ya pueda ver y extraer un dato **mínimo**: agente ejecutor, modo subagente, resultado, estado de la tarea y evidencia de asignación.
2. Confirmar que el identificador del caso y el ejecutor coinciden con la delegación solicitada. Si faltan datos, dejar `NO_VERIFICADO`; una sesión completada no basta para identificar al ejecutor.
3. Comparar controles positivos y negativos con casos **nuevos y ciegos**, con un evaluador diferente. La ejecución por el modelo no se certifica simplemente por responder correctamente.
4. Mantener los informes de HOME privados; nunca guardar el ID de sesión íntegro, prompt, token o código del usuario en GitHub o SQLite.

**Una skill presente en disco tampoco equivale a invocación real de la skill.**

## Control de seguridad y gobernanza

- Sin lectura de datos de proyecto, prompts completos, códigos fuente, logs de Kilo, contratos, archivos de usuario no relacionados ni secretos.
- Sin cambios en agentes, skills, `kilo.jsonc`, permisos, modelos, MCP, AutoApprove, Observer, SQLite, backups ni scheduler.
- Ninguna herramienta de la V4.6.3 crea automáticamente propuestas `pending_review`, relaciones jerárquicas, ascensos, fusiones o retiros; los cinco fixtures V4.6.2 no justifican tales acciones.
- Las reuniones siguen manuales: lunes a las 09:00 horario local Windows; primer lunes del mes, una sola reunión con cierre mensual y agenda semanal.
- El registro global sigue con un máximo de un escritor; este auditor se limita a leer metadatos declarados.

## Plan de validación

1. 26 pruebas unitarias con entradas controladas: duplicidades, contadores, límites steps, incoherencias, nombres/rutas inválidas, no inferencia de autoría y salida sin datos sensibles.
2. CI Windows: instalador `Aplicar` sobre HOME aislado, verificación del comando y módulo V4.6.3, ejecución del informe, invariantes de solo lectura, `Verificar` y rollback.
3. Operador: `Simular`, `Aplicar`, `Verificar`, `python -I $org`, inspección del resumen. No afirmar validación local antes de recibir su salida.
4. Revisión humana de hallazgos, y solo después definir propuestas específicas basadas en evidencias, con pruebas de regresión, riesgos y aprobación explícita.

**Siguiente fase V4.6.3:** cierre de auditoría de metadatos y verificaciones manuales de procedencia cuando el usuario aporte evidencia suficiente; ningún despliegue organizativo por defecto.
