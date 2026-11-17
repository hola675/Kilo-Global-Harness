# Dev Team V2-R.2 — líder único + especialistas ocultos con capacidades adaptativas

**Fecha:** 2026-11-17  
**Estado:** ACTIVE APPROVED BASELINE · V2-R.2  
**Primario visible:** `👥 Dev Team`  
**Especialistas ocultos:** 7  
**Mutaciones de subagentes:** DENY  
**MCP de subagentes:** NO EXPUESTO en esta fase

## Objetivo

V2-R introduce la primera capa multiagente aprobada del Harness sin volver a llenar el selector principal.

El operador interactúa únicamente con `👥 Dev Team`. El líder puede delegar análisis concretos a especialistas ocultos mediante `task`. Los hijos son no interactivos y trabajan en contexto aislado.

## Equipo V2-R

| ID | Rol | Visible | Escritura | Shell | Delegación | MCP |
|---|---|---:|---:|---:|---:|---:|
| `vx-dev-team` | Team Lead / Technical Lead | sí | ask | ask | allowlist | ninguno automático |
| `vx-dev-explorer` | codebase exploration | no | deny | deny | deny | deny |
| `vx-dev-architect` | architecture/contracts | no | deny | deny | deny | deny |
| `vx-dev-frontend` | frontend analysis | no | deny | deny | deny | deny |
| `vx-dev-backend-data` | backend/data analysis | no | deny | deny | deny | deny |
| `vx-dev-quality` | quality/test planning | no | deny | deny | deny | deny |
| `vx-dev-security` | security analysis | no | deny | deny | deny | deny |
| `vx-dev-research` | local repository research | no | deny | deny | deny | deny |

Los especialistas se definen en `runtime/dev-team-v2r/agents/` para mantenerlos separados del árbol legacy de agentes VX.

## Patrón de orquestación

```text
Usuario
  │
  ▼
👥 Dev Team
  │
  ├── simple  → 0-1 especialista
  ├── media   → 1-2 especialistas
  └── compleja→ 2-4 especialistas
                  │
                  ▼
          resultados estructurados
                  │
                  ▼
             👥 Dev Team
                  │
             síntesis/decisión
```

No existe comunicación lateral entre hijos. No hay Swarm, Board ni Agent Manager.

## Profundidad

Solo una profundidad:

```text
Usuario → Dev Team → Subagente
```

Los hijos tienen `task: deny`.

## Contrato de delegación

El líder envía:

- `objective`
- `scope`
- `questions`
- `allowed_paths`
- `known_facts`
- `unknowns`
- `evidence_required`
- `exclusions`
- `output_format`
- `budget`

Los hijos devuelven:

- `STATUS`
- `FINDINGS`
- `EVIDENCE`
- `RISKS`
- `RECOMMENDATION`
- `UNKNOWNS`

No se devuelve el transcript completo como contrato normal.

## Permisos de hijos

Requeridos:

- `glob`
- `grep`

Opcional según el host:

- `lsp`

Denegados:

- `read`
- `edit`
- `write`
- `apply_patch`
- `bash`
- `task`
- `skill`
- `agent_manager`
- `external_directory`
- `board_read`
- `board_post`
- herramientas MCP namespaced

### Nota de compatibilidad Kilo

La certificación runtime V2-R original detectó que Kilo exponía `list_mcp_resources`, `list_mcp_resource_templates` y `read_mcp_resource` a los hijos.

La causa está en Kilo actual: esas tres tools genéricas se clasifican internamente bajo el permiso `read`. Con `read: allow`, permanecen visibles aunque las tools MCP namespaced estén denegadas.

V2-R.1 priorizó aislamiento MCP estricto:

```yaml
read: deny
glob: allow
grep: allow
lsp: allow
```

Así los especialistas mantienen inspección local no mutable, pero pierden la herramienta `read` directa y, con ella, la exposición de los recursos MCP genéricos.

### LSP adaptativo en V2-R.2

La segunda certificación runtime confirmó que `glob` y `grep` están disponibles, mientras que `lsp` no aparece en el inventario del host actual.

Esto no es un fallo de ACL. En Kilo actual, la tool `lsp` se registra únicamente cuando el host habilita la bandera experimental `KILO_EXPERIMENTAL_LSP_TOOL`. Por tanto:

- `lsp: allow` significa "permitirla si existe";
- no significa "forzar que Kilo la registre";
- V2-R.2 exige `glob` + `grep`;
- `lsp` es una capacidad opcional;
- no se activa ninguna bandera experimental global automáticamente.

## Instalación

El instalador canónico continúa siendo:

```powershell
$script = '.\scripts\Instalar-DevTeam-Only.ps1'
pwsh -NoProfile -File $script -Modo Diagnostico
pwsh -NoProfile -File $script -Modo Simular
pwsh -NoProfile -File $script -Modo Aplicar
pwsh -NoProfile -File $script -Modo Verificar
```

La semántica de “Only” es: **Dev Team es el único modo personalizado visible aprobado**. Los siete especialistas son internos y `hidden: true`.

## Seguridad

El instalador:

- preserva `kilo.jsonc` byte-a-byte;
- no modifica ni autentica los 13 MCP;
- preserva agentes/skills de terceros;
- retira agentes VX legacy no aprobados;
- crea backup reversible;
- puede restaurar backups V1 y V2-R.

## Evidencia requerida antes de V2-W

Antes de permitir cualquier subagente escritor:

1. Kilo debe mostrar solo `👥 Dev Team` en el selector;
2. el líder debe delegar exitosamente a al menos Explorer y Architect;
3. un hijo debe ser incapaz de editar y ejecutar shell;
4. el padre debe recibir solo el resultado estructurado;
5. una tarea simple no debe invocar agentes innecesarios;
6. una tarea compleja debe mantener máximo 2-4 especialistas salvo excepción explícita;
7. no debe cambiar `kilo.jsonc` ni la lista de MCP.

## Próxima fase

Después del smoke real V2-R.2:

- medir routing del líder;
- ajustar descripciones/prompts;
- conectar MCP read-only tool-by-tool donde aporte valor;
- mantener mutaciones denegadas;
- solo después evaluar builders aislados/worktrees como V2-W.
