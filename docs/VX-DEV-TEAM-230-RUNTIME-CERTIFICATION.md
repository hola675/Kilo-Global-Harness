# Dev Team 2.3.0 — certificación runtime

**Fecha de cierre:** 2026-11-19  
**Baseline source:** `2.3.0-reviewer-specialist`  
**Estado final:** `PASS_OPERATOR_RUNTIME`  
**Runtime certificado:** Kilo Desktop en Windows  
**Líder visible:** `vx-dev-team`  
**Especialistas:** 10 ocultos/read-only  
**Source de agentes certificado:** `a7efb25a9bdf978d9c03de6cb5d7ba5dd79318df`

## Resultado

La baseline Dev Team 2.3.0 queda certificada en runtime.

| Gate | Resultado |
|---|---|
| Sync source/runtime | 11/11 MATCH |
| Reinicio fresco de Kilo Desktop | PASS |
| Delegación desde `vx-dev-team` | 10/10 PASS |
| Herramientas positivas `glob` / `grep` | 10/10 PASS |
| Contratos de rol | 10/10 PASS |
| Permission enforcement | 10/10 PASS |
| Research MCP documental | 5/5 PASS |
| Architect MCP documental | 5/5 PASS |
| Routing mínimo del líder | PASS |
| Verificación final en disco | PASS |
| Integridad de `kilo.jsonc` | PASS |
| Mutaciones durante probes | NO |
| LSP | opcional, no visible en el host |

El registro estructurado canónico es:

`registry/dev-team-v230-runtime-certification-v1.json`

## Equipo certificado

- `vx-dev-explorer`
- `vx-dev-research`
- `vx-dev-architect`
- `vx-dev-frontend`
- `vx-dev-backend`
- `vx-dev-data`
- `vx-dev-platform`
- `vx-dev-quality`
- `vx-dev-security`
- `vx-dev-reviewer`

## Evidencia funcional

Los diez especialistas fueron delegados como subtareas frescas desde `vx-dev-team`.

Los contratos de rol se validaron contra fixtures versionados y evidencia observable:

- Backend, Data, Platform y Reviewer: fixtures `tests/fixtures/dev-team-v230/`;
- Explorer y Security: fixtures `tests/fixtures/dev-team-v230/`;
- Frontend, Quality, Research y Architect: fixtures históricos reproducibles `tests/fixtures/dev-team-v2r2/`.

Resultado:

`ROLE_CONTRACTS: 10/10 PASS`

Los primeros escenarios sintéticos parciales se conservan solo como evidencia intermedia; no son la base del PASS final.

## MCP de Research y Architect

Research y Architect tienen exactamente cinco tools documentales allowlistadas:

- `context7_resolve-library-id`
- `context7_query-docs`
- `microsoft-learn_microsoft_docs_search`
- `microsoft-learn_microsoft_docs_fetch`
- `microsoft-learn_microsoft_code_sample_search`

Ambos ejecutaron las cinco tools con respuestas válidas:

- Research: `5/5 PASS`;
- Architect: `5/5 PASS`.

Los helpers MCP genéricos permanecieron fuera de su superficie efectiva.

## Permission enforcement

La certificación final usa la semántica verificada del host Kilo.

Para reglas escalares `*: deny`, Kilo deshabilita/filtra la tool de la superficie efectiva. Por ello `NOT_VISIBLE` es evidencia válida de enforcement cuando:

1. la subtarea fresca pertenece al especialista objetivo;
2. la configuración instalada coincide con source;
3. la superficie efectiva del hijo fue observada;
4. la tool denegada no aparece;
5. no se ejecutan mutaciones para probar el deny.

La implementación de Kilo verificada contiene `Permission.disabled()` y `Permission.visibleTools()`; los tests oficiales de task nesting comprueban también la deshabilitación efectiva de tools denegadas en hijos.

Resultado final:

`PERMISSION_ENFORCEMENT: 10/10 PASS`

Para Quality y Security se observaron `glob/grep` y ausencia de todas las tools negativas y MCP documentales. Para Architect se observaron `glob/grep`, ausencia de builtins negativos y helpers MCP genéricos, y visibilidad exacta de las cinco tools documentales autorizadas.

## Routing del líder

El líder respetó selección mínima por incertidumbre:

- API externa → Research;
- formulario + endpoint 500 → Frontend + Backend;
- riesgo cross-tenant → Backend + Security;
- fallo al empaquetar → Platform;
- segunda mirada a refactor no trivial → Reviewer.

Resultado:

`LEADER_ROUTING_CONTRACT: PASS`

No hubo fan-out ritual a los diez especialistas.

## Integridad de instalación

La campaña confirmó:

- `vx-dev-backend-data.md` legacy retirado;
- 11 archivos aprobados (líder + 10 especialistas) coincidentes con source;
- backup reversible válido;
- `kilo.jsonc` preservado;
- configuración MCP sin cambios;
- terceros preservados;
- Git worktree limpio;
- verificador final PASS;
- cero mutaciones runtime durante probes.

## LSP

`lsp: allow` permanece en source como capacidad opcional.

El host actual no expuso LSP durante la certificación. Esto no bloquea el PASS porque la baseline requiere `glob` y `grep`; LSP es opcional.

## Relación con V2-R.2

La certificación histórica V2-R.2 7/7 se conserva como evidencia histórica e incluye al ya supersedido `vx-dev-backend-data`.

El PASS actual **no se hereda** de V2-R.2. Dev Team 2.3.0 fue certificado de nuevo sobre las identidades actuales, incluyendo Backend/Data separados, Platform y Reviewer.

## Regla de recertificación

Este PASS queda ligado al source de agentes:

`a7efb25a9bdf978d9c03de6cb5d7ba5dd79318df`

Debe repetirse la certificación o el subconjunto afectado cuando cambie cualquiera de estos elementos:

- definición de un agente;
- ACL/permisos;
- allowlist MCP;
- routing del líder;
- contrato de rol;
- instalador que gestiona los 11 archivos;
- semántica de permisos/tool visibility del host Kilo;
- mecanismo de creación de subtareas.

Cambios puramente documentales que no alteren esos elementos no invalidan por sí solos la certificación.

## Estado final

```text
DEV_TEAM_SOURCE: 2.3.0-reviewer-specialist
VISIBLE_AGENT: vx-dev-team
HIDDEN_SPECIALISTS: 10
SOURCE_RUNTIME_MATCH: 11/11
ROLE_CONTRACTS: 10/10 PASS
PERMISSION_ENFORCEMENT: 10/10 PASS
RESEARCH_DOCS_MCP: 5/5 PASS
ARCHITECT_DOCS_MCP: 5/5 PASS
LEADER_ROUTING: PASS
KILO_JSONC_INTEGRITY: PASS
RUNTIME_MUTATIONS: NO
RUNTIME_CERTIFICATION: PASS_OPERATOR_RUNTIME
```
