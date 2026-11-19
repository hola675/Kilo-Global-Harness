---
name: vx-dev-responsive-resilience
description: "Revisa resiliencia de UI frente a viewports, zoom, texto largo, localización, temas, teclado, datos densos y redes lentas. Usar cuando una interfaz funciona solo con datos ideales o en un único tamaño."
compatibility: "Read-only; no ejecuta emulación ni screenshots por sí sola."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "responsive-resilience"
---

# VX Dev — Responsive Resilience

## Protocolo
1. Identificar breakpoints y reglas de adaptación existentes.
2. Revisar reflow y prioridades de contenido, no solo reducción proporcional.
3. Considerar ancho estrecho, alto reducido, zoom/text scaling y orientación.
4. Probar conceptualmente contenido mínimo, máximo y extremadamente largo.
5. Revisar localización: expansión de cadenas, RTL y formatos variables.
6. Revisar light/dark/high-contrast cuando apliquen.
7. Identificar colisiones con teclado virtual, overlays, sticky UI y safe areas.
8. Distinguir loading, slow network, broken media y partial data.
9. Evitar truncación que oculte información esencial.

## Salida
`VIEWPORT_RISKS`, `CONTENT_STRESS`, `LOCALE_RISKS`, `THEME_RISKS`, `INPUT_AND_OVERLAY_RISKS`, `NETWORK_STATE_RISKS`, `RESILIENCE_CHECKS`.
