# Dev Team Skills Pack V2 — Gap Fill

**Estado:** `SOURCE_READY_RUNTIME_INACTIVE`  
**Base protegida:** 18 skills V1  
**Nuevas skills:** 9  
**Objetivo total futuro:** 27  
**Runtime:** sin cambios

## Por qué estas 9

La investigación de skills actuales y la matriz legacy mostró huecos repetidos que no encajan limpiamente en las 18 skills V1. Se priorizaron workflows con trigger, entrada y criterio de éxito distintos; no se añadieron skills por lenguaje/framework ni duplicados de capacidades ya cubiertas.

| Skill | Hueco que cubre | Roles propuestos |
|---|---|---|
| `vx-dev-requirements-acceptance` | requisitos y aceptación antes de QA | Team, Quality |
| `vx-dev-release-readiness` | gate explícito de release | Team, Platform, Reviewer |
| `vx-dev-observability-privacy` | observabilidad útil sin fuga de datos | Platform, Security |
| `vx-dev-performance-analysis` | baseline y regresión de rendimiento | Quality, Platform |
| `vx-dev-sql-performance` | queries/planes/índices/waits | Data |
| `vx-dev-doc-traceability` | trazabilidad de decisión a evidencia | Research, Reviewer |
| `vx-dev-regression-analysis` | impacto de cambios sobre contratos previos | Quality, Reviewer |
| `vx-dev-task-dependency-planning` | dependencias y orden de trabajo | Team, Architect |
| `vx-dev-incident-analysis` | timeline/impacto/causalidad operacional | Platform, Backend |

## Fronteras contra V1

- Requirements Acceptance define **qué debe cumplirse**; Test Strategy define **cómo probarlo**.
- Release Readiness decide si existe evidencia suficiente; Platform Delivery describe el flujo técnico.
- Performance Analysis cubre medición general; SQL Performance cubre específicamente consultas y planes.
- Doc Traceability construye enlaces; Source Reconciliation decide qué fuente respalda una afirmación.
- Regression Analysis parte de comportamiento previo; Test Strategy diseña cobertura global.
- Incident Analysis añade timeline/impacto/blast radius; Debug Triage se centra en hipótesis técnicas.
- Task Dependency Planning descompone trabajo; Team Handoff mueve evidencia entre owners.

## Seguridad y autoridad

Las nueve skills son advisory/read-only. No contienen `allowed-tools`, shell embebido ni scripts. No conceden MCP, edit, write, bash, task, Agent Manager o Board. No modifican `kilo.jsonc`.

## Activación

Esta rama **no debe instalar las nueve skills todavía**. Antes de ampliar 18→27:

1. ejecutar evals positivos/negativos;
2. revisar false positives entre skills vecinas;
3. aprobar ACL exacta por agente;
4. actualizar instalador y backups;
5. simular;
6. aplicar una sola vez con aprobación del operador;
7. verificar hashes y recertificar los agentes afectados.

## Base de investigación

Se usaron como principios: progressive disclosure, descripciones específicas, eval-driven skill development, workflows con fronteras claras y evidencia explícita para release/performance/incident. Las skills son originales; las fuentes se usan como referencia de prácticas, no como texto copiado.
