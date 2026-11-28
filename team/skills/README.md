# Programa de skills propias
Versión del archivo: 0.23.0 | Última modificación: 2026-11-28

Estado: núcleo común candidato completo (13/13), revisión transversal estática F06-AUD-R; descubrimiento e invocaciones parciales reportadas, certificación funcional R2 limitada y laboratorio retirado a cuarentena. Revisión independiente estática reportada R5.1 sin contradicciones normativas materiales; Q7/Q13 PASS_REPORTED, integridad externa 78/78 y nueve invocaciones de skills reportadas. F06 DONE_POC_LIMITED; brechas de runtime en F07/F09/F12, archivo del fixture Q pendiente. Especialización F08 en diseño candidato; aprendizaje pendiente. No instalar ni declarar release. La versión normativa de cada componente está en su cabecera/metadata; [inventario de candidato actual](../../registry/manifest.json) permite comprobar correspondencia, no es instalador.

## F06 — núcleo común (13)

| Skill | Responsabilidad primaria |
|---|---|
| [team-routing](team-routing/SKILL.md) | Decidir quién interviene, cohesión y nivel de reparto; no ejecutar el DAG. |
| [team-task-contract](team-task-contract/SKILL.md) | Entregar alcance, entradas, aceptación y handoff; no ordenar ejecución. |
| [team-coordination](team-coordination/SKILL.md) | Ejecutar dependencias, concurrencia, recursos, retornos y Swarm; no reconstruir contexto perdido. |
| [team-context-recovery](team-context-recovery/SKILL.md) | Recuperar contexto material e identidad tras interrupción; no reintentar defectos técnicos. |
| [requirements-acceptance](requirements-acceptance/SKILL.md) | Precisar intención, requisitos y aceptación; no seleccionar arquitectura. |
| [architecture-decisions](architecture-decisions/SKILL.md) | Decidir límites, alternativas, contratos y reversibilidad; no construir el cambio. |
| [implementation-discipline](implementation-discipline/SKILL.md) | Construir incremento completo, preservar trabajo y limpiar con evidencia. |
| [systematic-debugging](systematic-debugging/SKILL.md) | Diagnosticar causa, aislar y corregir; no usar reintentos como solución. |
| [focused-testing](focused-testing/SKILL.md) | Auditar sistema de calidad, consolidar pruebas, seleccionar evidencia y comprobar delta. |
| [git-workflow](git-workflow/SKILL.md) | Administrar ramas, índice, refs, integración y consolidación; no sustituir certificación. |
| [tool-mcp-discovery](tool-mcp-discovery/SKILL.md) | Resolver capacidad efectiva, permisos y alternativas de herramientas; no ampliar privilegios. |
| [secure-development](secure-development/SKILL.md) | Construir controles seguros por riesgo; no sustituir revisión independiente de Bastión. |
| [skill-authoring](skill-authoring/SKILL.md) | Investigar, crear, evaluar, mejorar y retirar skills; no activar globalmente. |

Code carga por necesidad real de procedimiento, no por asociación temática. Las referencias entre skills delimitan responsabilidades, no cadenas de carga; los límites globales se mantienen si falta una skill. Los especialistas utilizan habilidades pertinentes dentro del contrato y permisos efectivos. No hay un orquestador propio ni una skill por agente. Consultar [protocolo de línea base de calidad](focused-testing/references/quality-baseline.md) solo para adopción o revalidación del sistema de pruebas.

## F08 — especialización (21 ID candidatos)
[ux-product-design](ux-product-design/SKILL.md) (candidata 0.1.0, evaluación NOT_RUN), [visual-ui-review](visual-ui-review/SKILL.md) (candidata 0.1.0, NOT_RUN), [accessibility](accessibility/SKILL.md) (candidata 0.1.0, NOT_RUN), [frontend-engineering](frontend-engineering/SKILL.md) (candidata 0.1.0, NOT_RUN), [design-system](design-system/SKILL.md) (candidata 0.1.0, NOT_RUN), backend-api, integration-contracts, database-modeling, data-migrations, local-first-sync, desktop-tauri, windows-powershell, linux-infrastructure, devops-ci, performance-profiling, test-automation, code-review, threat-modeling, dependency-audit, technical-documentation, editorial-writing.
Arquitectura candidata y fronteras de conocimiento: [F08.3](../../docs/ARQUITECTURA.md#f083--arquitectura-candidata-de-conocimiento-especializado), requisitos en [investigación F08.2](../../docs/INVESTIGACION-SKILLS.md). Revisión pendiente; no son skills aceptadas ni cuota. Activar desktop-tauri solo si proyecto lo exige; local-first-sync cuando exista ese requisito; no imponer stack ni proveedor. F08 requiere puerta F06 superada.

## F11 — aprendizaje (1)
team-learning. Integrar observaciones, deduplicación, propuestas, staging, evaluación y revisión; no activar antes de su propia certificación.

## Perfiles contextuales
Web/UX, ERP modular, desktop, infraestructura y documentación: criterios de selección, no copias de skills. AGENTS.md del proyecto contiene sus reglas propias; no introducir datos privados en habilidades globales.

## Método y evidencia
Aplicar [skill-authoring](skill-authoring/SKILL.md) como procedimiento único de creación/evolución. Fuentes iniciales y criterios: [FUENTES](../../docs/FUENTES.md); contraste por habilidad: [investigación](../../docs/INVESTIGACION-SKILLS.md); [evaluación F06](../../tests/F06-SKILLS.md); secuencia y estado de puertas: [roadmap](../../docs/ROADMAP.md); historia resumida: [changelog](../../CHANGELOG.md). No duplicar estos registros aquí. Validar comandos con efectos únicamente en entorno autorizado e inspeccionado.
