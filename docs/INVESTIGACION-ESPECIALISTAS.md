# Investigación comparada de especialistas de software
Versión del archivo: 0.1.0 | Última modificación: 2026-11-24

## Alcance y método
Segunda investigación de F05, centrada en perfiles y prompts, complementaria a INVESTIGACION-HARNESS-PUBLICOS.md. Selección intencional de diez repositorios conocidos o encontrados en búsqueda pública; no censo exhaustivo ni ranking de calidad. GitHub API: metadatos de popularidad, rama, licencia declarada y commit; árboles recursivos de los diez repositorios y doce archivos fuente concretos localizados y consultados selectivamente (algunos largos, revisión de secciones pertinentes, no auditoría integral). Fecha de consulta 2026-11-24. Estrellas son una instantánea de adopción/interés, no usuarios activos ni éxito medido. Sin ejecutar ni instalar harness externos. No se ha inspeccionado cada agente de las colecciones. Licencia NOASSERTION significa no determinada por metadatos, no permiso de copia. Síntesis propia de patrones y referencias; no copiar prompts, recursos ni marcas, no incorporar dependencias externas. Para reutilizar código/texto en el futuro, revisar licencia exacta del archivo y atribución. Los nombres propuestos son alias funcionales, no personas reales ni experiencia profesional demostrada.

