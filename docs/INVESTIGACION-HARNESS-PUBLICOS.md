# Investigación comparativa de harness públicos
Versión: 0.1.0 | Última modificación: 2026-11-24
Estado: análisis documental, no certificación de runtime.

## Objetivo
Construir un equipo de ingeniería global sobre Kilo Desktop, con Code nativo como líder, sin importar la arquitectura legacy ni instalar motores alternativos. Selección cualitativa por cercanía al objetivo, no por estrellas ni benchmarks no comparables.

## Referencias y decisiones
| Referencia | Patrón documentado | Aplicación propuesta | Límite |
|---|---|---|---|
| [Oh My OpenAgent](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/features.md) | Delegación por categoría, especialistas, tareas de fondo, herramientas de lenguaje | Enrutamiento por competencia, carga contextual de skills, uso de LSP disponible | No instalar su plugin ni sustituir Code por Sisyphus; hooks y API diferentes |
| [Superpowers](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md) | Implementación delegada, revisión de requisitos y calidad, evidencia | Contrato de tarea y revisión independiente según riesgo | Evitar rituales para tareas pequeñas |
| [GSD Core](https://github.com/open-gsd/gsd-core/blob/next/docs/explanation/the-phase-loop.md) | Fases con contexto, planificación, ejecución y verificación | Checkpoints y correcciones enfocadas | No imponer fases pesadas para cada cambio |
| [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/main/docs/TEAM-WORKTREE-MODE.md) | Equipo, estado compartido y worktrees | Aislamiento de cambios incompatibles; preservar trabajo no integrado | No asumir API de Claude Teams en Kilo |
| [OpenCode Swarm](https://github.com/ZaxbyHub/opencode-swarm) | Revisión independiente, puertas de calidad, control de alcance, estado reanudable | Validación por evidencia, auditoría, catálogo dinámico | No sustituir Code; no importar pipeline serial obligatorio |
| [Beads](https://github.com/gastownhall/beads/blob/main/docs/getting-started/quickstart.md) | Grafo de dependencias y tareas desbloqueadas | DAG de tareas y detección de bloqueos si se necesita persistencia adicional | Sin Dolt u otro tracker obligatorio en v0 |
| [Gas Town](https://github.com/gastownhall/gastown) | Coordinación de trabajadores y estado | Recuperación y seguimiento de trabajadores | No importar servicios ni jerarquía de roles |
| [OpenHands SDK](https://github.com/OpenHands/software-agent-sdk) | Sesiones, eventos y entornos aislados | Distinguir eventos, contexto y aislamiento real de archivos | No instalar otro SDK/motor |
| [Agent Orchestrator](https://github.com/anupamabhay/agent-orchestrator) | OpenCode plugin y modos/skills para Kilo VS Code | Referencia histórica de integración | Instrucciones de modos antiguas; no certifica Desktop |
| [Solo Code Harness](https://github.com/solo-code-com/Solo-Code-Harness) | Declara soporte Kilo y configuración multiherramienta | Candidato para auditoría posterior | Solo resultado indexado; lectura directa falló; no adoptar todavía |
| [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/) | Repositorio legible para agentes y mejora de herramientas/guardrails | AGENTS.md como mapa y reglas comprobables, mejora por fallos | No extrapolar rendimiento |
| [Anthropic](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) | Progreso incremental y continuidad entre contextos | Checkpoints con estado verificable, pruebas y reanudación | No dar por garantizada continuidad de Desktop |
| [12-factor agents](https://github.com/humanlayer/12-factor-agents) | Control de contexto y flujo | Contratos de entrada/salida pequeños | No reemplazar bucle nativo |

## Diseño propuesto
1. Code conserva prompt y modo nativos. Instrucciones globales breves; skills cargadas por necesidad.
2. Subagentes especializados capaces de analizar e implementar dentro de su alcance; general y explore se reutilizan.
3. Contrato de tarea: objetivo, criterios, alcance de escritura, dependencias, herramientas necesarias, verificación, estado y evidencia.
4. Code ejecuta directamente cambios triviales; delega tareas independientes por task en background cuando runtime lo permita. Swarm es comunicación, no autorización ni bloqueo mecánico.
5. No asignar el mismo archivo a dos escritores; usar worktree para cambios incompatibles. La separación de contexto no implica aislamiento de disco.
6. Verificación proporcional a riesgo: pruebas focalizadas para cambios pequeños; revisión fresca, pruebas integradas, seguridad o validación visual cuando corresponda. No declarar PASS sin ejecución; registrar NOT_RUN si falta entorno.
7. Estado: aprovechar todo lo nativo antes de agregar un registro mínimo por objetivo para recuperación. Evitar polling, reintentos infinitos y reejecución de tareas completadas.
8. Automejora: detectar fallo, proponer mejora mínima de skill/política, probar y revisar antes de activar. Nunca elevar permisos ni instalar dependencias de forma silenciosa.
9. MCP/plugins: descubrir y verificar disponibilidad por agente; no asumir que catálogo, conexión o permisos globales implican invocación. No duplicar integraciones.
10. No se copia código externo. Revisar licencia, versión y procedencia antes de incorporar cualquier componente externo.

## Prueba de concepto v0.1 (pendiente)
- Confirmar Desktop instalado, rutas de configuración y versión real del motor.
- Un subagente de prueba Markdown mode: subagent y una skill bajo demanda.
- Code delega dos tareas independientes; se comprueba solapamiento temporal, retorno, comunicación Swarm si está disponible y no solapamiento de escrituras.
- Simular un fallo y recuperación sin relanzamiento infinito. Revisión independiente de un diff de prueba.
- Comparar ejecución directa frente a delegada: tiempo total, llamadas, coste/uso si disponible, conflictos, pruebas ejecutadas y calidad del resultado.
- Ninguna dependencia externa obligatoria hasta evidenciar carencia del motor.

## Evidencia Kilo
- https://kilo.ai/docs/customize/custom-subagents (selección automática por description; precedencia global/proyecto; modo subagent).
- https://kilo.ai/docs/customize/marketplace (rutas de agentes y skills).
- https://kilo.ai/docs/desktop/settings/ai (gestión de agentes, skills y MCP).
- https://github.com/Kilo-Org/kilocode/blob/main/packages/kilo-docs/pages/automate/agent-manager.md (Agent Manager VS Code, task y Swarm; no asumir que agent_manager existe en Desktop).
- https://kilo.ai/docs/getting-started/settings (Swarm y permisos; validar en Desktop).
- https://github.com/onmax/best-of-agent-harnesses y https://github.com/jiji262/awesome-harness-engineering (catálogos de descubrimiento, no validación independiente).

Fecha de consulta: 2026-11-24. No se ejecutaron los harness externos ni se inspeccionó el equipo Windows; la selección no es exhaustiva. No se modifica legacy.
