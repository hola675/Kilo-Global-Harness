---
name: vx-dev-sql-performance
description: "Analiza rendimiento de consultas SQL, planes, índices, bloqueos y patrones de acceso sin modificar la base de datos. Usar ante queries lentas, scans inesperados, N+1, waits, locks o dudas sobre índices."
compatibility: "Read-only; no crea índices, no ejecuta DDL y no afirma mejoras sin medición."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "data-performance"
---

# VX Dev — SQL Performance

## Protocolo
1. Identificar query real o patrón normalizado y frecuencia.
2. Revisar filtros, joins, ordenación, límites y cardinalidades esperadas.
3. Interpretar plan disponible sin asumir que estimado = observado.
4. Buscar scans, sorts, spills, waits, locks y multiplicación de filas.
5. Revisar selectividad y orden de columnas de índices existentes.
6. Detectar N+1 y round-trips innecesarios desde la capa de acceso.
7. Separar mejora de query, schema, índice y capacidad.
8. Exigir medición antes/después para afirmar mejora.

## Salida
`QUERY_SHAPE`, `PLAN_FINDINGS`, `INDEX_FINDINGS`, `LOCKING_AND_WAITS`, `APP_ACCESS_PATTERN`, `HYPOTHESES`, `MEASUREMENT_REQUIRED`.
