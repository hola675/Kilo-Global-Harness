# VECIDYA · Kilo Global Harness / VX Evolution

> **BASELINE SOURCE ACTUAL — Dev Team 2.3.0 reviewer-specialist:** **`vx-dev-team`** es el único agente personalizado visible. Puede delegar mediante `task` a **10 subagentes ocultos de análisis no mutable**. Los hijos no escriben, no ejecutan shell, no cargan skills, no delegan ni usan Board/Agent Manager. `read: deny` mantiene ocultos los helpers MCP genéricos; MCP sigue deny-by-default y `vx-dev-research` dispone únicamente de cinco tools documentales explícitas de Context7/Microsoft Learn. `glob` y `grep` son capacidades mínimas y `lsp: allow` queda como capacidad opcional si el host la expone. `kilo.jsonc` y el resto del pack MCP se preservan como infraestructura separada.

> **Pack VX V0.3.0 + Dev Team V1 (2026-11-17):** **13 agentes VX y 31 skills en código**. Se añade `vx-dev-team` como agente primario visible `vx-dev-team`, con color propio `#8B5CF6`, delegación a especialistas VX y gates MCP conservadores. El pack conserva router/DAG, doctor, bootstrap DPAPI y reversión auditada. **VX Evolution V4.7.2** se integra solo como contratos aislados; `approval_granted=false` y `apply_supported=false`. **En la fecha de esta integración era solo código; posteriormente el operador instaló el Pack por convivencia y verificó sus archivos. La integración no activa scheduler, WebAuthn real ni publicación.** [Acta de integración](docs/VX-CONSOLIDACION-MAIN-20261116.md) · [17 hallazgos corregidos](docs/VX-AUDITORIA-COHERENCIA-PACK-20261116.md).

**Versión del código:** 4.6.3 · **Manifiesto del instalador:** 4.0.0 (restauración compatible con V3/V4) · **Estado:** V4.5.1 integrada y CI Windows PASS; **SQLite v4 y calendario V4.5.1 verificados en el Windows del usuario**. V4.6.0 y V4.6.1 tienen CI Windows PASS y validación local real de sus CLI, con 28 agentes únicos y 40 skills; pendiente prueba interactiva tras /reload. V4.6.2 tiene CI Windows PASS y CLI local validado (5 casos y destinos); después se recibieron 5/5 respuestas coincidentes en chat con fixtures sintéticos públicos. Atribución efectiva a especialistas/skills y competencia real NO_VERIFICADAS. PowerShell dentro de Kilo permanece bloqueado por política. V4.6.3 tiene CI Windows PASS y CLI local validado: 11 solapamientos de agentes, 0 diferencias explícitas comparadas, 19 límites steps elevados y 30 hallazgos de revisión; ninguna colisión de runtime ni competencia verificada. Ninguna reunión automática está habilitada.

Harness de ingeniería autónoma **exclusivamente para Kilo Code** en VS Code/VSCodium. Se instala **exclusivamente en el perfil GLOBAL de Windows**. Los proyectos no reciben skills, agentes, reglas, comandos ni MCP locales. El código y los documentos propios de cada proyecto sí pueden desarrollarse normalmente.

