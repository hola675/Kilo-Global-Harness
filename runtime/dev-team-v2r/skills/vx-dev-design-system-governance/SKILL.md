---
name: vx-dev-design-system-governance
description: "Audita y define consistencia de design systems: tokens, componentes, variantes, temas, naming, estados y excepciones. Usar cuando hay drift, valores hardcodeados, componentes duplicados o una extensión del sistema necesita reglas claras."
compatibility: "Read-only; no modifica Figma, tokens ni componentes."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "design-system"
---

# VX Dev — Design System Governance

## Protocolo
1. Descubrir fuentes de verdad: tokens, variables, themes, component library, Storybook y specs.
2. Separar primitive, semantic y component tokens cuando exista esa jerarquía.
3. Revisar cobertura de color, tipografía, spacing, radius, elevation, motion y breakpoints.
4. Detectar hardcodes, aliases rotos, nombres inconsistentes y drift entre temas.
5. Revisar anatomía de componentes, props, variantes, estados y composición.
6. Distinguir excepción justificada de duplicación accidental.
7. Verificar que destructive/success/warning/info expresen intención semántica consistente.
8. Marcar deuda de sistema y riesgo de proliferación antes de proponer nuevos tokens o componentes.

## Salida
`SYSTEM_SOURCES`, `TOKEN_GAPS`, `COMPONENT_GAPS`, `DRIFT`, `THEME_RISKS`, `EXCEPTIONS`, `GOVERNANCE_RECOMMENDATIONS`.
