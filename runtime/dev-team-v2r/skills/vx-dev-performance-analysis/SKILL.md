---
name: vx-dev-performance-analysis
description: "Diseña y revisa análisis de rendimiento basado en métricas, presupuesto y comparación reproducible. Usar ante latencia, throughput, consumo de recursos, regresiones de rendimiento o capacidad, sin ejecutar benchmarks."
compatibility: "Read-only; no ejecuta benchmarks ni optimiza código por sí sola."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "performance"
---

# VX Dev — Performance Analysis

## Protocolo
1. Definir métrica primaria y unidad antes de comparar.
2. Registrar baseline, carga, dataset, entorno y versión.
3. Separar latencia, throughput, CPU, memoria, I/O, red y colas.
4. Evitar conclusiones desde una única muestra o entorno no comparable.
5. Identificar percentiles relevantes y no depender solo de promedios.
6. Distinguir degradación funcional de saturación de capacidad.
7. Diseñar prueba mínima reproducible y criterio de regresión.
8. Relacionar el presupuesto de rendimiento con comportamiento observable.

## Salida
`PERFORMANCE_QUESTION`, `BASELINE`, `METRICS`, `CONTROLLED_VARIABLES`, `REGRESSION_CRITERIA`, `MEASUREMENT_PLAN`, `UNKNOWN_CONFOUNDERS`.
