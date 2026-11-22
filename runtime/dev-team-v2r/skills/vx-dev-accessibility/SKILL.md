---
name: vx-dev-accessibility
description: "Audita accesibilidad de UI con foco en WCAG 2.2: semántica, teclado, foco, formularios, errores, targets, movimiento, zoom y nombres accesibles. Usar en componentes interactivos, formularios y revisiones pre-release de frontend."
compatibility: "Read-only; automatización no sustituye verificación manual."
metadata:
  version: "1.0.0"
  last_modified: "2026-11-21"
  origin: "vx-dev-original"
  category: "accessibility"
---

# VX Dev — Accessibility Review

## Checklist mínimo
- Preferir elementos HTML nativos antes de ARIA.
- Toda función operable con teclado; sin keyboard traps.
- Foco visible y no oculto.
- Inputs con label/nombre accesible, autocomplete/type/inputmode cuando apliquen.
- Errores asociados al campo y resumen/foco cuando el flujo lo requiera.
- Controles pointer con tamaño/espaciado suficiente; WCAG 2.2 AA usa 24×24 CSS px como mínimo salvo excepciones.
- No depender solo de color para estado.
- Respetar zoom y `prefers-reduced-motion`.
- Icon-only controls con nombre accesible.
- Orden de headings y landmarks coherente.
- Contenido largo/locale/zoom no debe romper operación.

## Evidencia
No afirmar conformidad WCAG completa solo por inspección estática o scanner. Registrar criterio, elemento, severidad, evidencia y validación pendiente.

## Integración de evidencia/MCP
- Source puede sostener semántica prevista, pero teclado, foco, reflow y comportamiento real requieren evidencia runtime cuando sea posible.
- Si Playwright/Chrome DevTools están autorizados, usarlos solo para checks observables y registrar qué se probó.
- Un resultado automatizado no equivale a conformidad WCAG completa.
