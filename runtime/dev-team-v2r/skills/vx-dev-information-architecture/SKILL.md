---
name: vx-dev-information-architecture
description: "Analiza organización, navegación, jerarquía, búsqueda, etiquetas y findability de productos digitales. Usar cuando usuarios no encuentran contenido, hay demasiadas rutas, menús confusos o un flujo necesita estructura."
compatibility: "Read-only; no decide arquitectura técnica ni sustituye investigación de usuarios faltante."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "information-architecture"
---

# VX Dev — Information Architecture

## Protocolo
1. Identificar tareas principales y objetos del dominio que el usuario reconoce.
2. Mapear entradas, destinos, navegación global/local y retorno.
3. Revisar agrupación, jerarquía y nomenclatura desde el modelo mental del usuario.
4. Detectar duplicados, callejones sin salida y profundidad innecesaria.
5. Evaluar progressive disclosure frente a sobrecarga.
6. Revisar búsqueda, filtros y orden cuando la navegación no escala.
7. Mantener contexto y orientación en flujos profundos.
8. Separar evidencia de usuarios de preferencias internas del equipo.

## Salida
`TASK_MODEL`, `CONTENT_MODEL`, `NAVIGATION_MAP`, `FINDABILITY_GAPS`, `LABELING_GAPS`, `SEARCH_FILTER_GAPS`, `STRUCTURE_OPTIONS`.
