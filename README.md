# VECIDYA · Kilo Code Global Harness V3.0

**Versión:** 3.0.0 · **Estado:** candidato a validación mediante CI y prueba real en Windows.

Harness de ingeniería autónoma para Kilo Code en VS Code/VSCodium. Se instala **exclusivamente en el perfil GLOBAL de Windows**. Los proyectos no reciben skills, agentes, reglas, comandos ni MCP locales. El código y los documentos propios de cada proyecto sí pueden desarrollarse normalmente.

## Principios

- **Global-only**: `~/.config/kilo/{AGENTS.md,agents/,commands/,rules/}` y `~/.kilo/skills/`.
- **AutoApprove conservado**: no cambia settings de VS Code ni permisos de agentes.
- **main permanente**: una rama temporal `work/*` por tarea no trivial, validación, PR/merge según protección GitHub y eliminación exclusiva de la rama propia después de verificar integración.
- **Sin reescritura de `kilo.jsonc`**: modelos, MCP, tokens, versiones y límites steps quedan intactos.
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

Finalmente, en Kilo ejecuta `/reload`, luego `/vx-harness-estado` y `/vx-mcp`.

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

Todos los destinos anteriores están bajo HOME. Si se ejecuta desde `D:\Proyectos`, **no escribe allí**; esa carpeta es exclusivamente la fuente versionada del instalador.

### Limitaciones deliberadas

- No ejecuta automáticamente `git push`, `git merge` ni el borrado de ramas en tus repositorios; **define el comportamiento que Kilo debe seguir cuando realiza una tarea autorizada**. Si una protección del remoto bloquea una operación, no se elude.
- No cambia modelos ni fuerza un límite `steps` diferente. La auditoría detecta riesgos y el agente puede recomendar cambios posteriormente, con evidencia de compatibilidad.
- No instala ni repara servidores MCP automáticamente; distingue configuración de conectividad.
- Los agentes heredados definidos en `kilo.jsonc` y en Markdown no se eliminan ni modifican, porque pueden tener precedencia o permisos diferentes.
- La validación CI es un smoke test del instalador en Windows aislado. No valida conexión de los MCP del PC ni el comportamiento real de los modelos Kilo.

## Documentación

- [Auditoría actualizada](AUDITORIA-DETALLADA.md)
- [Guía operativa y compatibilidad](docs/ARQUITECTURA.md)
- [Instalador](scripts/Instalar-Kilo-Global-Harness.ps1)
- [Documentación oficial de Kilo sobre settings](https://kilo.ai/docs/getting-started/settings)
- [Skills globales](https://kilo.ai/docs/customize/skills)
- [Agentes globales](https://kilo.ai/docs/customize/custom-subagents)
- [Comandos](https://kilo.ai/docs/customize/workflows)

## Changelog

- **3.0.0 · 2026-11-13:** instalador global idempotente, AGENTS administrado sin tocar JSONC, simulación, backups con hashes, rollback conservador, skill V3, dos agentes VX globales, workflows actualizados y CI.
- **2.1.0:** política autónoma, Git main permanente y pausa opcional de task-observer.
- **2.0.0:** ciclo ingeniería y primera auditoría global.
