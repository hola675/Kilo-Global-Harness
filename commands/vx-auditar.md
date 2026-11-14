---
description: Auditoría de arquitectura, seguridad y calidad sin cambios
agent: plan
---
Revisa el repositorio en modo lectura. Usa Codebase Memory solo si está conectado
y el índice tiene cobertura suficiente. Entrega hallazgos con severidad, ruta,
evidencia concreta, hipótesis y propuesta de remediación. No escribas archivos.

**Control de falsos positivos:** antes de clasificar FAIL, reabre archivo y líneas en el árbol actual; si existe discrepancia entre agentes, usa `/vx-revalidar`. Captura HEAD y referencia local origin/main al principio/final si Git está disponible, sin ejecutar fetch/pull. Distingue una suite declarada de una prueba ejecutada; registra DESCARTADO las sospechas refutadas.
