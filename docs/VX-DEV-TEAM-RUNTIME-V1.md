# VX Dev Team Runtime V1

**Estado:** ACTIVE_V1 en código  
**Fecha:** 2026-11-17  
**Agente primario:** `vx-dev-team`  
**Nombre visible:** `👥 Dev Team`  
**Color:** `#8B5CF6`

## Identidad visual

Kilo soporta oficialmente `displayName` y `color` para agentes personalizados. La versión actual no expone un campo oficial para sustituir el glifo izquierdo del selector por un SVG/ícono arbitrario.

Por eso V1 usa una estrategia compatible y verificable:

- ID interno estable: `vx-dev-team`;
- display name: `👥 Dev Team`;
- color propio: `#8B5CF6`;
- sin campo `icon:` inventado.

La UI debe mostrar el emoji dentro del nombre visible y aplicar el color del agente donde Kilo lo represente.

## Instalación global

El instalador general ya copia todos los archivos `agents/*.md` al perfil global, por lo que `agents/vx-dev-team.md` se instala en:

```text
~/.config/kilo/agents/vx-dev-team.md
```

No se modifica `kilo.jsonc` y no se tocan los 13 MCP.

## Runtime V1

`vx-dev-team` es `mode: primary`, por tanto debe aparecer en el selector principal después de instalar y recargar Kilo.

Puede delegar mediante `task` a:

- vx-researcher
- vx-inspector
- vx-security-reviewer
- vx-test-analyst
- vx-frontend-adviser
- vx-workers-adviser
- vx-frontend-builder
- vx-backend-builder
- vx-qa-builder
- vx-data-builder
- vx-docs-builder

Los builders conservan sus propios permisos. Dev Team no convierte `ask` en `allow`.

## Escritura y shell

El Team Lead tiene:

- `edit: ask`
- `write: ask`
- `apply_patch: ask`
- `bash: ask`
- `agent_manager: deny` en V1
- `external_directory: deny`

Esto mantiene la interacción visible en el Permission Dock para cambios con efectos.

## MCP

V1 aplica una política conservadora a nivel de servidor:

### Allow

- `context7_*`
- `microsoft-learn_*`

### Ask

- `codebase-memory_*`
- `serena_*`
- `github_*`
- `playwright_*`
- `chrome-devtools_*`
- `postman_*`
- `snyk_*`
- `sentry_*`
- `cloudflare-api_*`
- `imagegen_*`
- `ida_*`

La matriz detallada por rol sigue en `registry/vx-dev-team-mcp-matrix-v1.json`. La siguiente refinación debe enumerar tools efectivas de cada MCP y separar lectura/mutación/destructivo tool-by-tool.

## Invariantes

- 1 escritor efectivo por worktree.
- hasta 3 lectores en paralelo.
- merge a main requiere autorización humana.
- deploy/DNS/IAM/infra/DDL destructivo requiere autorización humana.
- no autoevaluación como único revisor.
- no instalación silenciosa de skills/MCP.
- no alteración de AutoApprove.
- no secretos en prompts, logs o repositorio.

## Smoke test local esperado

Después del merge e instalación:

```powershell
Set-Location 'D:\Proyectos\Kilo-Global-Harness'
git switch main
git pull --ff-only origin main

$script = '.\scripts\Instalar-Kilo-Global-Harness.ps1'
pwsh -NoProfile -File $script -Modo Diagnostico
pwsh -NoProfile -File $script -Modo Simular
pwsh -NoProfile -File $script -Modo Aplicar
pwsh -NoProfile -File $script -Modo Verificar
```

Luego reiniciar/recargar Kilo y confirmar visualmente:

1. aparece `👥 Dev Team` en el selector;
2. su color es distinto;
3. puede delegar una tarea read-only a `vx-researcher`;
4. una acción `edit` solicita aprobación;
5. Context7 o Microsoft Learn no requieren aprobación adicional del agente;
6. un MCP con efectos como GitHub/Serena/Cloudflare solicita aprobación.

La prueba visual del selector y del Permission Dock es evidencia runtime; CI solo valida archivos y contratos.
