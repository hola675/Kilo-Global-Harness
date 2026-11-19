---
name: vx-dev-visual-craft
description: "Critica jerarquía visual, composición, tipografía, color, spacing, superficies y distintividad de una interfaz. Usar cuando la UI funciona pero se percibe genérica, amateur, plana, ruidosa o incoherente con la marca."
compatibility: "Read-only; la estética no puede anular accesibilidad, usabilidad ni el design system existente."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "visual-craft"
---

# VX Dev — Visual Craft

## Protocolo
1. Identificar foco principal, orden de lectura y acción primaria.
2. Revisar contraste de escala, peso, spacing y agrupación antes de efectos decorativos.
3. Evaluar tipografía por rol, ritmo, longitud de línea y densidad.
4. Revisar color por intención semántica y consistencia de tema.
5. Usar tone, border y shadow con funciones diferenciadas.
6. Detectar repetición de cards, radios, sombras o gradientes sin jerarquía.
7. Buscar composición y detalles distintivos coherentes con producto/brand, no novedad gratuita.
8. Aplicar Gestalt como ayuda de agrupación, no como puntuación mecánica.
9. Priorizar correcciones que reduzcan ruido antes de añadir elementos.

## Salida
`VISUAL_HIERARCHY`, `TYPOGRAPHY`, `COLOR_AND_SURFACES`, `SPACING_AND_GROUPING`, `GENERIC_UI_RISKS`, `DISTINCTIVE_DIRECTION`, `CRAFT_PRIORITIES`.

## Integración de evidencia/MCP
- La crítica visual debe basarse en screenshot/render real cuando esté disponible; source por sí solo tiene confianza limitada.
- Browser tooling puede aportar vistas/theme/zoom; ImageGen no es herramienta de auditoría.
- Mantener separado “observado” de “dirección estética propuesta”.
