# VECIDYA · Kilo Code Global Harness V4.2

**Versión del código:** 4.2.0 · **Instalador:** manifiesto 4.0.0 (rollback compatible con V3) · **Estado:** candidato a prueba funcional de equipos en Windows tras aprobar CI.

Harness de ingeniería autónoma para Kilo Code en VS Code/VSCodium. Se instala **exclusivamente en el perfil GLOBAL de Windows**. Los proyectos no reciben skills, agentes, reglas, comandos ni MCP locales. El código y los documentos propios de cada proyecto sí pueden desarrollarse normalmente.

## Principios

- **Global-only**: `~/.config/kilo/{AGENTS.md,agents/,commands/,rules/}` y `~/.kilo/skills/`.
- **AutoApprove conservado**: no cambia settings de VS Code ni permisos de agentes.
- **main permanente**: una rama temporal `work/*` por tarea no trivial, validación, PR/merge según protección GitHub y eliminación exclusiva de la rama propia después de verificar integración.
- **Sin reescritura de `kilo.jsonc`**: modelos, MCP, tokens, versiones y límites steps quedan intactos.
- **Reconcilicación V4.2 (solo diagnóstico)**: compara con metadatos seguros las fuentes JSONC y Markdown; no elimina agentes ni cambia sus permisos o pasos.
- **Verificación V4.1**: `/vx-revalidar` contrasta hallazgos antes de clasificarlos como fallos, preserva descartes y separa CI configurada de tests realmente ejecutados.
- **Equipos V4 con paralelismo estricto**: hasta tres subagentes de lectura, un escritor, revisión independiente. El selector no inicia agentes.
- **Instalación segura**: diagnóstico, simulación, backup, aplicación idempotente, verificación y restauración con comprobación de hashes.
- **Sin actualización silenciosa** de skills, MCP, extensiones ni modelos; el instalador no gestiona actualizaciones de Windows o VS Code.

## Instalación desde `D:\Proyectos\Kilo-Global-Harness`

Abre PowerShell 7, comprueba que el repositorio local corresponda al remoto correcto:

```powershell
Set-Location 'D:\Proyectos\Kilo-Global-Harness'
git remote -v
git status --short
```

Si es un directorio vacío y todavía no has clonado el proyecto:

```powershell
New-Item -ItemType Directory -Force 'D:\Proyectos' | Out-Null
git clone https://github.com/hola675/Kilo-Global-Harness.git 'D:\Proyectos\Kilo-Global-Harness'
Set-Location 'D:\Proyectos\Kilo-Global-Harness'
```

No uses `git reset --hard` en una carpeta que contenga trabajo local. Si ya existe el repositorio y está limpio, sincroniza de forma segura:

```powershell
git switch main
git pull --ff-only origin main
```

Después:

```powershell
$script = Join-Path (Get-Location) 'scripts\Instalar-Kilo-Global-Harness.ps1'
pwsh -NoProfile -File $script -Modo Diagnostico
pwsh -NoProfile -File $script -Modo Simular
pwsh -NoProfile -File $script -Modo Aplicar -PausarTaskObserver
pwsh -NoProfile -File $script -Modo Verificar
```

Si ya pausaste `task-observer`, la opción no realiza ningún nuevo movimiento. El respaldo se guarda en `~/.config/kilo-harness-backups/AAAAmmdd-HHMMSS` y **nunca debe subirse a GitHub**.

Finalmente, en Kilo ejecuta `/reload`, `/vx-harness-estado` y `/vx-equipo`. Antes de delegaciones automáticas, revisa la [guía operativa V4](docs/OPERACION-EQUIPOS-V4.md).

## Reversión

Utiliza la ruta de respaldo que imprimió el instalador:

```powershell
pwsh -NoProfile -File $script -Modo Restaurar -BackupFolder 'C:\Users\Admin\.config\kilo-harness-backups\AAAAMMDD-HHMMSS'
```

Por defecto, si un archivo administrado fue modificado **después de aplicar**, la restauración lo omite para evitar perder cambios. `-ForzarRestauracion` únicamente tras revisar esos cambios.

