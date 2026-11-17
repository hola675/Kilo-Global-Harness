# Dev Team MCP Read-Only Matrix V1 — propuesta de mínimo privilegio

**Fecha:** 2026-11-17  
**Estado:** PROPOSAL_ONLY_NOT_ACTIVE  
**Baseline objetivo:** Dev Team V2-R.2  
**Activa permisos:** NO  
**Modifica `kilo.jsonc`:** NO  
**Modifica los 13 MCP:** NO

## Objetivo

Diseñar la futura integración MCP de Dev Team sin romper el aislamiento ya certificado de los siete subagentes.

La unidad de autorización es la **tool exacta**, no el servidor completo.

Regla base:

```text
UNKNOWN       → DENY
MIXED         → DENY
MUTABLE       → DENY
ADMIN/DELETE  → DENY
READ_SENSITIVE→ revisar y probar antes de permitir
READ_SAFE     → candidato, nunca activación automática
```

En Kilo, las tools MCP se permissionan por su ID efectivo. El patrón observado en el código actual es:

```text
<server-id>_<tool-name>
```

Por ejemplo:

```text
context7_query-docs
microsoft-learn_microsoft_docs_search
serena_find_symbol
```

Antes de activar una sola entrada, el ID efectivo debe confirmarse en el runtime del usuario.

## Resultado de la investigación

### Wave 1 propuesta — documentación externa

Es la única ola que recomiendo preparar para una futura activación inmediata después de un snapshot de inventario.

**Research**

```text
context7_resolve-library-id
context7_query-docs
microsoft-learn_microsoft_docs_search
microsoft-learn_microsoft_docs_fetch
microsoft-learn_microsoft_code_sample_search
```

**Architect**

Las mismas cinco tools.

Motivo: son consultas de documentación y ejemplos oficiales/públicos, sin semántica de mutación en las superficies verificadas.

No se activa `context7_query-code`: esa superficie depende de preview/configuración y no se asume disponible.

## Wave 2 propuesta — inteligencia de código

### Serena

Candidatos para Explorer/Architect:

```text
serena_get_symbols_overview
serena_find_symbol
serena_find_referencing_symbols
serena_find_declaration
serena_find_implementations
```

Estas operaciones aportan navegación semántica que actualmente no ofrece el host porque la tool LSP nativa de Kilo está deshabilitada.

Se mantienen DENY inicialmente:

- `serena_read_file`: permitirla anularía conceptualmente el aislamiento conseguido con `read: deny`.
- `serena_search_for_pattern`: `grep` nativo ya cubre búsqueda textual.
- tools de memoria: pueden exponer o modificar memoria persistente.
- cualquier editor simbólico o de archivos.

### Codebase Memory

Candidatos posteriores:

- `search_graph`
- `trace_path`
- `get_code_snippet`
- `get_file_outline`
- `get_graph_schema`
- `compare_graphs`
- `get_architecture`
- `search_code`
- `index_status`
- `check_index_coverage`
- `detect_changes`

Estos accesos se clasifican mayormente como **READ_SENSITIVE** porque consultan código/estructura local que puede ser privado.

No se permiten todavía:

- `query_graph`: semántica efectiva a verificar antes de clasificarla como no mutable.
- `index_repository`: cambia índice persistente.
- `delete_project`: destructiva.
- `manage_adr`: tool mixta de lectura/escritura.
- `ingest_traces`: modifica grafo/evidencia persistente.

## Servidores diferidos

### GitHub

El servidor oficial soporta modo read-only y allowlist exacta de tools, pero la instancia global actual no está dedicada exclusivamente a lectura.

Candidatos futuros incluyen:

- `get_file_contents`
- `search_code`
- `get_file_blame`
- `get_repository_tree`
- `list_branches`
- `list_tags`
- `list_commits`
- `get_commit`
- `search_commits`
- `issue_read`
- `pull_request_read`
- `actions_list`
- `actions_get`
- `get_job_logs`

Son **READ_SENSITIVE**: pueden exponer repositorios privados, issues, PRs y logs.

No se concede `github_*`.

### Cloudflare API

Superficie verificada:

