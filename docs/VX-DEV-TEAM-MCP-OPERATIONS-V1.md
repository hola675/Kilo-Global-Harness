# Dev Team MCP Operations V1

**Estado:** `SOURCE_READY_RUNTIME_INACTIVE`  
**Nuevas skills:** 8  
**Skills MCP previas:** 2  
**Runtime/ACL/config MCP:** sin cambios

## Objetivo

Convertir la biblioteca MCP del harness en una capacidad operativa coherente para líder y subagentes autorizados. El problema no es solo disponer de MCP, sino saber **cuándo usarlos, cuál elegir, cuánto contexto cargar, qué evidencia conservar y cómo evitar side effects o duplicación**.

## Flujo recomendado

```text
PREGUNTA
  ↓
¿tool nativa/local suficiente?
  ├─ sí → usarla
  └─ no
      ↓
CATALOGAR intención
      ↓
SELECCIONAR servidor
      ↓
INSPECCIONAR tool/schema si hace falta
      ↓
VALIDAR permiso + datos + side effects
      ↓
EJECUTAR mínimo
      ↓
DESTILAR evidencia
      ↓
REUTILIZAR / HANDOFF
```

## Skills nuevas

| Skill | Uso |
|---|---|
| `vx-dev-mcp-capability-routing` | Qué MCP/tool usar y por qué |
| `vx-dev-mcp-server-playbook` | Para qué sirve cada familia MCP |
| `vx-dev-mcp-context-budget` | Evitar tool/context overload |
| `vx-dev-mcp-tool-contract` | Schema, auth, side effects y riesgo |
| `vx-dev-mcp-evidence-ledger` | Procedencia, versión, confianza y contradicciones |
| `vx-dev-mcp-handoff` | Pasar evidencia compacta entre roles |
| `vx-dev-mcp-failure-recovery` | Retry/fallback seguro |
| `vx-dev-mcp-sensitive-data` | Minimización y redacción |

## Biblioteca conocida

El playbook cubre las 13 familias registradas en la matriz histórica del harness:

Context7, Microsoft Learn, Serena, Codebase Memory, GitHub, Cloudflare API, Playwright, Chrome DevTools, Sentry, Snyk, Postman, IDA e ImageGen.

La lista sirve como **mapa de propósito**, no como afirmación de disponibilidad. Cada sesión debe confirmar qué tools ve realmente el agente.

## Cuándo usar cada tipo

- **Context7 / Microsoft Learn:** documentación oficial/versionada.
- **Serena / Codebase Memory:** estructura, símbolos, referencias, arquitectura y cambios del código.
- **GitHub:** estado remoto del repo, commits, PR, issues, Actions.
- **Playwright / Chrome DevTools:** comportamiento runtime real de UI/browser.
- **Sentry:** errores, traces, logs y métricas de producción.
- **Snyk:** salud y análisis de dependencias/código/IaC cuando esté permitido.
- **Postman:** catálogo/workspaces/colecciones y contexto de APIs.
- **Cloudflare:** documentación/API Cloudflare, separando docs/search de ejecución.
- **IDA:** reverse engineering cuando el rol/proyecto lo requiera.
- **ImageGen:** creación/edición visual, no análisis documental.

## Contexto

Las prácticas actuales del MCP recomiendan progressive discovery cuando el catálogo de tools crece: catálogo ligero → inspección de la tool elegida → ejecución. El harness debe evitar meter todos los schemas en contexto cuando no hacen falta.

## Límites

Estas skills no:
- habilitan servidores;
- cambian scopes;
- editan `kilo.jsonc`;
- permiten wildcards;
- convierten readOnlyHint en garantía;
- autorizan al subagente a hacer algo que su ACL no permita.

## Activación futura

Antes de asignarlas a todos los roles MCP:
1. capturar inventario runtime real por agente;
2. actualizar la matriz rol→servidor→tool;
3. identificar tools compartidas líder/subagentes;
4. ejecutar evals de routing y false positives;
5. aprobar ACL de skill exacta;
6. recertificar uso MCP sin modificar permisos de tools.
