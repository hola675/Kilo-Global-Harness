---
name: vx-dev-project-policy
description: "Aplica las políticas de proyecto del Dev Team: alcance mínimo, ramas/PR, CI, ADR, trazabilidad source↔runtime y gates antes de merge. Usar al planificar cambios transversales, integrar trabajo o decidir si una modificación está lista para revisión."
compatibility: "Kilo Code Dev Team. Advisory-only; no concede permisos ni ejecuta shell."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "governance"
---

# VX Dev — Project Policy

## Objetivo
Mantener cambios pequeños, trazables, reversibles y verificables sin confundir source, instalación, runtime y certificación.

## Protocolo
1. Anclar el trabajo a rama/base SHA y declarar alcance.
2. Preferir un cambio autocontenido; separar cambios ortogonales.
3. No usar reset/force/rebase destructivo sobre trabajo ajeno.
4. Exigir CI verde y revisión independiente antes de integrar cambios no triviales.
5. Crear ADR solo para decisiones estructurales significativas; registrar contexto, decisión, consecuencias y supersesión.
6. Distinguir: PROPUESTO, IMPLEMENTADO, INTEGRADO, INSTALADO, EJECUTADO, CERTIFICADO.
7. Si cambia un contrato, permiso, MCP, agente o skill, identificar explícitamente qué certificación queda invalidada.
8. Mantener rollback o reversión proporcional al riesgo.

## Límites
La skill no autoriza merge, deploy, cambios de permisos, publicación ni producción.

## Salida
`{scope,base_sha,policy_gates,decision_records,ci_evidence,review_state,rollback,unknowns}`.

Referencias de diseño: Google Engineering Practices, GitHub protected branches, AWS ADR guidance.
