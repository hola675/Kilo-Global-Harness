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
9. Aplicar certificación viva: cada cambio mantiene solo las pruebas que validan la verdad actual.
10. Si una prueba nueva cubre completamente la misma invariante que una prueba antigua y pasa, retirar la prueba supersedida del CI activo.
11. Conservar historia en Git, changelog, registries y evidencia; no mediante suites históricas activas.
12. Un cambio localizado requiere la prueba mínima eficaz; ampliar cobertura solo si cambió una invariante transversal.

## Límites
La skill no autoriza merge, deploy, cambios de permisos, publicación ni producción.

## Salida
`{scope,base_sha,policy_gates,decision_records,ci_evidence,review_state,rollback,unknowns}`.

Referencias de diseño: Google Engineering Practices, GitHub protected branches, AWS ADR guidance.

## Integración de evidencia/MCP
- Para gates de merge/release, reutilizar estado remoto ya obtenido por GitHub MCP si el rol lo tiene autorizado.
- Si una decisión depende de documentación externa o estado de CI, enrutar primero con `vx-dev-mcp-capability-routing`.
- Registrar SHAs, PRs, runs o fuentes en `vx-dev-mcp-evidence-ledger`; no repetir consultas ya resueltas por otro especialista.
