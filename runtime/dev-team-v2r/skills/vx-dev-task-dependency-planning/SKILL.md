---
name: vx-dev-task-dependency-planning
description: "Descompone trabajo en unidades ordenadas por dependencias, riesgo y evidencia. Usar cuando una tarea compleja requiere secuencia, ownership, gates o paralelización segura sin introducir orquestación de agentes hijos."
compatibility: "Advisory-only; respeta depth=1 y no concede task, Agent Manager, Board ni ejecución."
metadata:
  version: "1.0.0"
  origin: "vx-dev-original"
  category: "planning"
---

# VX Dev — Task Dependency Planning

## Protocolo
1. Definir resultado final verificable.
2. Dividir por dependencias reales, no por capas arbitrarias.
3. Marcar prerequisitos, decisiones bloqueantes y artefactos de salida.
4. Separar trabajo paralelo de trabajo que comparte estado mutable.
5. Asignar owner lógico por dominio sin delegar desde subagentes.
6. Colocar gates antes de operaciones irreversibles o de alto riesgo.
7. Minimizar ramas de trabajo simultáneas y puntos de integración.
8. Mantener estados: pendiente, listo, en curso, bloqueado, verificado.

## Salida
`WORK_BREAKDOWN`, `DEPENDENCY_GRAPH`, `PARALLEL_SAFE`, `BLOCKERS`, `OWNERS`, `GATES`, `INTEGRATION_ORDER`.
