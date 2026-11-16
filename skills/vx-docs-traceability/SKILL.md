---
name: vx-docs-traceability
description: "Usar al escribir documentación técnica, README, ADR, changelog, contratos y manuales para alinear texto con código, pruebas, decisiones y versiones reales; no inventar funciones implementadas."
---

# VX Docs Traceability V0.1

**Objetivo:** documentación que distingue proyecto, código integrado, instalación global, ejecución comprobada y propuesta. Para `vx-docs-builder`, Yoan y Sofía.

## Regla de procedencia
- **HECHO:** ruta/símbolo/commit o salida real demostrada.
- **DECLARADO:** descripción de agente/skill sin pruebas.
- **PROPUESTO:** diseño/version futura sin implementación.
- **NO_VERIFICADO:** falta fuente verificable o la fuente es externa no probada.
- **NO_EJECUTADO:** prueba/comando descrito pero sin ejecución.
- **PASS:** resultado de una ejecución identificada (comando, runner, SHA y alcance).

## Proceso
1. Identificar versión/fuente `main` frente a PR y runtime real; no concluir que un commit está instalado.
2. Consultar rutas de documentos y código existente, mantener título, convenciones, changelog y enlaces estables.
3. Actualizar solo secciones afectadas, dejando decisiones y riesgos pendientes visibles.
4. Citar rutas, IDs de versión y tests, sin exponer secretos ni datos de clientes; usar ejemplos sintéticos.
5. Comprobar enlaces internos y referencias de archivos con un lector/runner autorizado.
6. Entregar `{files_updated,source_evidence,assumptions,acceptance_status}` con revisión independiente.

Una documentación mejor no demuestra automáticamente mejora de competencia ni autoriza publicar.