| Tool | Clase | Decisión V1 |
|---|---|---|
| `docs` | READ_SAFE | candidato futuro |
| `search` | READ_SAFE | candidato futuro |
| `whoami` | READ_SENSITIVE | deny inicial |
| `execute` | MIXED | DENY |

`execute` puede llamar endpoints Cloudflare y por ello no puede tratarse como read-only.

### Playwright

Aunque existen tools orientadas a observación como snapshots, consola y red, varias pueden escribir archivos mediante parámetros y todas operan sobre una sesión de navegador potencialmente autenticada.

Resultado V1: **DENY completo** hasta disponer de wrapper/contrato que restrinja parámetros y sesión.

### Chrome DevTools

Tiene tools de consulta útiles, pero también JS arbitrario, navegación, input, extensiones, PWA, WebAuthn y otras mutaciones. Algunas consultas pueden revelar cookies, headers, storage o sesiones activas.

Resultado V1: **DENY completo** hasta una capa segura de parámetros.

### Snyk

Los scans son conceptualmente análisis, pero pueden enviar código/dependencias al servicio y algunos flujos pueden ejecutar herramientas del ecosistema local.

`snyk_version`, `snyk_auth_status` y consultas de salud de paquetes son menos riesgosas, pero no aportan suficiente valor para abrir el servidor a los hijos todavía.

Resultado V1: DENY.

### Postman

El endpoint configurado es `minimal`, pero “minimal” no significa read-only. La superficie es generada/dinámica y el propio producto incluye operaciones de modificación.

Candidatos observados como lectura:

- `getEnabledTools`
- `getWorkspaces`
- `searchPostmanElements`

Resultado V1: DENY hasta capturar la lista real de tools del endpoint OAuth actual.

### Sentry

Consultas como organizaciones, proyectos, issues, logs, trazas, métricas y perfiles son lectura pero contienen **telemetría de producción**.

Además existen `update_issue` y un gateway `execute_sentry_tool` que puede alcanzar tools mutables.

Resultado V1: DENY.

### IDA

Superficie actual verificada:

| Tool | Clase | Decisión |
|---|---|---|
| `reference` | READ_SAFE | deny inicial |
| `list_databases` | READ_SENSITIVE | deny inicial |
| `open_database` | MUTABLE/local side effect | DENY |
| `execute_python` | MIXED/arbitrary | DENY |
| `save_database` | MUTABLE | DENY |
| `close_database` | MUTABLE/session | DENY |

No existe todavía un especialista reverse aprobado en V2-R.2.

### ImageGen

Generar/editar/remover fondo consume recursos y escribe archivos; login cambia estado de autenticación.

Resultado V1: DENY completo.

## Principio importante: tool-level, no server-level

Nunca usar:

```text
github_*
serena_*
playwright_*
cloudflare-api_*
```

como allow para subagentes.

Una sola wildcard volvería a introducir exactamente el riesgo que V2-R.2 eliminó.

## Activación futura de Wave 1

Antes de cambiar un agente:

1. capturar inventario visible de tools MCP desde Research y Architect;
2. no invocar ninguna;
3. comparar IDs exactos con la propuesta;
4. si aparece una tool inesperada, mantener DENY;
5. aplicar únicamente las cinco entradas exactas;
6. verificar que `kilo.jsonc` no cambió;
7. `/reload`;
8. repetir inventario negativo/positivo;
9. hacer smoke de documentación;
10. obtener aprobación humana antes de mantener el cambio.

## Fuentes técnicas verificadas

La clasificación se construyó contra las fuentes oficiales/actuales de:

- Kilo Code — resolución y permissioning de tools MCP;
- Context7;
- Microsoft Learn MCP;
- GitHub MCP Server;
- Cloudflare MCP;
- Playwright MCP;
- Chrome DevTools MCP;
- Serena;
- Codebase Memory MCP;
- Hex-Rays IDA MCP;
- Postman MCP;
- Sentry MCP/toolkit;
- Snyk CLI MCP;
- ImageGen MCP usado por el pack.

El registro estructurado canónico de esta propuesta es:

`registry/dev-team-mcp-readonly-matrix-v1.proposal.json`

Hasta que exista una aprobación/implementación posterior, esta matriz **no cambia el runtime**.
