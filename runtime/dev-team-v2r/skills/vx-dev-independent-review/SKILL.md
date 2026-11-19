---
name: vx-dev-independent-review
description: "Revisa de forma independiente un cambio ya implementado para detectar regresiones de contrato, complejidad accidental, scope creep, mantenimiento y riesgos no cubiertos. Usar antes de integrar cambios no triviales o cuando se solicita una segunda mirada."
compatibility: "Read-only; Reviewer no implementa, no ejecuta tests ni decide el merge."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "review"
---

# VX Dev — Independent Change Review

## Protocolo
1. Reconstruir intención y diff real.
2. Verificar corrección frente al contrato, no frente a preferencias personales.
3. Buscar regresiones de compatibilidad y cambios de boundary.
4. Revisar complejidad añadida y alternativas más simples.
5. Detectar scope creep y archivos/abstracciones no justificadas.
6. Revisar evidencia de tests sin asumir que “CI verde” cubre el riesgo correcto.
7. Descartar falsos positivos explícitamente.
8. Priorizar hallazgos BLOCKER/HIGH/MEDIUM/LOW/INFO.
9. Emitir veredicto limitado al review.
10. Si el diff toca tests/CI, verificar política de certificación viva: `UPDATE`, `REPLACE` o `ADD`.
11. Detectar tests/gates sin invariante vigente o con oráculo duplicado.
12. No recomendar retirar un test supersedido hasta existir PASS real del reemplazo.

## Veredictos
`NO_BLOCKING_FINDINGS`, `CHANGES_REQUIRED`, `BLOCKED`, `INSUFFICIENT_EVIDENCE`.

No autoriza merge ni sustituye Quality o Security.

## Integración de evidencia/MCP
- Preferir evidencia independiente ya producida por CI, GitHub, browser o runtime antes de repetir análisis.
- Usar `vx-dev-mcp-evidence-ledger` para comprobar qué claims están realmente respaldados.
- Si hace falta nueva consulta, justificar el gap que el handoff existente no cubre.
