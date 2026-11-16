---
name: vx-data-contracts
description: "Usar al diseñar o implementar esquemas SQL, APIs de datos, migraciones, D1/SQLite/Postgres o transformaciones que necesiten compatibilidad e integridad; siempre con fixtures sintéticos y rollback propuesto."
---

# VX Data Contracts V0.1

**Objetivo:** estabilidad de datos y migraciones seguras. Para `vx-data-builder`, backend y revisión de Mateo. No concede acceso DB.

## Protocolo de datos
1. **Identificar motor real** y dialecto; versión, tabla/columnas afectadas, claves, cardinalidad y dependencias. No asumir Postgres ni Cloudflare D1.
2. **Contrato:** nombrar esquema actual y futuro, semántica de null, unicidad, foreign keys, índices, tipos y serialización.
3. **Compatibilidad:** revisar lectores/escritores existentes, migraciones hacia delante/atrás, alteraciones de defaults, valores históricos y paginación.
4. **Atomicidad:** transacciones si el motor las soporta, idempotencia de retries y efectos de consistencia eventual (KV ≠ SQL).
5. **Seguridad:** no mostrar credenciales, ni ejecutar DDL en producción, ni copiar datos reales. Si la migración puede perder datos, STOP para revisión humana.
6. **Tests:** fixture sintético de fila mínima, máximo, duplicados, nulls, concurrencia relevante y rollback controlado.
7. **Entrega:** `{schema_before,schema_after,compatibility,migration,rollback,fixture_tests,risks}`; marcar `NO_EJECUTADO` cuando proceda.

El operador autoriza por separado cualquier operación que cambie datos reales; un permiso `bash:ask` no equivale a permiso de migración.
