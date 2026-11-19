---
name: vx-dev-architecture-decision
description: "Diseña decisiones arquitectónicas implementables con opciones, tradeoffs, contratos y consecuencias. Usar cuando existe una decisión estructural real sobre módulos, límites, interfaces, dependencias, persistencia o estrategia de migración."
compatibility: "Read-only; no implementa ni concede permisos."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "architecture"
---

# VX Dev — Architecture Decision

## Cuándo usar
Solo para decisiones que cambian estructura, contratos duraderos, dependencias o propiedades no funcionales relevantes.

## Protocolo
1. Describir estado actual y restricciones verificadas.
2. Definir la decisión en una frase.
3. Presentar 2-3 opciones reales, incluida la mínima viable.
4. Comparar complejidad, compatibilidad, seguridad, operabilidad y reversión.
5. Explicitar contratos afectados y consumidores.
6. Elegir o dejar decisión pendiente según evidencia.
7. Registrar consecuencias positivas/negativas.
8. Si se acepta, proponer ADR con estado y supersesión.

## Salida
`OPTIONS`, `TRADEOFFS`, `CONTRACTS`, `DECISIONS_REQUIRED`, riesgos y recomendación.

No convertir propuesta en implementación ni inventar requisitos.
