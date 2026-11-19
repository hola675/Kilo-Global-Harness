---
name: vx-dev-ui-state-system
description: "Diseña y revisa estados de componentes y flujos UI: loading, empty, error, success, disabled, optimistic, undo y recuperación. Usar cuando una interfaz funciona técnicamente pero faltan estados, feedback o consistencia de interacción."
compatibility: "Read-only; complementa frontend UX y accesibilidad."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "ui-state"
---

# VX Dev — UI State System

## Modelo
Para cada acción o componente definir:
- estado inicial;
- trigger;
- pending/loading;
- success;
- empty;
- validation error;
- server/network error;
- retry/recovery;
- destructive confirmation o undo;
- disabled/read-only;
- stale/partial data si aplica.

## Reglas
1. No ocultar la etiqueta principal de un botón durante loading sin conservar contexto.
2. Evitar doble submit mientras la operación está en curso.
3. Errores deben explicar qué pasó y siguiente acción.
4. Empty state debe ofrecer siguiente paso cuando exista.
5. Optimistic UI exige reconciliación y rollback/undo.
6. Skeleton debe aproximar el layout final para reducir CLS.
7. Estado visual debe tener equivalente semántico/accesible.

## Salida
`STATE_MODEL`, transiciones, gaps, recovery path y riesgos.
