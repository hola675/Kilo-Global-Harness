---
name: vx-dev-interaction-motion
description: "Revisa feedback de interacción, transiciones, gestos, animación y continuidad espacial. Usar cuando motion, hover, press, drag, transición de estado o reduced-motion afectan comprensión, respuesta o accesibilidad."
compatibility: "Read-only; no implementa animaciones ni presupone soporte de input no observado."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "interaction-motion"
---

# VX Dev — Interaction Motion

## Protocolo
1. Identificar qué cambio de estado necesita comunicar la interacción.
2. Usar motion para causalidad, orientación o feedback; no como decoración obligatoria.
3. Revisar respuesta inmediata a press/click y continuidad entre estados.
4. Evitar animaciones largas, bloqueantes o que retrasen acciones frecuentes.
5. Revisar hover/focus/active como señales distintas y coherentes.
6. Para drag/gestures, asegurar alternativa y affordance comprensible.
7. Respetar reduced-motion y evitar movimiento esencial sin alternativa.
8. Revisar interrupción, cancelación y transición desde estados parciales.
9. Distinguir problema de motion de problema de rendimiento/jank.

## Salida
`INTERACTION_MODEL`, `FEEDBACK_GAPS`, `MOTION_PURPOSE`, `GESTURE_RISKS`, `REDUCED_MOTION_GAPS`, `TRANSITION_EDGE_CASES`.

## Integración de evidencia/MCP
- Motion y feedback requieren observación runtime cuando sea posible; Playwright/Chrome DevTools son condicionales.
- Registrar viewport, prefers-reduced-motion/theme y estado observado.
- No atribuir jank a motion sin medición; escalar a performance si hace falta.
