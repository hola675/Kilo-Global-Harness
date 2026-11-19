---
name: vx-dev-forms-ux
description: "Analiza formularios, validación, envío y recuperación de errores para reducir fricción y ambigüedad. Usar ante inputs, formularios largos, errores de validación, submit asíncrono, pasos multi-stage o acciones sensibles."
compatibility: "Read-only; no cambia reglas de negocio ni garantiza idempotencia backend."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "forms-ux"
---

# VX Dev — Forms UX

## Protocolo
1. Confirmar objetivo del formulario y datos estrictamente necesarios.
2. Revisar labels persistentes, ayudas, formatos y ejemplos.
3. Distinguir validación preventiva, inline, on-submit y server-side.
4. Exigir mensajes que expliquen qué ocurrió y cómo corregirlo.
5. Revisar orden de foco, agrupación, autofill y tipos de input.
6. Revisar estados idle, invalid, pending, success, partial failure y retry.
7. Evitar doble submit y comunicar progreso sin confundir disabled con loading.
8. Para acciones destructivas, nombrar consecuencia y preferir undo cuando sea seguro/reversible.
9. Separar UX de garantías técnicas como idempotencia, autorización o atomicidad.

## Salida
`FORM_GOAL`, `FIELD_FRICTION`, `VALIDATION_MODEL`, `ERROR_RECOVERY`, `SUBMIT_STATES`, `ACCESSIBILITY_GAPS`, `BACKEND_DEPENDENCIES`.
