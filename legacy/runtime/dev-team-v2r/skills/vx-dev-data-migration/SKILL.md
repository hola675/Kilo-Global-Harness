---
name: vx-dev-data-migration
description: "Analiza modelos persistentes, invariantes, queries y migraciones seguras. Usar ante cambios de schema, índices, constraints, backfills, retención, consistencia o compatibilidad de datos."
compatibility: "Read-only; no ejecuta DDL/DML ni asume motor de base de datos."
metadata:
  version: "1.0.0"
  last_modified: "2026-11-21"
  origin: "vx-dev-original"
  category: "data"
---

# VX Dev — Data Migration & Integrity

## Protocolo
1. Confirmar motor/dialecto/versión; si falta, declararlo UNKNOWN.
2. Mapear schema actual, relaciones, nulabilidad, unicidad e índices.
3. Definir invariantes de datos antes/después.
4. Revisar datos históricos incompatibles: nulls, duplicados, valores fuera de rango.
5. Separar preflight, backfill, constraint/index y cleanup.
6. Analizar lectores/escritores durante transición y rollback.
7. Considerar transacciones, locks, concurrencia e idempotencia solo según motor real.
8. No afirmar semántica específica de NULL/DDL sin motor confirmado.

## Salida
`DATA_MODEL`, `DATA_INVARIANTS`, `QUERY_IMPACT`, `CONSISTENCY_RISKS`, `MIGRATION_IMPACT`.

## Integración de evidencia/MCP
- Preferir schema/migrations/source locales; usar Codebase Memory/Serena solo para localizar consumidores o dependencias cuando esté autorizado.
- GitHub MCP puede aportar historial/PR/commit relevante sin sustituir verificación del source actual.
- Registrar versión del esquema y SHA para evitar mezclar estados.
