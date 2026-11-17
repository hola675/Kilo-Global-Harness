# Dev Team Only — baseline aprobado V1

**Fecha:** 2026-11-17  
**Estado:** SUPERSEDED — reemplazado por Dev Team V2-R  
**Único agente personalizado aprobado:** `👥 Dev Team`  
**ID interno:** `vx-dev-team`

## Decisión

El Harness se reinicia sobre un baseline mínimo. Por ahora solo está aprobado el agente `vx-dev-team`.

No están aprobados todavía:

- subagentes VX;
- builders VX;
- advisers/reviewers VX;
- skills VX;
- comandos o workflows VX;
- reglas globales VX;
- plugins/observer VX;
- runtime organizativo VX;
- Agent Manager;
- board;
- permisos MCP automáticos desde Dev Team.

Los componentes históricos permanecen versionados únicamente como referencia y para conservar trazabilidad. No forman parte del runtime aprobado.

## MCP

La configuración global de los 13 MCP se considera infraestructura separada. El reset Dev Team Only:

- no modifica `kilo.jsonc`;
- no elimina servidores MCP;
- no autentica/desautentica servidores;
- no concede permisos automáticos de MCP al agente.

Cada tool/MCP que vaya a usar Dev Team será definido y aprobado después.

## Dev Team

El agente aprobado tiene:

- `mode: primary`;
- `displayName: "👥 Dev Team"`;
- color `#8B5CF6`;
- lectura/búsqueda/LSP;
- `edit/write/apply_patch: ask`;
- `bash: ask`;
- `skill: deny`;
- `task: deny`;
- `agent_manager: deny`;
- board denegado;
- ninguna regla MCP namespaced en allow/ask.

## Instalación y limpieza

Usa únicamente:

```powershell
Set-Location 'D:\Proyectos\Kilo-Global-Harness'
git switch main
git pull --ff-only origin main

$script = '.\scripts\Instalar-DevTeam-Only.ps1'

pwsh -NoProfile -File $script -Modo Diagnostico
pwsh -NoProfile -File $script -Modo Simular
pwsh -NoProfile -File $script -Modo Aplicar
pwsh -NoProfile -File $script -Modo Verificar
```

El modo Aplicar crea un backup privado en:

```text
~/.config/kilo-devteam-backups/
```

Después ejecuta `/reload` en Kilo.

## Qué retira del perfil global

Solo recursos VX:

- agentes `vx-*.md` excepto `vx-dev-team.md`;
- comandos `vx-*.md`;
- reglas `vx-*.md`;
- plugin `vx-observer-light.js`;
- skills `vx-*` de `.kilo`, `.agents` y `.kilocode`;
- metadatos/scripts VX del directorio global `harness`;
- bloque administrado `VX-HARNESS-V3` dentro de `AGENTS.md`.

No elimina recursos de terceros.

## Rollback

Usa la carpeta de backup que imprimió Aplicar:

```powershell
pwsh -NoProfile -File $script -Modo Restaurar -BackupFolder 'C:\ruta\al\backup'
```

## Criterio de aceptación visual

Después de `/reload`, dentro del selector personalizado VX debe quedar únicamente:

```text
👥 Dev Team
```

Los modos nativos de Kilo, como Code, Plan, Ask y Debug, permanecen intactos.

## Próxima fase

A partir de este baseline, cada incorporación será incremental:

1. definir necesidad;
2. diseñar agente/skill/tool/workflow;
3. aprobar;
4. implementar;
5. probar;
6. integrar;
7. solo entonces instalarlo globalmente.
