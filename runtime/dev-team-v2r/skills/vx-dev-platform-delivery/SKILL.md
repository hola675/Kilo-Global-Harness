---
name: vx-dev-platform-delivery
description: "Analiza build, runtime, configuración, CI/CD, observabilidad, release y rollback sin desplegar. Usar ante fallos de empaquetado, diferencias de entorno, configuración, pipelines o preparación de entrega."
compatibility: "Read-only; no despliega, ejecuta shell ni cambia infraestructura."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "platform"
---

# VX Dev — Platform Delivery

## Protocolo
1. Mapear source → test → build → package → staging → production según evidencia.
2. Identificar variables/config/bindings requeridos y diferencias de entorno.
3. Separar build-time de runtime configuration.
4. Revisar healthcheck, métricas, logs, tracing y alertas como capacidades observadas/missing.
5. Identificar artefactos, versionado, promotion y rollback.
6. Exigir gates verificables antes de release.
7. No considerar un campo ausente como fallo ejecutado.
8. No asumir que local=production.

## Salida
`RUNTIME_MAP`, `BUILD_AND_RELEASE_FLOW`, `CONFIG_SURFACE`, `ENVIRONMENT_DIFFS`, `FAILURE_MODES`, `DEPLOYMENT_RISKS`, `OBSERVABILITY`.
