# Programa de skills propias
Versión del archivo: 0.14.0 | Última modificación: 2026-11-25

Catálogo candidato: team-routing 0.2.0, team-task-contract 0.1.0, team-coordination 0.1.0, team-context-recovery 0.1.0, requirements-acceptance 0.1.0, architecture-decisions 0.1.0, implementation-discipline 0.1.0, systematic-debugging 0.1.0, focused-testing 0.1.0, git-workflow 0.1.0, tool-mcp-discovery 0.1.0 y secure-development 0.1.0 implementadas como borradores evaluables; las demás aún por desarrollar, sin instalación ni certificación de runtime. Diseño original basado en investigación y fuentes oficiales actualizadas durante cada fase. No clonar packs masivos.

## F06 — núcleo común (13)
team-routing, team-task-contract, team-coordination, team-context-recovery, requirements-acceptance, architecture-decisions, implementation-discipline, systematic-debugging, focused-testing, git-workflow, tool-mcp-discovery, secure-development, skill-authoring.

## F08 — especialización (21)
ux-product-design, visual-ui-review, accessibility, frontend-engineering, design-system, backend-api, integration-contracts, database-modeling, data-migrations, local-first-sync, desktop-tauri, windows-powershell, linux-infrastructure, devops-ci, performance-profiling, test-automation, code-review, threat-modeling, dependency-audit, technical-documentation, editorial-writing.
Activar desktop-tauri solo si proyecto lo exige; local-first-sync cuando exista ese requisito; no imponer stack ni proveedor.
## F11 — aprendizaje (1)
team-learning. Integrar descubrimiento de skills, simplificación, observaciones, pruebas, staging y revisión.
## Perfiles contextuales
Web/UX, ERP modular, desktop, infraestructura y proyectos de documentación. Perfiles son criterios de selección y no copias de skills. En proyectos concretos, AGENTS.md contiene reglas propias; no introducir datos privados en habilidades globales.
## Proceso de creación por skill
1. Precisar objetivo, señales de activación/no activación, dueño, límites, resultado y casos reales.
2. Investigar documentación oficial de herramientas/estándares y repositorios primarios actuales; fijar fuente, revisión/fecha, licencia y aplicabilidad. Comparar dos enfoques cuando proceda; no usar ranking de estrellas como calidad.
3. Diseñar procedimiento breve, condiciones, fallbacks, verificación y ejemplos. Redactar contenido propio; atribuir material derivado y respetar licencias.
4. Crear nombre/SKILL.md con name y description compatibles, metadata version y last_modified; referencias solo cuando sean necesarias. Scripts deterministas y seguros, sin dependencias innecesarias.
5. Evaluar routing con casos positivos, negativos y ambiguos; tareas con y sin skill sobre fixtures equivalentes. Medir completitud, fallos, llamadas, latencia/contexto si observable. Validar literalmente comandos con efectos en sandbox/fixture.
6. Revisión independiente, corrección enfocada, registro de evidencia y licencia. Publicar solo si mejora o aporta capacidad clara; simplificar/retirar duplicados manteniendo cobertura.
## Fuentes iniciales
Agent Skills spec (agentskills.io), Anthropic skill-creator y mcp-builder, Superpowers, GSD, Task Observer, documentación oficial Kilo, Playwright, OWASP ASVS/WSTG. Por dominio: documentación oficial del stack y estándares aplicables (WCAG/W3C, NIST SSDF como candidatos a verificar durante F08). Ver docs/FUENTES.md.

## F06.1 — candidato inicial
[team-routing](team-routing/SKILL.md) — selección proporcional y dependencias de decisión, sin orquestador propio. [Evaluación](../../tests/F06-SKILLS.md). Separar de team-task-contract (entradas y handoff) y team-coordination (ejecución y recuperación) para evitar duplicaciones. No incorporar scripts ni preaprobaciones de herramientas.

F06.1-R: [investigación comparada de skills](../../docs/INVESTIGACION-SKILLS.md). Cada candidato conserva fuente fijada, licencia cuando verificable, decisiones de adopción/descarte y pruebas comparables. Routing 0.2.0 incorpora cohesión, competencia, coste y preparación; sin incorporar motor externo.

## F06.2-R — candidato inicial
[team-task-contract](team-task-contract/SKILL.md) — contexto suficiente, contrato proporcional, autonomía reversible, propiedad de archivos y handoff verificable; usa contrato lógico existente, no un esquema nuevo. [Investigación](../../docs/INVESTIGACION-SKILLS.md) y [evaluación](../../tests/F06-SKILLS.md). Próxima: team-coordination. Sin instalación ni runtime certificado.

