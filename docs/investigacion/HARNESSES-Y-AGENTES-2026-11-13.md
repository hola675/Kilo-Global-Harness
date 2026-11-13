# Investigación comparativa: harnesses, agentes y skills para Kilo Global Harness V4

**Fecha de corte:** 2026-11-13. **Alcance:** investigación previa a implementación, sin instalar herramientas externas.  
**Principio:** **GLOBAL ONLY** bajo `%USERPROFILE%`; ningún adaptador debe crear configuración de agentes/MCP/skills en repositorios de aplicaciones.

Se investigaron fuentes primarias de GitHub, documentación oficial Kilo y descubrimiento temático en ocho consultas Exa (orquestación, roles, skills, seguridad, memoria, compatibilidad). **No es un inventario literal de todos los repositorios existentes**: es una selección contrastada de 44 proyectos con relevancia para Kilo. Fechas, APIs y licencias pueden cambiar; al incorporar código se revisará el commit exacto y la licencia del archivo utilizado.

## Clasificación

- **Base:** Kilo nativo, no sustituir.
- **P1:** examinar individualmente patrones o assets primero.
- **P2:** ideas o integración opcional, normalmente requiere otro runtime.
- **P3:** índices/histórico o conflictivos con global-only, no instalar directamente.

**Importante:** P1 no significa copiar o instalar automáticamente. Requiere inspección del código, permisos, condiciones de licencia, duplicados, pruebas y aprobación de promoción.

## Catálogo de fuentes (44)

