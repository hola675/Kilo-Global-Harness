---
name: vx-dev-team-handoff
description: "Estructura handoffs y trabajo coordinado entre líder y especialistas del Dev Team. Usar cuando una tarea cruza roles, requiere entregar evidencia entre especialistas o necesita una integración final sin fan-out innecesario."
compatibility: "Kilo Code Dev Team depth=1. No usa Agent Manager, Board ni delegación desde hijos."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "collaboration"
---

# VX Dev — Team Handoff

## Principio
Coordinar por incertidumbres independientes, no por ritual. Un especialista entrega evidencia; el líder integra.

## Protocolo
1. Definir `task_id`, objetivo, base SHA, alcance y owner.
2. Delegar al mínimo conjunto de especialistas necesario.
3. Cada hijo devuelve hechos observados, inferencias, riesgos, desconocidos y handoff.
4. No transferir autorizaciones ni permisos entre sesiones.
5. No permitir escritura concurrente sobre el mismo alcance.
6. Si dos hallazgos se contradicen, resolver por evidencia, no por votación.
7. Reviewer/Quality/Security conservan fronteras distintas.
8. El líder registra qué evidencia utilizó y qué descartó.

## Handoff mínimo
`{task_id,owner,scope,evidence,contracts,tests_executed,tests_not_executed,risks,unknowns,next_owner}`.

## Límites
Los hijos no delegan. La skill no habilita task, Board, Agent Manager ni worktrees.
