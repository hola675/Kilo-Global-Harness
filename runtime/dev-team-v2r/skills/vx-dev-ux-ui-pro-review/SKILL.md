---
name: vx-dev-ux-ui-pro-review
description: "Orquesta una revisión UX/UI integral basada en evidencia cuando el usuario pide evaluar o mejorar una pantalla, flujo o interfaz completa. Usar para combinar jerarquía visual, usabilidad, estados, accesibilidad, responsive, contenido, sistema de diseño y calidad percibida sin inventar evidencia."
compatibility: "Read-only; no renderiza ni ejecuta browser por sí sola, no implementa cambios y no sustituye especialistas estrechos cuando el pedido es específico."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "ux-ui-orchestration"
---

# VX Dev — UX/UI Pro Review

## Objetivo
Producir una revisión senior, priorizada y trazable de una interfaz completa sin caer en puntuaciones decorativas ni recomendaciones genéricas.

## Regla de enrutamiento
Si el pedido es estrecho, preferir la skill especializada correspondiente. Usar esta skill cuando el alcance combine varias dimensiones UX/UI.

## Flujo
1. Entender producto, audiencia, tarea principal y criterio observable de éxito.
2. Inventariar evidencia disponible: código, screenshots, Figma, tokens, Storybook, estados y tests.
3. Separar observación confirmada, hipótesis y evidencia ausente.
4. Revisar en este orden:
   - bloqueos de tarea;
   - accesibilidad;
   - errores, recuperación y estados;
   - arquitectura de información;
   - contenido y microcopy;
   - responsive/resiliencia;
   - sistema de diseño;
   - jerarquía y craft visual;
   - motion e interacción;
   - rendimiento percibido.
5. Aplicar conflicto: intención del usuario > accesibilidad > convención de plataforma > sistema existente > estética.
6. Priorizar por severidad, impacto, confianza y costo aproximado.
7. No afirmar validación visual, de teclado, lector de pantalla o responsive si esa evidencia no fue observada.

## Salida
`SCOPE`, `EVIDENCE_MAP`, `BLOCKERS`, `MAJOR_FINDINGS`, `MINOR_FINDINGS`, `SPECIALIST_HANDOFFS`, `VERIFICATION_GAPS`, `PRIORITIZED_NEXT_ACTIONS`.
