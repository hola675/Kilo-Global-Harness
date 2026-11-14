# VECIDYA · Kilo Code Global Harness V4.6.1

**Versión del código:** 4.6.1 · **Manifiesto del instalador:** 4.0.0 (restauración compatible con V3/V4) · **Estado:** V4.5.1 integrada y CI Windows PASS; **SQLite v4 y calendario V4.5.1 verificados en el Windows del usuario**. V4.6.0 ya está integrada en main y validada en CI; V4.6.1 incorpora una matriz de evidencias declaradas con CI Windows PASS. Ambas herramientas están pendientes de validación en el Kilo real del usuario; ninguna reunión automática está habilitada.

Harness de ingeniería autónoma **exclusivamente para Kilo Code** en VS Code/VSCodium. Se instala **exclusivamente en el perfil GLOBAL de Windows**. Los proyectos no reciben skills, agentes, reglas, comandos ni MCP locales. El código y los documentos propios de cada proyecto sí pueden desarrollarse normalmente.

## Principios

- **Global-only**: `~/.config/kilo/{AGENTS.md,agents/,commands/,rules/}` y `~/.kilo/skills/`.
- **AutoApprove conservado**: no cambia settings de VS Code ni permisos de agentes.
- **main permanente**: una rama temporal `work/*` por tarea no trivial, validación, PR/merge según protección GitHub y eliminación exclusiva de la rama propia después de verificar integración.
- **Sin reescritura de `kilo.jsonc`**: modelos, MCP, tokens, versiones y límites steps quedan intactos.
- **PC ÚNICA:** VX Evolution usa exclusivamente este Windows. Sin sincronización multi-PC, infraestructura cloud ni configuración Kilo por repositorio.
- **VX Matriz V4.6.1:** análisis de agentes y skills con test IDs estables y evidencias opcionales declaradas, sin asignar nivel, score o ascensos; no ejecuta pruebas ni escribe SQLite.
- **VX Capacidades V4.6.0:** auditoría global de metadatos JSONC/Markdown y skills; diferencias de fuentes y capacidades **declaradas, no probadas**; nunca modifica SQLite, agentes, permisos ni skills.
- **Roadmap canónico:** [VX Evolution — estado verificado y fases V4.6–V5](docs/VX-EVOLUTION-ROADMAP.md). No confundir código/CI con validación del perfil Windows.
- **VX Reunión V4.5:** cierre mensual y semanal en **una sesión conjunta el primer lunes a las 09:00 hora local Windows**, con dos secciones; resto de lunes, solo semanal. SQLite v4, calendario, agendas, notas y decisiones manuales; sin scheduler, autopromociones ni notificaciones.
- **VX Observer V4.4:** captura opcional de tres señales Kilo con contadores horarios privados, sin mensajes ni llamadas a modelos.
- **VX Evolution V4.3:** motor global Kilo-only de inventario, observaciones explícitas, propuestas de versiones y vista previa de reuniones; ninguna aprobación o instalación automática.
- **Reconciliación V4.2 (solo diagnóstico)**: compara con metadatos seguros las fuentes JSONC y Markdown; no elimina agentes ni cambia sus permisos o pasos.
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

Si ya pausaste `task-observer`, la opción no realiza ningún nuevo movimiento. El respaldo único por ejecución (incluye milisegundos y sufijo aleatorio) se guarda en `~/.config/kilo-harness-backups/AAAAmmdd-HHMMSS-fff-sufijo` y **nunca debe subirse a GitHub**.

Finalmente, en Kilo ejecuta `/reload`, `/vx-harness-estado` y `/vx-equipo`. Antes de delegaciones automáticas, revisa la [guía operativa V4](docs/OPERACION-EQUIPOS-V4.md).

## Reversión

Utiliza la ruta de respaldo que imprimió el instalador:

