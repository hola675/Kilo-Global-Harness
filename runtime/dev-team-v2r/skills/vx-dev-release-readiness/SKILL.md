---
name: vx-dev-release-readiness
description: "Evalúa preparación de una entrega antes de merge, release o despliegue. Usar cuando hay que decidir si existe evidencia suficiente de calidad, compatibilidad, migración, rollback, observabilidad y riesgo residual."
compatibility: "Read-only; no despliega, no hace merge y no convierte checks pendientes en PASS."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "release"
---

# VX Dev — Release Readiness

## Frontera
Complementa `vx-dev-platform-delivery`: Platform Delivery mapea el flujo técnico; esta skill produce el gate de salida.

## Protocolo
1. Identificar artefacto, versión, SHA y alcance exacto.
2. Revisar CI, tests, migraciones, compatibilidad y configuración requerida.
3. Verificar plan de rollback o recuperación proporcional al riesgo.
4. Confirmar observabilidad mínima para detectar regresiones post-release.
5. Separar blocking issues de riesgos aceptables y unknowns.
6. Exigir evidencia concreta para cada gate.
7. Considerar dependencias externas, feature flags y cambios irreversibles.
8. No usar "parece listo" como criterio.

## Salida
`RELEASE_SCOPE`, `GATES`, `BLOCKERS`, `ROLLBACK`, `OBSERVABILITY_GATE`, `RESIDUAL_RISK`, `READINESS_STATUS`.

## Integración de evidencia/MCP
- Reutilizar GitHub Actions/PR, Sentry y evidencia de plataforma ya recopilada por los especialistas.
- Cada gate debe apuntar a una evidencia concreta con SHA/run/ID.
- Si falta evidencia, marcar blocker/unknown; no abrir nuevas herramientas salvo gap específico.
