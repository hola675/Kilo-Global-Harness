---
name: vx-self-improvement
description: "Usar para proponer mejoras propias VX a prompts, skills, agentes y rutas de equipo tras evidencias de errores repetidos o brechas de capacidad; siempre elaborar candidato versionado, nunca autoeditar instalación global ni autopromocionarse."
---

# VX Self Improvement V0.1 — mejoras controladas, no autoaplicadas

**Ámbito:** exclusivamente componentes VX propios, gestión de propuestas y V4.8 Academy futura. No se entrena el modelo base, no se modifican prompts en caliente y no se gobiernan agentes/skills externos.

## Detectar
1. Recibir un problema concreto: regresión, tareas repetidas fallidas, latencia excesiva **medida**, handoff deficiente o duplicidad demostrada.
2. Clasificar fuente como `DECLARADO`, `RUNNER_VERIFIED`, `INDEPENDENTLY_REVIEWED` o `NO_MEDIDO`; no usar autoinformes como certificados.
3. Decidir **causa probable**: skill, instrucciones, herramienta ausente, permiso bloqueado, dependencia defectuosa o capacidad real no demostrada. Un permiso bloqueado no es un error a saltarse.
4. Comparar la intervención mínima: actualizar descripción/referencia de skill VX, corregir un contrato, reutilizar otra habilidad, cambiar selector o **proponer** nuevo agente solo si las demás opciones no bastan.

## Diseñar candidato
5. Generar `{component_id,version_before,proposed_version,diff_summary,source_evidence,expected_change,negative_tests,rollback_plan}`; ninguna edición de HOME o rol de Kilo.
6. Mantener casos de aprendizaje separados de casos holdout. Ejecución de un agente no equivale a medición independiente.
7. Evaluar en entorno sintético con mismo modelo/tools/versiones y prueba comparativa. Si no hay runner, registrar `NO_MEDIDO`.
8. Someter a revisión externa distinta del autor y a autorización humana separada. Sin autenticación/aplicación segura, mantener estado `PENDING_REVIEW`.

## Gobierno
- Ningún agente puede certificarse, ascenderse o elevar `edit/bash/mcp/task/agent_manager` mediante esta skill.
- Skills disponibles bajo demanda no necesariamente aíslan su catálogo por agente; selección minimiza contexto, no ofrece seguridad.
- No autocrear equipos/departamentos; exigir necesidad repetida, calidad medida y costo comparado.
- No sobrescribir cambios del operador, datos privados o configuraciones de terceros.

**Salida:** propuesta de mejora versionada, matriz antes/después `NO_MEDIDO` salvo pruebas reales, riesgos y plan de reversión. Nunca mensaje «ya mejoré» sin ejecución.
