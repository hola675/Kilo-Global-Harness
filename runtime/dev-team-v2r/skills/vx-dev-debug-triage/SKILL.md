---
name: vx-dev-debug-triage
description: "Diagnostica bugs, regresiones y fallos de build/integración antes de proponer cambios. Usar cuando existe un síntoma reproducible, error observado, test fallido o diferencia entre entornos."
compatibility: "Read-only; no ejecuta shell ni modifica código."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "debugging"
---

# VX Dev — Debug Triage

## Protocolo
1. Capturar observado vs esperado, versión, entrada y entorno.
2. Reducir el problema a la mínima superficie verificable.
3. Formular máximo tres hipótesis falsables.
4. Rastrear capas: entrada → contrato → lógica → IO/dependencia → salida.
5. Separar causa, correlación y síntoma.
6. Buscar regresión temporal/diff cuando exista evidencia.
7. Proponer la prueba más barata que discrimine entre hipótesis.
8. Solo después proponer corrección mínima y test de regresión.

## Estados
`REPRODUCED`, `NOT_REPRODUCED`, `ROOT_CAUSE_SUPPORTED`, `HYPOTHESIS`, `UNKNOWN`.

No repetir parches sin nueva evidencia ni declarar causa raíz desde un stacktrace parcial.

## Integración de evidencia/MCP
- Elegir la fuente por hipótesis: source→Serena/Codebase Memory, cambios→GitHub, runtime→Sentry, UI real→Playwright/Chrome DevTools.
- No consultar todas las fuentes a la vez; cada llamada debe falsar o sostener una hipótesis concreta.
- Tras obtener evidencia, producir reuse keys y handoff compacto.