## F06.3-R — candidato inicial
[team-coordination](team-coordination/SKILL.md) — despacho dinámico por resultados, recursos exclusivos, procesamiento de retornos y Swarm, recuperación selectiva e integración. [Investigación](../../docs/INVESTIGACION-SKILLS.md) y [evaluación](../../tests/F06-SKILLS.md). Próxima: team-context-recovery. Sin motor nuevo, instalación ni certificación runtime.

## F06.4-R — candidato inicial
[team-context-recovery](team-context-recovery/SKILL.md) — checkpoint proporcional, reconstrucción por identidad y procedencia, preservación de resultados vigentes y continuación segura tras pérdida de contexto. [Investigación](../../docs/INVESTIGACION-SKILLS.md) y [evaluación](../../tests/F06-SKILLS.md). Próxima: requirements-acceptance. Sin almacenamiento nuevo, instalación ni certificación runtime.

## F06.5-R — candidato inicial
[requirements-acceptance](requirements-acceptance/SKILL.md) — intención, alcance, ambigüedad, requisitos y aceptación verificable; sin imponer formato, aprobación o metodología universal. [Investigación](../../docs/INVESTIGACION-SKILLS.md) y [evaluación](../../tests/F06-SKILLS.md). Próxima: architecture-decisions. Sin instalación ni certificación runtime.

## F06.6-R — candidato inicial
[architecture-decisions](architecture-decisions/SKILL.md) — alternativas viables, restricciones, límites y contratos, consecuencias, reversibilidad y registro proporcional; sin imponer patrón o stack. [Investigación](../../docs/INVESTIGACION-SKILLS.md) y [evaluación](../../tests/F06-SKILLS.md). Próxima: implementation-discipline. Sin instalación ni certificación runtime.

## F06.7-R — candidato inicial
[implementation-discipline](implementation-discipline/SKILL.md) — incremento mínimo completo, reutilización, flujos reales, protección de cambios, transición compatible, limpieza segura y verificación focalizada. [Investigación](../../docs/INVESTIGACION-SKILLS.md) y [evaluación](../../tests/F06-SKILLS.md). Próxima: systematic-debugging. Sin instalación ni certificación runtime.

## F06.8-R — candidato inicial
[systematic-debugging](systematic-debugging/SKILL.md) — diagnóstico causal, hipótesis discriminantes, evidencia mínima, contención autorizada y corrección focalizada; sin reintentos ciegos ni instrumentación obligatoria. [Investigación](../../docs/INVESTIGACION-SKILLS.md) y [evaluación](../../tests/F06-SKILLS.md). Próxima: focused-testing. Sin instalación ni certificación runtime.

## F06.9-R — candidato inicial
[focused-testing](focused-testing/SKILL.md) — auditoría inicial y optimización de calidad, pruebas canónicas y certificación por impacto, con [marcador versionado por proyecto](focused-testing/references/quality-baseline.md). Disparador candidato en política 0.18.0; sin motor ni instalación. [Investigación](../../docs/INVESTIGACION-SKILLS.md) y [evaluación](../../tests/F06-SKILLS.md). Próxima: git-workflow.

## F06.10-R — candidato inicial
[git-workflow](git-workflow/SKILL.md) — mínima divergencia, protección de cambios/índice, integración por evidencia, consolidación y continuidad del marcador. Política candidata 0.19.0 con regla de ramas propias; sin nuevas ramas ni retirada histórica. [Investigación](../../docs/INVESTIGACION-SKILLS.md) y [evaluación](../../tests/F06-SKILLS.md). Próxima: tool-mcp-discovery.

## F06.11-R — candidato inicial
[tool-mcp-discovery](tool-mcp-discovery/SKILL.md) — selección por capacidad efectiva, herramientas nativas/locales/Desktop/MCP, autorización, evidencia contextual y brechas; sin catálogo persistente ni ampliación automática. [Investigación](../../docs/INVESTIGACION-SKILLS.md) y [evaluación](../../tests/F06-SKILLS.md). Próxima: secure-development. F09/F10 pendientes.

## F06.12-R — candidato inicial
[secure-development](secure-development/SKILL.md) — seguridad desde construcción, identidad/autorización, fronteras, secretos, datos, cadena de suministro, agentes y evidencia; revisión independiente por riesgo. [Investigación](../../docs/INVESTIGACION-SKILLS.md) y [evaluación](../../tests/F06-SKILLS.md). Próxima: skill-authoring. Sin instalación ni certificación runtime.
