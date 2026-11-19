---
name: vx-dev-frontend-ux
description: "Revisa flujos frontend y calidad UX/UI: jerarquía, responsive, interacción, navegación, contenido, performance percibida y coherencia visual. Usar al evaluar pantallas, componentes, formularios o flujos de usuario antes de implementar o revisar cambios."
compatibility: "Read-only; no genera diseño gráfico ni ejecuta navegador."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "frontend-ux"
---

# VX Dev — Frontend UX Review

## Revisión
1. Identificar usuario, tarea principal y camino feliz.
2. Mapear estados: idle, loading, empty, success, validation, error, disabled y retry.
3. Verificar jerarquía visual, agrupación, alineación, densidad y consistencia con el sistema existente.
4. Revisar responsive en móvil, laptop y ancho amplio; contemplar texto largo, zoom y overflow.
5. Mantener navegación semántica y URL cuando el estado deba ser enlazable/recuperable.
6. Exigir feedback inmediato para acciones y recuperación ante errores.
7. Revisar rendimiento percibido: evitar layout shifts, trabajo innecesario y cargas pesadas; medir antes de optimizar.
8. Separar defecto observable de preferencia estética.

## Evidencia
Para cada hallazgo: `{element_or_flow,observed,impact,evidence,recommendation,confidence}`.

Referencias: W3C WCAG 2.2, web.dev Core Web Vitals, USWDS, Vercel Web Interface Guidelines.

## Integración de evidencia/MCP
- Código estático no demuestra comportamiento visual/runtime.
- Si está autorizado y hace falta evidencia real, usar Playwright/Chrome DevTools para estados, responsive, consola o red; aplicar `vx-dev-mcp-sensitive-data` en sesiones autenticadas.
- Si no hay browser MCP disponible, marcar la revisión visual/interactiva como no verificada.