## Qué instala

| Origen del repositorio | Ubicación global en Windows | Resultado |
| --- | --- | --- |
| `rules/AGENTS-global-managed.md` | Sección marcada dentro de `~/.config/kilo/AGENTS.md` | Política corta y universal |
| `rules/vx-global-harness-v3.md` | `~/.config/kilo/rules/` | Manual ampliado de trabajo |
| `commands/vx-*.md` | `~/.config/kilo/commands/` | Workflows `/vx-*` |
| `agents/vx-*.md` | `~/.config/kilo/agents/` | Coordinador y revisor |
| `skills/vx-engineering-harness/SKILL.md` | `~/.kilo/skills/` | Orquestación bajo demanda |
| `registry/vx-agent-registry-v4.json` | `~/.config/kilo/harness/` | Registro de agentes y nueve perfiles |
| `scripts/{Seleccionar-Equipo-V4,Validar-Registro-V4}.ps1` | `~/.config/kilo/harness/scripts/` | Enrutamiento determinista y validación sin efectos |

Todos los destinos anteriores están bajo HOME. Si se ejecuta desde `D:\Proyectos`, **no escribe allí**; esa carpeta es exclusivamente la fuente versionada del instalador.

### Limitaciones deliberadas

- Ni el instalador ni el selector ejecutan subagentes, Git o MCP automáticamente: las tareas las realiza Kilo siguiendo sus permisos. No ejecuta automáticamente `git push`, `git merge` ni el borrado de ramas en tus repositorios; **define el comportamiento que Kilo debe seguir cuando realiza una tarea autorizada**. Si una protección del remoto bloquea una operación, no se elude.
- No cambia modelos ni fuerza un límite `steps` diferente. La auditoría detecta riesgos y el agente puede recomendar cambios posteriormente, con evidencia de compatibilidad.
- No instala ni repara servidores MCP automáticamente; distingue configuración de conectividad.
- Los agentes heredados definidos en `kilo.jsonc` y en Markdown no se eliminan ni modifican, porque pueden tener precedencia o permisos diferentes.
- La validación CI es un smoke test del instalador en Windows aislado. No valida conexión de los MCP del PC ni el comportamiento real de los modelos Kilo.

## Diagnostico de agentes y MCP (sin modificar configuracion)

```powershell
pwsh -NoProfile -File .\scripts\Auditar-Kilo-Global.ps1
pwsh -NoProfile -File .\scripts\Auditar-Kilo-Global.ps1 -Json
```

La salida nunca incluye secretos. Los agentes definidos en JSON y Markdown se **fusionan por precedencia**, no son necesariamente agentes duplicados en ejecucion; revisar campos efectivos antes de limpiar. El plugin declarado en opencode.json y tui.json puede atender a dos superficies distintas. Los limites `steps` elevados se informan pero no se cambian sin una revision del comportamiento de los agentes.

**ImageGen:** tres generaciones CLI con `codex-imagegen-mcp@0.2.3` confirmadas por el operador; las herramientas en Kilo requieren comprobacion separada. Usa `/vx-imagegen` para diagnosticar sin consumir cuota. Ver [validacion ImageGen](docs/IMAGEGEN-MCP.md).

## Investigación y diseño de la siguiente etapa V4

- [Catálogo contrastado de 44 fuentes de agentes/harnesses](docs/investigacion/HARNESSES-Y-AGENTES-2026-11-13.md).
- [Arquitectura de selección de agentes, paralelismo, gates y coste](docs/investigacion/ORQUESTACION-MULTIAGENTE-V4.md).
- [Registro estructurado de fuentes (solo candidatos)](inventory/harness-sources-2026-11-13.json).

**Esta documentación NO importa ni activa agentes externos.** El plan V4 conserva la configuración exclusivamente global, AutoApprove, MCP y modelos existentes. La implementación requiere adaptación selectiva y pruebas posteriores.

## Documentación