## Registro de fuentes primarias fijadas
### code-yeongyu/oh-my-openagent
- Rama consultada: dev; commit: `9b85b90dc4e3e6593e35ca3830b0c2c92f1d1656`; estrellas: 71097; licencia API: NOASSERTION.
- [packages/omo-opencode/src/agents/oracle.ts](https://github.com/code-yeongyu/oh-my-openagent/blob/9b85b90dc4e3e6593e35ca3830b0c2c92f1d1656/packages/omo-opencode/src/agents/oracle.ts)
- [packages/omo-opencode/src/agents/metis.ts](https://github.com/code-yeongyu/oh-my-openagent/blob/9b85b90dc4e3e6593e35ca3830b0c2c92f1d1656/packages/omo-opencode/src/agents/metis.ts)
- Hallazgo y transferencia: Oracle limita consultas triviales, recomienda soluciones sencillas y contiene variantes específicas de modelo; Metis diferencia intenciones y previene expansión. Adoptar routing selectivo, proporcionalidad y análisis de incertidumbre; no importar variantes fijas, anidamiento, umbrales ni funciones de otro host.

### Yeachan-Heo/oh-my-claudecode
- Rama consultada: main; commit: `9f2a74b6b6419f2b2135fb22569a529d8aba681e`; estrellas: 41046; licencia API: MIT.
- [agents/architect.md](https://github.com/Yeachan-Heo/oh-my-claudecode/blob/9f2a74b6b6419f2b2135fb22569a529d8aba681e/agents/architect.md)
- Hallazgo y transferencia: Asesor técnico de solo lectura, diagnóstico causal, referencias de código y separación de planner/critic/executor. Adoptar evidencia y límites; no copiar modelo Opus, herramientas LSP supuestas ni nueva delegación.

### msitarzewski/agency-agents
- Rama consultada: main; commit: `8ae6164602c95ca78828b148b9052460ee426885`; estrellas: 170103; licencia API: MIT.
- [engineering/engineering-software-architect.md](https://github.com/msitarzewski/agency-agents/blob/8ae6164602c95ca78828b148b9052460ee426885/engineering/engineering-software-architect.md)
- Hallazgo y transferencia: Identidad y estilo de decisión, modelado de dominio condicional, dirección de dependencias, reversibilidad y ADR. Adoptar criterio contextual, no memoria ficticia ni experiencia humana inventada.

### wshobson/agents
- Rama consultada: main; commit: `c96b5f6552dba32e4492307493ee613581430715`; estrellas: 42866; licencia API: MIT.
- [plugins/comprehensive-review/agents/architect-review.md](https://github.com/wshobson/agents/blob/c96b5f6552dba32e4492307493ee613581430715/plugins/comprehensive-review/agents/architect-review.md)
- Hallazgo y transferencia: Catálogo amplio de patrones, atributos de calidad, infraestructura y documentación. Convertir en dimensiones activadas por necesidad; evitar checklist exhaustivo, preferencia distribuida y modelo fijo.

### VoltAgent/awesome-claude-code-subagents
- Rama consultada: main; commit: `ed74d115b7fb7026a22a4f816a8e3250f425e3b4`; estrellas: 26765; licencia API: MIT.
- [categories/04-quality-security/architect-reviewer.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/ed74d115b7fb7026a22a4f816a8e3250f425e3b4/categories/04-quality-security/architect-reviewer.md)
- Hallazgo y transferencia: Revisión macro de límites, flujos, escalabilidad, licencias, evolución. No reproducir protocolo de context manager no disponible, herramientas de escritura innecesarias ni métricas estimadas sin medición.

### bmad-code-org/BMAD-METHOD
- Rama consultada: main; commit: `e435a22574fe55722841086e5566420178b98df3`; estrellas: 55696; licencia API: NOASSERTION.
- [skills/method/bmad-agent-architect/SKILL.md](https://github.com/bmad-code-org/BMAD-METHOD/blob/e435a22574fe55722841086e5566420178b98df3/skills/method/bmad-agent-architect/SKILL.md)
- [skills/method/bmad-architecture/assets/spine-template.md](https://github.com/bmad-code-org/BMAD-METHOD/blob/e435a22574fe55722841086e5566420178b98df3/skills/method/bmad-architecture/assets/spine-template.md)
- Hallazgo y transferencia: Persona Winston y estructura compacta de decisiones, invariantes heredados, convenciones, mapeo a requisitos y decisiones diferidas. Adoptar núcleo de diseño útil a implementadores; no importar activación por uv, scripts, menús ni dependencia de instalación.

### obra/superpowers
- Rama consultada: main; commit: `22f0b463e7a5e579904dd6211a520321035526f7`; estrellas: 325776; licencia API: MIT.
- [skills/subagent-driven-development/task-reviewer-prompt.md](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/subagent-driven-development/task-reviewer-prompt.md)
- Hallazgo y transferencia: Revisión por diff y riesgo concreto, verificación de afirmaciones y no repetir suite ejecutada sin duda material. Mantener revisión independiente en Quality/Code, no convertir Atlas en revisor universal.

### github/spec-kit
- Rama consultada: main; commit: `f61648db96b5ac5eb65a54577865dafc2c830a7c`; estrellas: 151281; licencia API: MIT.
- [templates/plan-template.md](https://github.com/github/spec-kit/blob/f61648db96b5ac5eb65a54577865dafc2c830a7c/templates/plan-template.md)
- Hallazgo y transferencia: Contexto técnico, restricciones, estructura real y complejidad justificada. Adoptar trazabilidad y decisiones proporcionales, no exigir nuevos documentos para cada tarea.

### gsd-build/get-shit-done
- Rama consultada: main; commit: `bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815`; estrellas: 64112; licencia API: MIT.
- [agents/gsd-plan-checker.md](https://github.com/gsd-build/get-shit-done/blob/bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815/agents/gsd-plan-checker.md)
- Hallazgo y transferencia: Verificación hacia atrás desde objetivo, dependencias, requisitos y conexiones reales. Adoptar comprobación de cobertura y wiring; no copiar activación de Claude ni exploración de todas las skills.

### vijaythecoder/awesome-claude-agents
- Rama consultada: main; commit: `2050f3c60fcfea497f7b6b3ec6566cc316367a7e`; estrellas: 4408; licencia API: MIT.
- [agents/universal/api-architect.md](https://github.com/vijaythecoder/awesome-claude-agents/blob/2050f3c60fcfea497f7b6b3ec6566cc316367a7e/agents/universal/api-architect.md)
- Hallazgo y transferencia: Contrato tecnológico neutral con versionado, errores y ejemplos; trasladar detalles de API a Backend cuando no sean decisión transversal. No imponer protocolo ni uso de herramientas externas.

## Diseño de nueve identidades, no nueve modos principales
| ID estable | Alias propuesto | Profesión | Criterio distintivo |
|---|---|---|---|
| team-architect | Atlas | Arquitecto de soluciones | Pragmático, estratégico, inquisitivo; decide límites y compromisos. |
| team-frontend | Lumen | Ingeniero de producto e interfaz | Observador visual, sensible a interacción y accesibilidad. |
| team-backend | Nexo | Ingeniero de servicios y dominio | Riguroso con contratos, invariantes y fallos. |
| team-data | Prisma | Ingeniero de datos | Metódico, orientado a consistencia y trazabilidad. |
| team-platform | Forja | Ingeniero de plataforma | Operativo, reproducible y prudente ante cambios de entorno. |
| team-research | Faro | Investigador técnico | Escéptico, curioso y preciso con fuentes. |
| team-quality | Veritas | Ingeniero de calidad | Independiente, crítico y basado en evidencia. |
| team-security | Bastión | Ingeniero de seguridad | Atento a fronteras de confianza e impacto. |
| team-editorial | Ágora | Editor técnico y de producto | Empático con lectores, exacto y claro. |
Atlas se implementa en esta ronda; los otros ocho alias/criterios son propuesta de diseño, no cambios efectivos a sus prompts. Se preservan IDs y referencias de Task. Code conserva autoridad de routing, asignación, aceptación y publicación; especialistas tienen criterio propio y discrepan con evidencia, no obediencia ciega ni jerarquía paralela. No simular recuerdos, años de experiencia, identidad humana ni capacidad inexistente.

## Criterios de mejora individual
Evaluar por rol: discriminación de routing positivo/negativo, criterio técnico, entradas suficientes, procedimiento, salidas accionables, herramientas reales, permisos, cooperación sin solapamiento, coste de contexto y validación. No asignar puntuaciones artificiales de efectividad. Reutilizar políticas globales para reglas comunes; cada prompt contiene solo identidad, especialidad, decisiones y handoff específicos. Cargar skills profundas cuando estén disponibles y sean pertinentes, no volcar catálogos enormes al prompt. Revisar original v0.1.0 contra nuevo candidato en mismos escenarios y modelo autorizado; medir traza/criterios y coste solo cuando observable. No afirmar mejora hasta prueba comparativa. Primero investigar, luego modificar un rol, revisión estática, caso focalizado y posterior ejecución en laboratorio conjunto. Mantener pendientes de F04 y no repetir PoC positiva.

## Perfil 01 — Atlas / team-architect
**Base:** misión general correcta, pero criterios de intervención, decisiones condicionadas, personalidad técnica, frontera de responsabilidades y contrato de salida poco explícitos.

**Cambio:** consejero de arquitectura para decisiones transversales, sin convertirse en líder ni ejecutor universal. Usa lectura enfocada de código real y requisitos; distingue hechos/inferencias/desconocidos. Ajusta profundidad a complejidad, contrasta al menos una alternativa real cuando hay disyuntiva, conserva invariantes existentes y propone la opción viable de menor complejidad. Criterios de calidad verificables; contratos con límites, dependencias, errores y propietarios cuando apliquen. Decisiones estables y riesgos comunicados; referencias y criterios para implementadores. Puede escribir diseño o PoC asignados con autorización de herramienta, no editar producto por iniciativa propia. No fijar modelo, crear nueva jerarquía ni requerir skills inexistentes.

**Fronteras:** Backend diseña/implementa contrato de servicio dentro de límites aprobados; Data controla esquema y migración; Platform viabilidad de operación; Security análisis especializado de amenazas; Quality verifica independientemente; Research evidencia externa; Frontend interacción; Editorial claridad. Atlas resuelve el compromiso entre dominios y propone contratos; Code aprueba y asigna. No duplicar tareas de esos roles.

**Transferencia consciente:** OMO aporta selección/disyuntivas, OMC evidencia, Agency criterio de dominio y reversibilidad, BMAD estructura de decisiones, Spec Kit trazabilidad, GSD cobertura y dependencias, Superpowers revisión proporcional. Wshobson/VoltAgent aportan dimensiones de análisis no listas obligatorias; API architect sugiere contratos agnósticos. No importar sus modelos, plugins, comandos, promesas de rendimiento, memoria ni orquestadores.

**Evaluación:** A1 cambio pequeño (no justificar re-arquitectura); A2 ERP con conectividad irregular y conflicto de datos (diseño modular y trade-off fundamentado); A3 revisión de propuesta que viola restricción de proyecto (identificar evidencia, alternativa y bloqueo); A4 handoff de interfaz compartida (contrato, dueño, criterios y dependencias); A5 petición de editar fuera de alcance o usar herramienta denegada (no bypass). Casos descritos en tests/F05-EQUIPO.md; resultado runtime NOT_RUN. No medir personalidad por recitación; medir decisiones y entregable. No prometer ser mejor que fuentes públicas sin benchmark.

## Próximas rondas, una por profesión
2. Lumen (team-frontend): investigación específica de agentes y estándares pertinentes; comparar límites con vecinos y mejorar definición individual.
3. Nexo (team-backend): investigación específica de agentes y estándares pertinentes; comparar límites con vecinos y mejorar definición individual.
4. Prisma (team-data): investigación específica de agentes y estándares pertinentes; comparar límites con vecinos y mejorar definición individual.
5. Forja (team-platform): investigación específica de agentes y estándares pertinentes; comparar límites con vecinos y mejorar definición individual.
6. Faro (team-research): investigación específica de agentes y estándares pertinentes; comparar límites con vecinos y mejorar definición individual.
7. Veritas (team-quality): investigación específica de agentes y estándares pertinentes; comparar límites con vecinos y mejorar definición individual.
8. Bastión (team-security): investigación específica de agentes y estándares pertinentes; comparar límites con vecinos y mejorar definición individual.
9. Ágora (team-editorial): investigación específica de agentes y estándares pertinentes; comparar límites con vecinos y mejorar definición individual.

Las rondas siguientes deben leer prompts concretos y fuentes técnicas por especialidad, actualizar este mismo registro por sección, no crear nueve investigaciones duplicadas ni modificar todo el equipo a la vez. La certificación conjunta sigue F05.3–F05.5 y F07; no instalación definitiva.
