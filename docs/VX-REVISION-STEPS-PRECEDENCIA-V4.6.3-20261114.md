# VX Evolution V4.6.3 — Hallazgos sobre steps y precedencia (revisión manual)

**Registro:** 2026-11-14 · **Ámbito:** únicamente HOME global del usuario Windows, Kilo Code · **Fuente local:** tablas resumidas aportadas por el operador desde `vx_organizational_audit.py --json`. **No se inspeccionaron prompts, credenciales, contenido de Kilo JSONC ni logs.** Código de agentes y configuración activos sin cambios.

## Hechos observados

- Git local actualizado en `main` al commit documental `5bc46174e68323438e26bb092c5eee600ef3e531`, rama remota `work/v4-6-3-cierre-local-auditoria` eliminada, `origin/main` restante.
- Las once coincidencias de nombre entre JSONC y Markdown son: `architect`, `code-reviewer`, `code-simplifier`, `code-skeptic`, `codebase-memory`, `codebase-memory-auditor`, `codebase-memory-scout`, `data`, `docs-specialist`, `frontend-specialist` y `test-engineer`.
- Para las once coincidencias, `different_declared_fields=[]` y `effective_precedence=NO_VERIFICADO`. El comparador revisa **solo metadatos explícitos compartidos**: `mode`, `steps` y reglas sencillas `permission.edit/bash/task` cuando existen en ambas. Ausencia de diferencias **no** implica mismo prompt, mismos permisos efectivos, ni carga confirmada del runtime.
- En el **top 10** por `configured_steps` obtenido por el operador, los diez tienen `10 000 000`, todos desde `kilo-agent-jsonc`:

| Agente | steps declarados |
| --- | ---: |
| architect | 10 000 000 |
| plan | 10 000 000 |
| implementador-vecidya | 10 000 000 |
| general | 10 000 000 |
| frontend-specialist | 10 000 000 |
| explore | 10 000 000 |
| docs-specialist | 10 000 000 |
| debug | 10 000 000 |
| qa-vecidya | 10 000 000 |
| data | 10 000 000 |

- El inventario original informó **19 definiciones** con `steps > 400`, pero la tabla proporcionada solo mostró las diez primeras. **No atribuir 10 000 000 a las otras nueve sin inspeccionar su valor.** Una definición por fuente no es un agente único ni un consumo medido.

## Interpretación basada en documentación de Kilo

La referencia oficial [Kilo Code: Custom Modes](https://kilo.ai/docs/customize/custom-modes) describe `steps` como el **máximo de iteraciones del agente** (rondas de llamadas a herramientas) antes de obligar a una respuesta de texto. Como límite de seguridad operativo, diez millones de iteraciones es extraordinariamente permisivo; ello **no demuestra** que alguna sesión alcanzase el límite ni que exista consumo excesivo.

La misma documentación describe la **fusión de propiedades** de configuraciones, con precedencia documentada entre configuración global JSONC, configuración de proyecto, archivos de directorio Markdown y variables de entorno. Esta es una **regla documentada** y no una comprobación del **Kilo instalado ni del contexto específico de una sesión**. No declarar prioridad efectiva de un agente o subagente sin observar el runtime.

### Puntos de revisión humana (sin cambios)

1. Identificar las nueve entradas restantes de `AGENT_STEPS_REVIEW` y cuáles son límites únicos versus solapamientos de nombre. Revisar valores de `mode` y permisos declarados, sin mostrar prompts o reglas complejas.
2. Confirmar en la interfaz de Kilo qué modo y fuente se usa de verdad para uno o dos agentes representativos; evitar mezclar configuraciones del proyecto abierto con el HOME global.
3. Proponer, **no aplicar**, límites finitos de iteraciones adaptados a cada tipo de trabajo, acompañados de casos de control, medición de tasa de terminación y recuperación cuando se alcanza el límite. Ninguna cifra nueva se aprueba por silencio.
4. Confirmar que los seis agentes que el instalador señaló con `edit` o `bash` en `allow` son **declaraciones** y no permisos operativos ni acciones ejecutadas. Revisarlos separadamente y sin copiar credenciales.
5. Mantener `competence=NO_MEDIDO`, procedencia de delegaciones `NO_VERIFICADO`, y las reuniones automáticas y scheduler **OFF**.

## Próxima consulta local recomendada

El operador puede ejecutar desde PowerShell 7, con `vx_organizational_audit.py` ya instalado, este comando de solo lectura que **no guarda archivos**:

```powershell
$org = Join-Path $HOME '.config/kilo/harness/scripts/vx_organizational_audit.py'
$report = python -I $org --json | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) { throw 'Auditoria local fallo' }
$report.findings |
  Where-Object { $_.kind -eq 'AGENT_STEPS_REVIEW' } |
  Sort-Object -Property @{Expression='configured_steps';Descending=$true}, @{Expression='component';Descending=$false} |
  Select-Object component,source_context,configured_steps |
  Format-Table -AutoSize
```

El objetivo es recopilar **19 filas**, no solo las diez primeras.

Esta observación es un hito de investigación de V4.6.3 y **no** crea una versión nueva, cambios de permisos, agentes, skill, modelos, MCP, SQLite o programador.