**IDA MCP (Pack VX 0.2.1, 2026-11-16):** [skill original para IDA 9.4+](skills/vx-ida-mcp-reverse-engineering/SKILL.md) y [comando /vx-ida](commands/vx-ida.md), perfil `reverse-engineering`, router con 31 skills y un sexto MCP **opcional y deshabilitado**. Preferencia por [servidor oficial Hex-Rays](https://github.com/HexRaysSA/ida-mcp); diagnóstico de HCLI/IDAPython sin cambios de configuración. **No equivale a instalar o conectar IDA MCP**, ni amplía ACL de agentes. Las menciones históricas a 30 skills/5 MCP describen el Pack antes de esta ampliación.

**VX Academy (V4.8 en diseño, no activa):** el trabajo de PR #28 añade [currículo](docs/VX-ACADEMY-CAPACITACION-V1-20261115.md), [mentoría](docs/VX-ACADEMY-MENTORIA-EVOLUCION-V1-20261115.md), [evaluación independiente](docs/VX-ACADEMY-EVALUADOR-INDEPENDIENTE-V1-20261115.md) y [grafo de organización propuesto](registry/vx-organization-graph-v1.proposal.json). Su inventario original de 7 agentes y 2 skills corresponde a una fotografía del **15 de noviembre**, anterior al Pack actual de **13 agentes VX/31 skills VX**; el recuento histórico de **30 skills VX** es de antes de añadir la skill IDA. Los catálogos académicos son propuestas, no roles adicionales, certificados ni mecanismos de activación.

**Pack VX global instalado y P1 completada en Kilo (2026-11-16, estado histórico previo a Dev Team V1):** el operador instaló por convivencia con 19 agentes inline y skills externas intactas: 12/12 agentes VX de aquella versión y 31/31 skills VX en disco, respaldos DPAPI y MCP sin cambios. Se observó en captura el selector `Vx Integrador` activo y los cinco builders visibles; la herramienta nativa `skill` cargó `vx-engineering-harness` y `vx-ida-mcp-reverse-engineering`. En P1, `task` a `vx-inspector` terminó primero `BLOCKED` por repetir un prerequisito de interfaz y, después de trasladar la confirmación visual del operador, `completed` con revisión del README de solo lectura declarada. **Delegación efectiva de lectura: evidenciada por respuesta de `task`; permisos efectivos de inspector y builders, conexión IDA MCP y precedencia siguen NO VERIFICADOS.** [Guía de convivencia](docs/VX-INSTALACION-CONVIVENCIA-0.2.3-WINDOWS.md) · [Acta y piloto siguiente](docs/VX-CERTIFICACION-RUNTIME-20261116.md). El instalador 0.2.2 limpio no es el mecanismo recomendado para este HOME.

**P2.1: selector correcto antes de editar (2026-11-16).** En la captura de VX-Team-Lab el agente seleccionado era **Code**, no **Vx Docs Builder**, y el control de autonomía mostraba **Auto** (sin prueba de aprobación manual). Por ello la respuesta anterior de `TOOL_UNAVAILABLE` **no demuestra un fallo de ACL del builder**. El nuevo comando global `/vx-p2` solicita `vx-docs-builder` mediante frontmatter y empieza en diagnóstico de solo lectura; la edición requiere confirmación visual del agente y aprobación manual por acción, con la primera solicitud rechazada. Se conservan `edit: ask`, `bash: deny` y los 19 agentes inline/skills externas. [Acta y procedimiento](docs/VX-CERTIFICACION-RUNTIME-20261116.md).

## MCP Pack global V1 — 13 servidores reproducibles (2026-11-17)

El entorno Kilo Desktop de referencia tiene **13/13 MCP conectados**: Codebase Memory, IDA, Playwright, Context7, ImageGen, GitHub, Cloudflare API, Chrome DevTools, Snyk, Postman, Microsoft Learn, Sentry y Serena.

Este pack es **independiente del instalador general del Harness**. `scripts/Instalar-Kilo-Global-Harness.ps1` conserva su política histórica y **no modifica MCP ni credenciales**. Solo `scripts/Instalar-MCP-Pack-Windows.ps1`, invocado explícitamente por el operador, puede instalar dependencias locales y registrar esos 13 MCP en `kilo.jsonc`, siempre con backup previo.

- [Guía completa de instalación, autenticación, actualización y rollback](docs/VX-MCP-PACK-WINDOWS-V1-20261117.md)
- [Registro operativo MCP V2](registry/vx-mcp-catalog-v2.json)
- [Snapshot del runtime validado](inventory/mcp-runtime-2026-11-17.json)
- [Instalador MCP para Windows](scripts/Instalar-MCP-Pack-Windows.ps1)
- [Validador estático del pack](scripts/Validar-MCP-Pack.ps1)
- [Wrapper GitHub sin token persistente](scripts/mcp/github-mcp-kilo.ps1)

El registro no contiene secretos. OAuth permanece interactivo; GitHub obtiene su token desde el keyring de `gh` únicamente en memoria del proceso. “Connected” acredita handshake MCP; las capacidades funcionales se documentan separadamente según las pruebas realmente realizadas.

## vx-dev-team — source 2.3.0 + evidencia runtime V2-R.2

El diseño mantiene **un solo modo personalizado visible**: `vx-dev-team`, mostrado como **`vx-dev-team`** con color `#8B5CF6`. La evidencia runtime aprobada V2-R.2 es histórica; la baseline source 2.3.0 todavía requiere despliegue/sync y validación explícita antes de considerarse certificada en Kilo Desktop.

Detrás del líder existen diez especialistas `mode: subagent` y `hidden: true`:

- `vx-dev-explorer` — cartografía del codebase con `CODE_MAP` e `IMPACT_SURFACE`
- `vx-dev-architect` — decisiones estructurales con `OPTIONS`, `TRADEOFFS`, `CONTRACTS` y `DECISIONS_REQUIRED`
- `vx-dev-frontend` — UI flows, component/state model, interaction states, accessibility/responsive y API touchpoints
- `vx-dev-backend` — APIs, servicios, dominio, auth de aplicación e integraciones
- `vx-dev-data` — schemas, persistencia, queries, constraints, índices y migraciones
- `vx-dev-platform` — runtime/build/configuración/entrega con análisis read-only
- `vx-dev-reviewer` — revisión independiente del cambio implementado, sin aprobar merges
- `vx-dev-quality` — invariants, test matrix, oracles, regression surface y verification plan
- `vx-dev-security` — assets, trust boundaries, attack surface, access control y evidence-backed threat findings
- `vx-dev-research` — investigación técnica con `SOURCE_LEDGER`, `CONTRADICTIONS` y allowlist documental Context7/Microsoft Learn

Todos los hijos requieren `glob` y `grep`; `lsp` queda permitida pero es opcional porque Kilo solo registra esa tool cuando el host habilita `KILO_EXPERIMENTAL_LSP_TOOL`. Tienen `read/edit/write/apply_patch/bash/task/skill/agent_manager/board: deny`. El `read: deny` mantiene ocultas las herramientas genéricas de recursos MCP.

El líder escala el esfuerzo según complejidad: 0-1 especialista para tareas simples, 1-2 para medias y 2-4 para complejas. No invoca los diez por defecto y la profundidad máxima es una sola: **Usuario → vx-dev-team → Subagente**.

La evolución del equipo se hace por responsabilidades estables, no por cantidad de agentes. `vx-dev-backend` y `vx-dev-data` sustituyen al antiguo `vx-dev-backend-data`; `vx-dev-platform` y `vx-dev-reviewer` ya forman parte del source y de la ACL del líder. Ninguno de los especialistas nuevos hereda automáticamente certificación runtime histórica.

GitHub no despliega automáticamente estas definiciones al runtime de Kilo Desktop; una actualización del source requiere instalación/sincronización explícita y reload antes de validar el comportamiento efectivo.

Los MCP globales siguen siendo infraestructura independiente y deny-by-default para el equipo. `vx-dev-research` y `vx-dev-architect` tienen únicamente cinco tools documentales explícitas de Context7/Microsoft Learn cada uno; cualquier otra tool MCP requiere allowlist específica y certificación separada.

- [Diseño operativo V2-R.2](docs/VX-DEV-TEAM-V2R-READONLY.md)
- [Matriz MCP read-only V1 — propuesta inactiva](docs/VX-DEV-TEAM-MCP-READONLY-MATRIX-V1.md)
- [Registro estructurado MCP read-only V1](registry/dev-team-mcp-readonly-matrix-v1.proposal.json)
- [Certificación runtime de los cinco especialistas pendientes](docs/VX-DEV-TEAM-V2R2-CERTIFICACION-ESPECIALISTAS.md)
- [Contrato estructurado de certificación](registry/dev-team-v2r2-specialist-certification-v1.json)
- [Baseline estructurado V2-R](registry/dev-team-readonly-baseline-v2.json)
- [Baseline V1 supersedido](registry/dev-team-only-baseline-v1.json)
- [Arquitectura V1 histórica](docs/VX-DEV-TEAM-ARCHITECTURE-V1.md)
- [Matriz MCP V1 histórica](docs/VX-DEV-TEAM-MCP-MATRIX-V1.md)

**Estado de evidencia:** la certificación runtime **V2-R.2 7/7** se conserva como evidencia histórica e incluye al ya supersedido `vx-dev-backend-data`. La baseline source **2.3.0** contiene **10 especialistas**; `vx-dev-backend`, `vx-dev-data`, `vx-dev-platform` y `vx-dev-reviewer` requieren despliegue/sync y smoke runtime antes de recibir estado operativo propio. La Wave 1 documental de Research/Architect conserva sus allowlists exactas.


## Principios

- **Global-only**: `~/.config/kilo/{AGENTS.md,agents/,commands/,rules/}` y `~/.kilo/skills/`.
- **AutoApprove conservado**: no cambia settings de VS Code ni permisos de agentes.
- **main permanente**: una rama temporal `work/*` por tarea no trivial, validación, PR/merge según protección GitHub y eliminación exclusiva de la rama propia después de verificar integración.
- **Sin reescritura de `kilo.jsonc`**: modelos, MCP, tokens, versiones y límites steps quedan intactos.
- **PC ÚNICA:** VX Evolution usa exclusivamente este Windows. Sin sincronización multi-PC, infraestructura cloud ni configuración Kilo por repositorio.
- **Kilo Desktop V4.6.3:** siete agentes VX y dos skills VX visibles globalmente; `task` completó una sesión hija, pero identidad interna y llamada `skill` siguen sin certificar. [Evidencia y puerta de V4.7](docs/VX-DESKTOP-VALIDACION-Y-PUERTA-V4.7-20261114.md).
- **VX Organización V4.6.3:** informe solo lectura de solapamientos, steps declarados, perfiles y fuentes Kilo; no afirma precedencia, procedencia de subagentes, jerarquías ni rendimiento.
- **VX Ensayos V4.6.2:** cinco escenarios sintéticos para contraste manual antes/después, sin ejecutar agentes, puntuar ni activar roles; evidencia aportada siempre declarada.
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
$script = Join-Path (Get-Location) 'scripts\Instalar-DevTeam-Only.ps1'
pwsh -NoProfile -File $script -Modo Diagnostico
pwsh -NoProfile -File $script -Modo Simular
pwsh -NoProfile -File $script -Modo Aplicar
pwsh -NoProfile -File $script -Modo Verificar
```

El reset crea un respaldo privado reversible en `~/.config/kilo-devteam-backups/AAAAmmdd-HHMMSS-fff-sufijo`. No modifica `kilo.jsonc`, MCP ni recursos ajenos al namespace VX.

Finalmente, en Kilo ejecuta `/reload` y confirma visualmente que, además de los modos nativos, el único agente VX visible sea `vx-dev-team`. No uses comandos `/vx-*` legacy.

## Reversión

Utiliza la ruta de respaldo que imprimió el instalador:

```powershell
pwsh -NoProfile -File $script -Modo Restaurar -BackupFolder 'C:\Users\Admin\.config\kilo-devteam-backups\AAAAMMDD-HHMMSS-fff-sufijo'
```

Por defecto, si un archivo administrado fue modificado **después de aplicar**, la restauración lo omite para evitar perder cambios. `-ForzarRestauracion` únicamente tras revisar esos cambios.

## Qué instala

| Origen | Destino global | Estado |
| --- | --- | --- |
| `agents/vx-dev-team.md` | `~/.config/kilo/agents/vx-dev-team.md` | primario visible `vx-dev-team` |
| `runtime/dev-team-v2r/agents/vx-dev-explorer.md` | `~/.config/kilo/agents/` | subagente oculto no mutable |
| `runtime/dev-team-v2r/agents/vx-dev-architect.md` | `~/.config/kilo/agents/` | subagente oculto read-only |
| `runtime/dev-team-v2r/agents/vx-dev-frontend.md` | `~/.config/kilo/agents/` | subagente oculto read-only |
| `runtime/dev-team-v2r/agents/vx-dev-backend.md` | `~/.config/kilo/agents/` | subagente oculto backend read-only |
| `runtime/dev-team-v2r/agents/vx-dev-data.md` | `~/.config/kilo/agents/` | subagente oculto data read-only |
| `runtime/dev-team-v2r/agents/vx-dev-quality.md` | `~/.config/kilo/agents/` | subagente oculto read-only |
| `runtime/dev-team-v2r/agents/vx-dev-security.md` | `~/.config/kilo/agents/` | subagente oculto read-only |
| `runtime/dev-team-v2r/agents/vx-dev-research.md` | `~/.config/kilo/agents/` | subagente oculto read-only |

El instalador canónico es `scripts/Instalar-DevTeam-Only.ps1`. Retira del perfil global agentes VX legacy no aprobados, comandos/rules/plugins/skills VX heredados y preserva recursos de terceros. **No modifica `kilo.jsonc`, modelos, AutoApprove ni MCP.**


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
- [VX Ensayos V4.6.2: escenarios y comparación declarativa manual](docs/VX-ENSAYOS-COMPETENCIAS-V4.6.2.md)
- [Cierre de CLI V4.6.2 en Windows y bloqueo de herramienta en Kilo](docs/VX-VALIDACION-CLI-V4.6.2-20261114.md)
- [Cierre de batería sintética V4.6.2: cinco respuestas coincidentes y límites de evidencia](docs/VX-CIERRE-BATERIA-V4.6.2-20261114.md)
- [VX Auditoría organizativa V4.6.3: criterios y validación](docs/VX-AUDITORIA-ORGANIZATIVA-V4.6.3.md)
- [Validación CLI en Windows de V4.6.3: 30 hallazgos estáticos, sin cambios activos](docs/VX-VALIDACION-LOCAL-V4.6.3-20261114.md)
- [Revisión de 11 solapamientos y límites steps declarados de diez millones](docs/VX-REVISION-STEPS-PRECEDENCIA-V4.6.3-20261114.md)
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

## Fase V4.6 — historial de capacitación y auditoría con evidencia (no es la siguiente fase activa)

**Estado histórico V4.6:** las CLI de V4.6.0–V4.6.3 fueron probadas localmente en Windows y CI; V4.6.2 incluyó una batería conversacional con 5/5 respuestas coincidentes con fixtures públicos, sin demostrar competencia real. El Pack VX actual se instaló por convivencia y su piloto P1 logró una delegación nativa `task` a `vx-inspector` tras una denegación inicial por traspaso insuficiente de contexto. **Siguiente puerta activa:** P2 de permisos de builders `ask` en un proyecto sintético aislado, con autorización específica, no evaluación automática de V4.6. La ejecución de PowerShell desde Kilo sigue bloqueada; scheduler OFF.

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

Esta auditoría recorre únicamente fuentes Kilo **globales** y no abre SQLite ni crea propuestas. Compara fuentes JSONC/Markdown, límites `steps`, permisos simples y skills repetidas por nombre; cruza las **declaraciones** del router. Desempeño de agente y precedencia efectiva = **NO_MEDIDO/NO_VERIFICADO**. Ver [guía V4.6.0](docs/VX-CAPACIDADES-V4.6.0.md) y [roadmap](docs/VX-EVOLUTION-ROADMAP.md). La V4.6.1 añadió la matriz local de competencias sin ejecutar agentes; V4.6.2 y V4.6.3 se cerraron posteriormente como pruebas de metadatos/CLI, no como certificación de capacidades reales. No se crearán jefes ni agentes automáticamente.

## V4.6.1 — Matriz global de competencias (solo lectura)

Después de instalar la versión integrada, ejecutar `/vx-matriz` o:

```powershell
$matrix = Join-Path $HOME '.config/kilo/harness/scripts/vx_competency_matrix.py'
python -I $matrix              # resumen privado, sin nombres individuales
python -I $matrix --json       # matriz detallada: mantener LOCAL
```

Cruza declaraciones V4.6.0 con IDs estables para planificar pruebas futuras. Acepta evidencia JSON opcional dentro de HOME, pero **un PASS declarado jamás equivale a competencia verificada**. Niveles y puntuación siguen `NO_ASIGNADO` y `NO_MEDIDO`. Guía: [V4.6.1](docs/VX-MATRIZ-COMPETENCIAS-V4.6.1.md).

## V4.6.2 — Ensayos sintéticos de competencia (sin ejecutar modelos)

Cuando el cambio esté integrado e instalado, utilizar `/vx-ensayos` o:

```powershell
$trial = Join-Path $HOME '.config/kilo/harness/scripts/vx_competency_trials.py'
python -I $trial
python -I $trial --list-cases
```

La herramienta muestra cinco escenarios de revisión, regresión y calidad de evidencia; no ejecuta agentes y no crea archivos de resultados. Un caso que coincida con su fixture **no demuestra competencia**, ya que las respuestas son declaradas y el banco es público. Ver [V4.6.2](docs/VX-ENSAYOS-COMPETENCIAS-V4.6.2.md).

## V4.5.1 — Primera reunión conjunta del mes

Se confirma **una sesión cada primer lunes a las 09:00 hora local de Windows**, con dos secciones independientes del acta: cierre mensual del mes anterior y seguimiento semanal. No hay scheduler ni notificaciones. Para usuarios con SQLite v3, migrar explícitamente mediante `python -I $vx joint-migrate --json` (genera backup) y comprobar `integrity` antes de crear actas; v2 requiere antes `meeting-migrate`. Los comandos manuales `meeting-joint-calendar`, `meeting-joint-prepare`, `meeting-joint-view` y `meeting-joint-close` no programan reuniones. La confirmación de decisiones y cierre sigue siendo interactiva.

## Changelog

- **V2-R.2 certificación · 2026-11-17:** 7/7 especialistas runtime certificados mediante evidencia del operador; glob/grep disponibles, LSP opcional, read/mutación/shell/task/skill/MCP ausentes. Próxima fase: diseño MCP read-only tool-by-tool, sin activación todavía.

- **Dev Team V1 · 2026-11-17:** nuevo agente primario `vx-dev-team` visible como `vx-dev-team`, color propio, 13 agentes VX/31 skills, delegación a especialistas y política MCP conservadora (`Context7`/`Microsoft Learn` allow; resto ask). No modifica `kilo.jsonc` ni los 13 MCP; smoke visual en Desktop pendiente tras instalación/reload.

- **Validación Desktop · 2026-11-14:** inventario global VX y delegación de tarea confirmados con limitaciones, sin certificar carga de skill. Próxima fase V4.7: diseño de publicación segura, pruebas aisladas y aprobación explícita; ningún cambio activo.

- **Inventario steps V4.6.3 cerrado · 2026-11-14:** 19/19 entradas por encima de 400 tienen steps=10000000 en JSONC. Fuente efectiva, rondas consumidas, impacto y límites alternativos NO_VERIFICADOS; propuesta de evaluación sin cambios operativos.

- **Revisión de límites 4.6.3 · 2026-11-14:** 11 agentes con nombres superpuestos y ninguna diferencia en los metadatos simples cotejados; 10 de 19 entradas steps elevadas muestran 10 millones. Documentación oficial de Kilo consultada; funcionamiento en esta instalación y las nueve entradas restantes todavía pendientes. Solo documentación, sin cambio de límites.

- **Cierre local V4.6.3 · 2026-11-14:** instalación y CLI Windows PASS; 11 solapamientos, 0 diferencias explícitas, 19 valores steps elevados, 30 hallazgos de metadatos; sin prueba de precedencia o delegación real. Solo actualización documental, scheduler OFF.

- **4.6.3 · 2026-11-14:** auditor de organización Kilo declarativa, comando global /vx-organizacion, pruebas de metadatos y CI Windows; no ejecuta modelos ni modifica agentes, skills o SQLite. Validación local pendiente.

- **Cierre de batería 4.6.2 · 2026-11-14:** cinco respuestas coinciden con fixtures públicos, una retransmisión duplicada no se contabilizó, sesiones atribuidas no verificadas; 0 niveles asignados. Solo documentos, sin modificaciones operativas.

- **4.6.2 verificación local · 2026-11-14:** PowerShell local confirma 5 escenarios/5 destinos; 0 coincidencias, 0 respuestas, rendimiento NO_MEDIDO. PowerShell dentro de Kilo bloqueado por política, sin ejecución de agentes. Solo documentación, sin cambios de runtime.

- **4.6.2 · 2026-11-14:** cinco escenarios sintéticos, comparación declarativa antes/después, controles de falsos positivos y privacidad, comando /vx-ensayos y CI Windows. Los resultados no constituyen evaluación real de agentes ni autorizan cambios.
- **Cierre local 4.6.0–4.6.1 · 2026-11-14:** CLI local ejecutado sin errores: 39 fuentes/28 agentes, 40 skills, 11 solapamientos, 19 límites steps elevados, 76 filas, 15 declaraciones, 0 evidencias. Rama temporal V4.6.1 eliminada y solo main remota; prueba interactiva Kilo pendiente.

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
