---
name: vx-dev-codebase-investigation
description: "Mapea un codebase con evidencia: entrypoints, símbolos, consumidores, dependencias, tests e impacto. Usar cuando no está claro dónde vive un comportamiento, qué archivos toca un cambio o qué referencias deben revisarse antes de implementar."
compatibility: "Read-only; diseñado para vx-dev-explorer con glob/grep y LSP opcional."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "discovery"
---

# VX Dev — Codebase Investigation

## Protocolo
1. Anclar commit/árbol si está disponible.
2. Encontrar entrypoint y símbolos concretos.
3. Seguir referencias hacia consumidores, contratos y tests.
4. Separar dependencia directa de coincidencia textual.
5. Clasificar impacto DIRECT/INDIRECT/POSSIBLE/OUT_OF_SCOPE.
6. Usar LSP solo si el host lo expone; su ausencia no bloquea.
7. Registrar rutas y líneas/patrones de evidencia.
8. Detenerse antes de diseñar solución salvo que se pida explícitamente.

## Salida
`CODE_MAP`, `IMPACT_SURFACE`, hallazgos, evidencia, riesgos, unknowns y handoff.

No escribir, ejecutar shell ni convertir una búsqueda incompleta en certeza.