```powershell
pwsh -NoProfile -File $script -Modo Restaurar -BackupFolder 'C:\Users\Admin\.config\kilo-harness-backups\AAAAMMDD-HHMMSS-fff-sufijo'
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
| `scripts/{Seleccionar-Equipo-V4,Validar-Registro-V4,Reconciliar-Agentes-V4.2}.ps1` | `~/.config/kilo/harness/scripts/` | Enrutamiento, validación y diagnóstico |
| `scripts/vx_evolution_core.py` | `~/.config/kilo/harness/scripts/` | Motor local Kilo-only; no crea BD durante la instalación |
| `skills/vx-evolution-core/SKILL.md` | `~/.kilo/skills/` | Guía de gobernanza por demanda |
| `commands/vx-{evolution,observer,upgrade,capacitacion,auditoria-equipo,reunion}.md` | `~/.config/kilo/commands/` | Departamentos lógicos de VX Evolution |
| `plugins/vx-observer-light.js` | `~/.config/kilo/plugin/` | **Solo opt-in** con `-InstalarVXObserverV44`; permanece apagado hasta `observer-mode light` |

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
- [VX Evolution V4.3: arquitectura, contratos, seguridad y decisiones](docs/VX-EVOLUTION-V4.3.md)
- [VX Observer V4.4: instalación opt-in, privacidad, migración y pruebas](docs/VX-OBSERVER-V4.4.md)
- [VX Capacidades V4.6.0: diagnóstico solo lectura y contrato de evidencias](docs/VX-CAPACIDADES-V4.6.0.md)
- [VX Matriz V4.6.1: contrato, evidencias y rúbrica propuesta](docs/VX-MATRIZ-COMPETENCIAS-V4.6.1.md)
- [VX Reunión V4.5: fechas locales, actas y decisiones manuales](docs/VX-REUNION-V4.5.md)
- [Decisiones aprobadas y pendientes sobre reuniones, retención y autonomía](docs/VX-EVOLUTION-DECISIONES.md)
- [Roadmap maestro VX Evolution: estado real, brechas y plan V4.6–V5](docs/VX-EVOLUTION-ROADMAP.md)
- [Política versionada de diseño para reunión semanal (desactivada)](config/vx-reunion-policy.v1.json)
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

## V4.3 — VX Evolution Core (Kilo Code únicamente)

Después de instalar, el operador puede consultar el motor **sin crear una base de datos**:

```powershell
$vx = Join-Path $HOME '.config/kilo/harness/scripts/vx_evolution_core.py'
python -I $vx status --json
```

Para comenzar a conservar observaciones globalmente hace falta inicializar **una sola vez** la BD privada de forma explícita:

```powershell
python -I $vx init --json
python -I $vx inventory-sync --json
python -I $vx meeting-preview --cadence weekly --json
python -I $vx integrity --json
```

**Decisión de gobierno:** futura `vx-reunion` semanal, lunes 09:00 según la zona horaria local de Windows. Está registrada solo en la especificación `config/vx-reunion-policy.v1.json`; no hay scheduler, notificaciones ni reunión automática hasta V4.5 probada y aprobada. La vista previa V4.3 todavía calcula periodos UTC.

Los slash commands `/vx-evolution`, `/vx-upgrade`, `/vx-capacitacion`, `/vx-auditoria-equipo`, `/vx-reunion` y `/vx-observer` coordinan funciones de gestión. **Ninguno permite publicar agentes o skills ni aprobar propuestas.** V4.4 introduce señales mínimas del runtime mediante un plugin opcional; **no** captura automáticamente resultados o calidad de cada tarea. Las reuniones programadas siguen pendientes de V4.5; el comando `observe` continúa siendo explícito. La base privada de VX Evolution no se elimina al restaurar versiones del instalador.

## V4.4 — Observer ligero de Kilo (instalación opcional)

No se instala ni activa automáticamente en una actualización normal. Para incorporarlo, ejecutar el instalador con `-InstalarVXObserverV44` (y `-Modo Verificar` con el mismo switch). El plugin permanece **inerte** hasta realizar la activación explícita `observer-mode --mode light`.

```powershell
$installer = '.\scripts\Instalar-Kilo-Global-Harness.ps1'
pwsh -NoProfile -File $installer -Modo Simular -InstalarVXObserverV44
pwsh -NoProfile -File $installer -Modo Aplicar -InstalarVXObserverV44
pwsh -NoProfile -File $installer -Modo Verificar -InstalarVXObserverV44
$vx = Join-Path $HOME '.config/kilo/harness/scripts/vx_evolution_core.py'
python -I $vx observer-status --json
```

Para una base anterior (schema v1), usar explícitamente `python -I $vx observer-migrate --json`, con backup previo automático. Para una instalación limpia, `python -I $vx init --json`. Tras reiniciar Kilo y revisar otros plugins, `python -I $vx observer-mode --mode light --json` autoriza solo señales agregadas; `python -I $vx observer-report --days 7 --json` las resume. Para apagar inmediatamente: `python -I $vx observer-mode --mode off --json`.

No hay instalación de nuevos MCP, cambios en AutoApprove ni servicio residente. El horario de `vx-reunion` del lunes a las 09:00 hora local sigue documentado pero sin programar.

## V4.5 — VX Reunión (manual y global)

La reunión semanal está definida **lunes a las 09:00 hora local Windows** y el cierre mensual para el **primer lunes del mes siguiente**, pero el cierre se integra con la semanal en **una única sesión el primer lunes a las 09:00**, con dos secciones independientes. El scheduler continúa **deshabilitado**.

```powershell
$vx = Join-Path $HOME '.config/kilo/harness/scripts/vx_evolution_core.py'
python -I $vx status --json
python -I $vx meeting-calendar --cadence weekly --json
python -I $vx meeting-calendar --cadence monthly --json
# Migración explícita de SQLite v2 a v3, con backup previo:
python -I $vx meeting-migrate --json
python -I $vx meeting-preview --cadence weekly --json
python -I $vx meeting-preview --cadence monthly --json
```

Para crear **voluntariamente** un borrador de acta: `meeting-prepare --cadence weekly|monthly --json`. Para consultar usar `meeting-view --id UUID --json`. Las decisiones necesitan una terminal interactiva local y no activan upgrades; ver [guía V4.5](docs/VX-REUNION-V4.5.md).

## Siguiente fase — V4.6: capacitación y auditoría con evidencia

**Estado:** V4.6.0 integrada y probada en CI; V4.6.1 implementada y CI Windows PASS; V4.6.2–V4.6.3 pendientes. La V4.5.1 ya fue validada en el Windows del usuario; todavía falta ejecutar allí la auditoría y matriz de V4.6. No activar scheduler.

La capacitación priorizará mejorar skills y especialistas existentes; la auditoría recomendará consolidación, delegación o contratación **solo con evidencia y evaluación independiente**. No introducir agentes, jerarquías, permisos, prompts, MCP ni cambios operativos automáticamente. Los contadores `session_idle` y `session_error` de V4.4 no demuestran calidad.

El roadmap, las puertas de validación, los criterios de aceptación, las fases 4.6.0–4.6.3 y las decisiones pendientes se mantienen en [`docs/VX-EVOLUTION-ROADMAP.md`](docs/VX-EVOLUTION-ROADMAP.md). El cierre mensual sigue siendo una **única sesión el primer lunes a las 09:00, con dos secciones**. Programador y notificaciones permanecen **OFF**.

## V4.6.0 — Diagnóstico global Kilo de capacidades (solo lectura)

La V4.5.1 ya está validada localmente con SQLite v4, integridad OK, Observer `light` y calendario conjunto del 7 de diciembre de 2026 a las 09:00. Se confirmó que esta organización VX funcionará exclusivamente en **un PC Windows**, sin sincronización.

Tras instalar la nueva versión del harness, usar `/vx-capacidades` en Kilo o consultar desde PowerShell:

```powershell
$audit = Join-Path $HOME '.config/kilo/harness/scripts/vx_capability_audit.py'
python -I $audit                 # resumen por defecto, sin nombres individuales
python -I $audit --json          # informe estructurado, revisión LOCAL
```

Esta auditoría recorre únicamente fuentes Kilo **globales** y no abre SQLite ni crea propuestas. Compara fuentes JSONC/Markdown, límites `steps`, permisos simples y skills repetidas por nombre; cruza las **declaraciones** del router. Desempeño de agente y precedencia efectiva = **NO_MEDIDO/NO_VERIFICADO**. Ver [guía V4.6.0](docs/VX-CAPACIDADES-V4.6.0.md) y [roadmap](docs/VX-EVOLUTION-ROADMAP.md). La V4.6.1 añade la matriz local de competencias, sin ejecutar pruebas reales; V4.6.2–4.6.3 siguen pendientes. No se crearán jefes ni agentes automáticamente.

## V4.6.1 — Matriz global de competencias (solo lectura)

Después de instalar la versión integrada, ejecutar `/vx-matriz` o:

```powershell
$matrix = Join-Path $HOME '.config/kilo/harness/scripts/vx_competency_matrix.py'
python -I $matrix              # resumen privado, sin nombres individuales
python -I $matrix --json       # matriz detallada: mantener LOCAL
```

Cruza declaraciones V4.6.0 con IDs estables para planificar pruebas futuras. Acepta evidencia JSON opcional dentro de HOME, pero **un PASS declarado jamás equivale a competencia verificada**. Niveles y puntuación siguen `NO_ASIGNADO` y `NO_MEDIDO`. Guía: [V4.6.1](docs/VX-MATRIZ-COMPETENCIAS-V4.6.1.md).

## V4.5.1 — Primera reunión conjunta del mes

Se confirma **una sesión cada primer lunes a las 09:00 hora local de Windows**, con dos secciones independientes del acta: cierre mensual del mes anterior y seguimiento semanal. No hay scheduler ni notificaciones. Para usuarios con SQLite v3, migrar explícitamente mediante `python -I $vx joint-migrate --json` (genera backup) y comprobar `integrity` antes de crear actas; v2 requiere antes `meeting-migrate`. Los comandos manuales `meeting-joint-calendar`, `meeting-joint-prepare`, `meeting-joint-view` y `meeting-joint-close` no programan reuniones. La confirmación de decisiones y cierre sigue siendo interactiva.

## Changelog

- **4.6.1 · 2026-11-14:** matriz Kilo global de solo lectura, enlaces agente/skill→capacidad→test ID→evidencia declarada, 20 pruebas unitarias, instalador reversible y CI Windows; sin evaluación ni cambios operativos.

- **4.6.0 · 2026-11-14:** auditoría global de Kilo solo lectura, pruebas de privacidad y regresión, revisión declarativa de agentes/skills, comando `/vx-capacidades`, instalación reversible. Sin cambios en SQLite, horarios, plugins o permisos.

- **2026-11-14 (documentación/roadmap, sin cambios de runtime):** evaluación del cierre V4.5.1 y plan V4.6 con subfases de capacitación, auditoría, pruebas y controles; bloqueo de scheduler conservado.

- **4.5.1 · 2026-11-14:** sesión conjunta con dos secciones, migración SQLite v4 respaldada, pruebas de coincidencia, privacidad y cierre indivisible; programador OFF.

- **4.5.0 · 2026-11-14:** calendario local de reuniones, cierre del mes anterior primer lunes siguiente, esquema SQLite v3 con migración backup, agendas de cinco propuestas, notas, decisiones y actas manuales; pruebas Windows. No crea automatizaciones.

- **4.4.0 · 2026-11-14:** plugin Kilo global opcional, captura enumerada de tres señales sin payload, SQLite schema v2 y migración explícita con backup, contadores horarios con límite, opt-in/off reversible, pruebas Windows y documentación de privacidad.

- **4.3.0 · 2026-11-14:** núcleo SQLite Kilo-only, inventario global de agentes/skills, observaciones y propuestas locales, agenda semanal/mensual previa, comandos de gobierno, skill, pruebas de privacidad y recuperación. Sin hooks ni scheduler.

- **4.2.0 · 2026-11-14:** herramienta de reconciliación de agentes globales JSONC/Markdown, detección de solapamiento de campos y `steps`, protección de datos sensibles, CI Windows y distribución reversible. No modifica la configuración heredada.

- **4.1.0 · 2026-11-14:** comando global `/vx-revalidar`, snapshots Git de solo lectura, descarte explícito de falsos positivos y diferenciación de evidencia de código frente a tests ejecutados. Sin cambios de permisos/modelos/MCP.

- **4.0.0 · 2026-11-13:** registro global, cinco subagentes read-only, `/vx-equipo`, selector, validador, instalador reversible y pruebas en CI Windows.
- **3.1.0 · 2026-11-13:** auditoría global de solo lectura (sin secretos), comando de verificación ImageGen sin generación automática, aclaración de precedencia de agentes y plugins.
- **3.0.0 · 2026-11-13:** instalador global idempotente, AGENTS administrado sin tocar JSONC, simulación, backups con hashes, rollback conservador, skill V3, dos agentes VX globales, workflows actualizados y CI.
- **2.1.0:** política autónoma, Git main permanente y pausa opcional de task-observer.
- **2.0.0:** ciclo ingeniería y primera auditoría global.
