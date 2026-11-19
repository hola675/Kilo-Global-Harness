---
name: vx-dev-data-visualization
description: "Revisa dashboards, charts y visualizaciones para elegir representación, escala, comparación, densidad y accesibilidad correctas. Usar cuando la UI comunica métricas, tendencias, distribuciones o relaciones mediante gráficos."
compatibility: "Read-only; no inventa datos ni declara significancia estadística sin evidencia."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "data-visualization"
---

# VX Dev — Data Visualization

## Protocolo
1. Definir pregunta que la visualización debe responder.
2. Elegir forma según tarea: comparar, tendencia, composición, distribución, relación o geografía.
3. Revisar escala, cero, dominios, intervalos y unidades.
4. Evitar dual axes o codificaciones que dificulten comparación salvo justificación.
5. Revisar densidad, orden visual y jerarquía en dashboards.
6. No depender solo de color; añadir etiquetas, patrones o estructura cuando sea necesario.
7. Proporcionar valores accesibles/tabulares cuando la gráfica no sea suficiente.
8. Revisar estados sin datos, datos parciales, loading y error.
9. Distinguir correlación, causalidad y significancia.

## Salida
`ANALYTIC_QUESTION`, `CHART_FIT`, `SCALE_RISKS`, `DENSITY_RISKS`, `ACCESSIBILITY_GAPS`, `STATE_GAPS`, `ALTERNATIVE_REPRESENTATION`.

## Integración de evidencia/MCP
- Browser evidence puede confirmar escalas, labels, responsive y estados; source puede confirmar configuración.
- No enviar datasets sensibles completos si basta con muestra sintética o metadata.
- Un gráfico renderizado no demuestra corrección de los datos subyacentes.