- [Auditoría actualizada](AUDITORIA-DETALLADA.md)
- [Guía operativa y compatibilidad](docs/ARQUITECTURA.md)
- [Protocolo de revalidación V4.1](docs/PROTOCOLO-REVALIDACION-V4.1.md)
- [Diagnóstico y plan de reconciliación V4.2](docs/RECONCILIACION-AGENTES-V4.2.md)
- [Guía de equipos V4: seguridad, fallos y prueba funcional](docs/OPERACION-EQUIPOS-V4.md)
- [Registro V4 de agentes y perfiles](registry/vx-agent-registry-v4.json)
- [Instalador](scripts/Instalar-Kilo-Global-Harness.ps1)
- [Documentación oficial de Kilo sobre settings](https://kilo.ai/docs/getting-started/settings)
- [Skills globales](https://kilo.ai/docs/customize/skills)
- [Agentes globales](https://kilo.ai/docs/customize/custom-subagents)
- [Comandos](https://kilo.ai/docs/customize/workflows)

## V4 — Componer equipos globales

El registro `registry/vx-agent-registry-v4.json` describe cinco nuevos subagentes VX de **solo lectura**, dos agentes existentes y nueve perfiles de trabajo. `/vx-equipo` permite a `vx-integrador` coordinar investigación, implementación y revisión con Kilo nativo. No se ejecuta ningún motor externo ni se importan agentes de terceros sin revisión de licencia y seguridad.

Comprueba el registro y recibe una propuesta desde PowerShell (sin invocar modelos):

```powershell
Set-Location 'D:\Proyectos\Kilo-Global-Harness'
pwsh -NoProfile -File .\scripts\Validar-Registro-V4.ps1
pwsh -NoProfile -File .\scripts\Seleccionar-Equipo-V4.ps1 -Perfil cloudflare
pwsh -NoProfile -File .\scripts\Seleccionar-Equipo-V4.ps1 -Tarea 'Auditar UI React' -Json
```

La V4 **no modifica** los 12 agentes mezclados entre JSON/Markdown ni los 19 limites `steps: 10000000`: quedan pendientes de reconciliación con pruebas de compatibilidad. El selector no controla realmente el costo del modelo; solo acota delegaciones propuestas.

## V4.2 — Auditoría de compatibilidad de agentes

Sin editar `kilo.jsonc` ni copiar credenciales, ejecuta:

```powershell
pwsh -NoProfile -File '.\scripts\Reconciliar-Agentes-V4.2.ps1'
pwsh -NoProfile -File '.\scripts\Reconciliar-Agentes-V4.2.ps1' -Json
```

Después de instalar, el script queda en `~/.config/kilo/harness/scripts/` y el comando `/vx-reconciliar` queda disponible en Kilo. Los resultados son una propuesta de análisis, **no cambios aplicados**. Ver [protocolo V4.2](docs/RECONCILIACION-AGENTES-V4.2.md).

## Changelog

- **4.2.0 · 2026-11-14:** herramienta de reconciliación de agentes globales JSONC/Markdown, detección de solapamiento de campos y `steps`, protección de datos sensibles, CI Windows y distribución reversible. No modifica la configuración heredada.

- **4.1.0 · 2026-11-14:** comando global `/vx-revalidar`, snapshots Git de solo lectura, descarte explícito de falsos positivos y diferenciación de evidencia de código frente a tests ejecutados. Sin cambios de permisos/modelos/MCP.

- **4.0.0 · 2026-11-13:** registro global, cinco subagentes read-only, `/vx-equipo`, selector, validador, instalador reversible y pruebas en CI Windows.
- **3.1.0 · 2026-11-13:** auditoría global de solo lectura (sin secretos), comando de verificación ImageGen sin generación automática, aclaración de precedencia de agentes y plugins.
- **3.0.0 · 2026-11-13:** instalador global idempotente, AGENTS administrado sin tocar JSONC, simulación, backups con hashes, rollback conservador, skill V3, dos agentes VX globales, workflows actualizados y CI.
- **2.1.0:** política autónoma, Git main permanente y pausa opcional de task-observer.
- **2.0.0:** ciclo ingeniería y primera auditoría global.