| Proyecto | Tipo | Decisión | Utilidad y límite |
| --- | --- | --- | --- |
| [Kilo-Org/kilocode](https://github.com/Kilo-Org/kilocode) | núcleo | **Base** | Base nativa Task, Agent Manager, Swarm, plugins y permisos |
| [obra/superpowers](https://github.com/obra/superpowers) | metodología | **P1** | Planificación, TDD, debugging, subagent-driven development; evitar duplicar skills existentes |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | harness | **P1** | Memoria, contexto, evidencia, instrucciones y especialización; portada actual ECC |
| [wshobson/agents](https://github.com/wshobson/agents) | catálogo | **P1** | Agentes/skills/commands escritos para varias plataformas; seleccionar roles uno por uno |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | catálogo | **P1** | Biblioteca extensa de roles; adaptar frontmatter y privilegios |
| [first-fluke/oh-my-agent](https://github.com/first-fluke/oh-my-agent) | harness | **P1** | Roles de producto, frontend, backend, QA, refactor; puertas de calidad |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | metodología | **P1** | Descubrimiento, PRD, arquitectura, criterios de aceptación y QA |
| [ZaxbyHub/opencode-swarm](https://github.com/ZaxbyHub/opencode-swarm) | orquestación | **P1** | Gates, reviewer distinto de writer, control de edición y skills en cuarentena; plugin no nativo Kilo |
| [mksglu/context-mode](https://github.com/mksglu/context-mode) | contexto | **P1** | Plugin con integración Kilo documentada; evaluar ahorro real y conflicto con memoria |
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | meta-harness | **P1** | Arquitectura everything-is-a-plugin Cordis; runtime separado en preview |
| [trailofbits/skills](https://github.com/trailofbits/skills) | seguridad | **P1** | Auditoría especializada; revisar licencias de cada pieza y no duplicar habilidades |
| [cloudflare/skills](https://github.com/cloudflare/skills) | dominio | **P1** | Workers, Cloudflare, deployment; ya hay skills existentes, adaptar deltas |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | dominio | **P1** | React/Next y composición; ya hay skills existentes, adaptar deltas |
| [anthropics/skills](https://github.com/anthropics/skills) | estándar | **P1** | SKILL.md y formato; licencias heterogéneas por carpeta |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | evaluación | **P1** | Pruebas, regresión y red teaming de prompts y agentes |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | catálogo | **P2** | Colección de agentes, instrucciones y skills portables tras revisión |
| [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) | catálogo | **P2** | Plantillas, MCP, agentes y hooks; evitar instalador masivo de Claude |
| [code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) | orquestación | **P2** | Delegación intensiva y routing multmodelos; plugin de otro runtime |
| [ruvnet/claude-flow](https://github.com/ruvnet/claude-flow) | orquestación | **P2** | Swarm y memoria con muchos subsistemas; alto peso de dependencias |
| [open-mercato/cezar](https://github.com/open-mercato/cezar) | orquestación | **P2** | Worktrees, tareas concurrentes, métricas; crea estado por proyecto |
| [omnigent-ai/omnigent](https://github.com/omnigent-ai/omnigent) | meta-harness | **P2** | Supervisión de varios CLI; verificar madurez y Kilo real antes de probar |
| [hyw007726/multi-agent-orchestrator-skill](https://github.com/hyw007726/multi-agent-orchestrator-skill) | orquestación | **P2** | Adaptadores CLI incluido Kilo; escribe coord/ y usa permisos autónomos |
| [yw0nam/any-subagent](https://github.com/yw0nam/any-subagent) | orquestación | **P2** | Subsesiones identificadas por nombre; primario Claude/Codex |
| [engn-dev/meta-harness-studio](https://github.com/engn-dev/meta-harness-studio) | meta-harness | **P2** | Generación de configs entre herramientas; ruta Kilo antigua y poca validación |
| [deepklarity/harness-kit](https://github.com/deepklarity/harness-kit) | metodología | **P2** | DAG, pruebas y coste con tool externo; patrones portables |
| [solo-code-com/Solo-Code-Harness](https://github.com/solo-code-com/Solo-Code-Harness) | harness | **P2** | Múltiples engines desde fuente Kilo; ejemplo experimental de tamaño reducido |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | framework | **P2** | Grafos de estado y ejecución durable; no es plugin Kilo |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | framework | **P2** | Orquestación para .NET/Python con checkpoints y trazas |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | framework | **P2** | Handoffs, guardrails, trace y herramientas; runtime separado |
| [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | framework | **P2** | Roles y crews de agentes, runtime Python externo |
| [mastra-ai/mastra](https://github.com/mastra-ai/mastra) | framework | **P2** | Orquestación y observabilidad TS; licencia mixta en ee/ |
| [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | IDE-agente | **P2** | Comparar agentes autonomos y aislamiento; servicio independiente |
| [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent) | evaluación | **P2** | Solución de issues y benchmarks de software; reutilizar ideas de pruebas |
| [OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev) | orquestación | **P2** | Colaboración por roles, múltiples conversaciones; capa externa |
| [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) | framework | **P2** | Skills y composición en .NET; posible backend empresarial separado |
| [UKGovernmentBEIS/inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) | evaluación | **P2** | Evals y conjuntos de pruebas independientes del harness |
| [agentops-ai/agentops](https://github.com/agentops-ai/agentops) | telemetría | **P2** | Costos/trazas de agentes con SDK externo; datos privados y carga |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | MCP | **P2** | Servidores MCP de referencia, instalar solo tools necesarios |
| [agentsmd/agents.md](https://github.com/agentsmd/agents.md) | estándar | **P2** | Formato de instrucciones; mantener en HOME, no en proyectos |
| [Picrew/awesome-agent-harness](https://github.com/Picrew/awesome-agent-harness) | índice | **P3** | Índice para ampliar exploración, no integrar directamente |
| [arach/awesome-agent-clients](https://github.com/arach/awesome-agent-clients) | índice | **P3** | Mapa de clientes/IDE/orquestadores; catálogo de descubrimiento |
| [e2b-dev/awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) | índice | **P3** | Lista amplia de agentes; localizar solo implementaciones relevantes |
| [microsoft/autogen](https://github.com/microsoft/autogen) | histórico | **P3** | README advierte proyecto archivado/sustituido; no usar como base |
| [jordimarsal/harness](https://github.com/jordimarsal/harness) | harness | **P3** | Gates y flujos, instalador escribe en proyecto; solo inspiración |

## Resultados verificados de mayor impacto

1. **Kilo nativo:** `task` con subagentes aislados en contexto pero **sin worktree**; permite tareas foreground/background. Agent Manager crea sesiones aisladas en worktrees. Kilo Swarm sirve como tablero de comunicación entre padre e hijos, **no** planificador ni creador de agentes. No necesitamos dos capas adicionales que hagan lo mismo.
2. **Fuentes de roles:** wshobson/agents y VoltAgent sirven para extraer competencias acotadas, no importar cientos de prompts. Normalizar en Markdown YAML de Kilo y revisión de privilegios.
3. **Metodologías:** Superpowers y BMAD aportan TDD, criterios de aceptación, handoffs y revisión. Ya existen skills en la instalación actual: comparar hashes y descripciones, no duplicar.
4. **Quality gates:** OpenCode Swarm y oh-my-agent separan autor, crítico y verificador. Sus hooks/plugins son específicos y no se ejecutan automáticamente en Kilo; portar las *ideas* y diseñar gates propios.
5. **Context Mode:** documenta integración como plugin de Kilo y hooks. Prioridad de piloto **sin sustituir Codebase Memory**: medir ruido/latencia y validar que no procese información privada indebidamente.
6. **DeepSeek Harness:** modularidad Cordis de plugins. Es un runtime independiente en preview con cambios incompatibles; ideas sí, mezcla binaria directa no.
7. **ECC:** mantener como fuente de patrones de contexto y memoria; migró desde everything-claude-code a ECC. Su instalación masiva puede superponer agentes y hooks; priorizar adaptación selectiva.
8. **Bibliotecas de skills:** Anthropic incluye carpetas de licencia distinta; Cloudflare y Vercel ya tienen presencia en la máquina; Trail of Bits requiere revisión específica del licenciamiento antes de redistribuir.
9. **Evaluación:** promptfoo e Inspect AI pueden aportar pruebas offline y red-team; medir coste y falsos positivos antes de correr LLM judges.
10. **No usar Microsoft AutoGen como cimiento nuevo:** su README avisa archivo/no mantenimiento y recomienda Microsoft Agent Framework.

## Protocolo de incorporación

```text
descubrir URL -> verificar licencia archivo + commit SHA -> revisión de prompt injection
-> analizar herramientas y permisos -> contrastar con catálogo local
-> adaptar a agent/skill Kilo global en namespace vx- -> pruebas estructurales
-> prueba de comportamiento con tarea pequeña -> medir coste/calidad
-> revisión humana -> registrar procedencia y promover
```

**Sin autoimportación / autoupdate.** La fuente se audita de forma aislada, no se ejecutan install scripts ni hooks durante investigación. Guardar `source_url`, `commit_sha`, `source_path`, `license`, `adaptation_notes`, `test_evidence` por componente.

## Riesgos y restricciones

- Los repositorios de terceros pueden incluir instrucciones maliciosas, hooks o scripts con capacidades de red/lectura de secretos. Tratar el código como no confiable.
- `mcp` conectado no significa que deba activarse siempre: herramientas numerosas agregan peso al contexto.
- Mantener **AutoApprove**, pero permisos efectivos por agente y operaciones de alto riesgo deben conservar sus bloqueos.
- No hay garantía de que una suscripción de un proveedor habilite los CLI o API de otro.
- Una misma rama Git no puede estar simultáneamente checkout activa en varios worktrees: **un solo branch temporal + lectura paralela + un writer** es el modo estricto. Para edición en paralelo *aislada* se precisan branches work/* auxiliares y limpieza tras merge, habilitada solo por consentimiento expreso.
- No copiar prompts fuente sin verificar licencias; usar atribución y conservar avisos MIT/Apache/CC donde apliquen.

## Fuentes de compatibilidad

- https://kilo.ai/docs/automate/agent-manager
- https://kilo.ai/docs/automate/agent-manager-workflows
- https://kilo.ai/docs/customize/custom-subagents
- https://kilo.ai/docs/automate/extending/plugins
- https://kilo.ai/docs/customize/agent-permissions
- https://agentskills.io/specification

Continuación: [Diseño de orquestación V4](./ORQUESTACION-MULTIAGENTE-V4.md).
