# Dev Team 2.3.0 — certificación runtime

**Baseline source:** `2.3.0-reviewer-specialist`  
**Estado actual:** PARTIAL OPERATOR RUNTIME — functional/runtime contracts 10/10 PASS; permission enforcement pending  
**Runtime objetivo:** Kilo Desktop en Windows  
**Líder visible:** `vx-dev-team`  
**Especialistas:** 10 ocultos/read-only

## Evidencia ya cerrada

El operador confirmó:

- sync en disco: PASS;
- source/runtime: 11/11 archivos MATCH;
- `vx-dev-backend-data.md`: retirado del runtime;
- backup reversible: válido;
- `kilo.jsonc`: integridad preservada;
- reinicio fresco de Kilo Desktop: demostrado;
- `vx-dev-backend`, `vx-dev-data`, `vx-dev-platform` y `vx-dev-reviewer`: delegación fresca 4/4 PASS;
- `glob` y `grep`: 4/4 ejecutados;
- contratos de rol de Backend/Data/Platform/Reviewer contra fixtures reales: 4/4 PASS;
- LSP: no disponible en el host y no bloqueante;
- mutaciones runtime durante probes: ninguna observada.

## Distinción de evidencia de permisos

La certificación 2.3.0 separa dos niveles:

### TOOL_SURFACE_ISOLATION

Una tool marcada como `NOT_VISIBLE` demuestra que no fue expuesta al hijo en esa ejecución.

Esto es evidencia operativa útil de aislamiento de superficie.

### PERMISSION_DENY_ENFORCEMENT

`NOT_VISIBLE` no demuestra por sí solo que el backend de permisos haya rechazado una invocación.

Para afirmar enforcement efectivo se requiere evidencia explícita de rechazo/deny del host o un mecanismo equivalente verificable.

Por tanto, la evidencia actual de los cuatro especialistas nuevos es:

- tool surface isolation: OBSERVADO;
- permission deny enforcement: NOT_PROVEN.

No se convierte `NOT_VISIBLE` en `DENY_EXECUTED`.

## Contratos funcionales

Los primeros probes usaron escenarios sintéticos y quedaron `PARTIAL`. Después se repitieron contra fixtures versionados reales y los cuatro contratos quedaron **4/4 PASS**.

Fixtures ya cerrados:

- Backend: `tests/fixtures/dev-team-v230/backend/`
- Data: `tests/fixtures/dev-team-v230/data/`
- Platform: `tests/fixtures/dev-team-v230/platform/`
- Reviewer: `tests/fixtures/dev-team-v230/reviewer/`

El contrato estructurado está en:

`registry/dev-team-v230-runtime-certification-v1.json`

## Fixtures

### V230-BACKEND-01

Analiza:

- `account_service.ts`
- `accounts_handler.ts`

Debe reconstruir el flujo real de `POST /accounts`, normalización, 201/409/422 y límites entre handler/servicio.

### V230-DATA-01

Analiza:

- `schema.sql`
- `historical_rows.sql`
- `migration.sql`

Debe detectar duplicados históricos, nullable legacy y riesgo de crear un índice UNIQUE sin preflight/backfill.

### V230-PLATFORM-01

Analiza:

- `pipeline.yml`
- `config/staging.json`
- `config/production.json`

Debe mapear pipeline/config y registrar healthcheck/metrics/rollback ausentes como gaps/riesgos, no como fallos ejecutados.

### V230-REVIEWER-01

Compara:

- `before.ts`
- `after.ts`
- `test_tenant_data.ts`

Debe detectar que `tenant_id` cambia del contexto autenticado a input controlado por request y que el test no protege esa propiedad.

## Gate para los cuatro especialistas nuevos

Cada especialista queda `ROLE_CONTRACT: PASS` únicamente si:

1. fue delegado por `vx-dev-team`;
2. `glob` y `grep` ejecutaron;
3. produjo todas sus secciones obligatorias;
4. sus hallazgos se apoyan en rutas fixture;
5. no inventó ejecución ni runtime;
6. no realizó mutaciones.

La ausencia de LSP no bloquea.

El enforcement interno de permisos se reporta en una dimensión separada y no se inventa.

## Segunda tanda de certificación

La segunda tanda quedó cerrada por evidencia del operador:

- Explorer: PASS
- Frontend: PASS
- Quality: PASS
- Security: PASS
- Research: PASS + MCP documental 5/5
- Architect: PASS + MCP documental 5/5
- routing del líder: PASS

Con esto los contratos funcionales/runtime están **10/10 PASS**. La certificación global sigue `PARTIAL` únicamente por el gate independiente de enforcement de permisos.

## Estado de certificación completa

La baseline 2.3.0 todavía **no** se marca runtime-certified.

Cerrado:

- disk sync / restart / config integrity: PASS;
- delegación: 10/10 PASS;
- glob/grep: 10/10 PASS;
- contratos de rol: 10/10 PASS;
- Research MCP: 5/5;
- Architect MCP: 5/5;
- routing del líder: PASS;
- mutaciones durante probes: NO.

Pendiente únicamente:

- enforcement efectivo de permisos de las tools negativas.

### Semántica oficial de Kilo para deny

La documentación oficial define `deny` como bloqueo/deshabilitación completa de una tool. La implementación actual de Kilo contiene `Permission.disabled()` y `Permission.visibleTools()`, que eliminan del catálogo visible las tools con regla efectiva escalar `*: deny`. Los tests oficiales de task nesting también verifican que una tool de hijo denegada aparezca como deshabilitada en la superficie del prompt.

Por tanto, `NOT_VISIBLE` puede aceptarse como evidencia de enforcement cuando:

1. se conoce la regla efectiva escalar `deny` del hijo;
2. la subtarea fue creada realmente con ese agente;
3. la superficie efectiva del hijo fue observada;
4. la tool negativa no aparece.

No se promoverán los seis agentes restantes por inferencia: requieren observación de superficie o evidencia de sesión equivalente.
