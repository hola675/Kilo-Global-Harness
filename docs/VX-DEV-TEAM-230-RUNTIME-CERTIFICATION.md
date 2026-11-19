# Dev Team 2.3.0 — certificación runtime

**Baseline source:** `2.3.0-reviewer-specialist`  
**Estado actual:** PARTIAL OPERATOR RUNTIME  
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

Los primeros probes usaron escenarios sintéticos sin archivos de implementación. Los cuatro contratos quedaron `PARTIAL`.

Para cerrarlos se crearon fixtures reales:

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

## Estado de certificación completa

La baseline 2.3.0 **no** se considera runtime-certified todavía.

Pendiente:

1. cerrar contratos fixture de Backend/Data/Platform/Reviewer;
2. certificar Explorer/Frontend/Quality/Security en runtime fresco;
3. certificar Research y Architect con sus 5 MCP documentales;
4. validar routing mínimo del líder;
5. confirmar repo/config sin cambios después de toda la campaña.

Solo entonces puede promoverse la baseline de `ACTIVE_SOURCE_BASELINE_RUNTIME_PENDING` a estado runtime certificado.
