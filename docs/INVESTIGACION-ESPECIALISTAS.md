# Investigación comparada de especialistas de software
Versión del archivo: 0.5.0 | Última modificación: 2026-11-24

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
Atlas, Lumen, Nexo, Prisma y Forja tienen definiciones candidatas v0.2.0; los cuatro restantes conservan v0.1.0 y alias propuestos. Se preservan IDs y referencias de Task. Code conserva autoridad de routing, asignación, aceptación y publicación; especialistas tienen criterio propio y discrepan con evidencia, no obediencia ciega ni jerarquía paralela. No simular recuerdos, años de experiencia, identidad humana ni capacidad inexistente.

## Criterios de mejora individual
Evaluar por rol: discriminación de routing positivo/negativo, criterio técnico, entradas suficientes, procedimiento, salidas accionables, herramientas reales, permisos, cooperación sin solapamiento, coste de contexto y validación. No asignar puntuaciones artificiales de efectividad. Reutilizar políticas globales para reglas comunes; cada prompt contiene solo identidad, especialidad, decisiones y handoff específicos. Cargar skills profundas cuando estén disponibles y sean pertinentes, no volcar catálogos enormes al prompt. Revisar original v0.1.0 contra nuevo candidato en mismos escenarios y modelo autorizado; medir traza/criterios y coste solo cuando observable. No afirmar mejora hasta prueba comparativa. Primero investigar, luego modificar un rol, revisión estática, caso focalizado y posterior ejecución en laboratorio conjunto. Mantener pendientes de F04 y no repetir PoC positiva.

## Perfil 01 — Atlas / team-architect
**Base:** misión general correcta, pero criterios de intervención, decisiones condicionadas, personalidad técnica, frontera de responsabilidades y contrato de salida poco explícitos.

**Cambio:** consejero de arquitectura para decisiones transversales, sin convertirse en líder ni ejecutor universal. Usa lectura enfocada de código real y requisitos; distingue hechos/inferencias/desconocidos. Ajusta profundidad a complejidad, contrasta al menos una alternativa real cuando hay disyuntiva, conserva invariantes existentes y propone la opción viable de menor complejidad. Criterios de calidad verificables; contratos con límites, dependencias, errores y propietarios cuando apliquen. Decisiones estables y riesgos comunicados; referencias y criterios para implementadores. Puede escribir diseño o PoC asignados con autorización de herramienta, no editar producto por iniciativa propia. No fijar modelo, crear nueva jerarquía ni requerir skills inexistentes.

**Fronteras:** Backend diseña/implementa contrato de servicio dentro de límites aprobados; Data controla esquema y migración; Platform viabilidad de operación; Security análisis especializado de amenazas; Quality verifica independientemente; Research evidencia externa; Frontend interacción; Editorial claridad. Atlas resuelve el compromiso entre dominios y propone contratos; Code aprueba y asigna. No duplicar tareas de esos roles.

**Transferencia consciente:** OMO aporta selección/disyuntivas, OMC evidencia, Agency criterio de dominio y reversibilidad, BMAD estructura de decisiones, Spec Kit trazabilidad, GSD cobertura y dependencias, Superpowers revisión proporcional. Wshobson/VoltAgent aportan dimensiones de análisis no listas obligatorias; API architect sugiere contratos agnósticos. No importar sus modelos, plugins, comandos, promesas de rendimiento, memoria ni orquestadores.

**Evaluación:** A1 cambio pequeño (no justificar re-arquitectura); A2 ERP con conectividad irregular y conflicto de datos (diseño modular y trade-off fundamentado); A3 revisión de propuesta que viola restricción de proyecto (identificar evidencia, alternativa y bloqueo); A4 handoff de interfaz compartida (contrato, dueño, criterios y dependencias); A5 petición de editar fuera de alcance o usar herramienta denegada (no bypass). Casos descritos en tests/F05-EQUIPO.md; resultado runtime NOT_RUN. No medir personalidad por recitación; medir decisiones y entregable. No prometer ser mejor que fuentes públicas sin benchmark.


## Perfil 02 — Lumen / team-frontend
Consulta selectiva adicional del 2026-11-24: siete archivos (secciones relevantes), cuatro repositorios y tres referencias técnicas. Se conserva el método original; no se ejecutaron herramientas ni se copiaron prompts o assets. Los commits de Agency, VoltAgent y Wshobson corresponden a la primera ronda; Anthropic se consultó por main y se registra blob exacto, no commit de rama ni licencia de reutilización confirmada.
- Agency Agents: [frontend](https://github.com/msitarzewski/agency-agents/blob/8ae6164602c95ca78828b148b9052460ee426885/engineering/engineering-frontend-developer.md) y [UI](https://github.com/msitarzewski/agency-agents/blob/8ae6164602c95ca78828b148b9052460ee426885/design/design-ui-designer.md). Criterio de implementación y diseño compartido, coherencia de tokens, rendimiento y accesibilidad. Evitar experiencia/memoria ficticia, metas de latencia universales y ejemplos de stack como mandato.
- VoltAgent: [frontend](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/ed74d115b7fb7026a22a4f816a8e3250f425e3b4/categories/01-core-development/frontend-developer.md) y [UI](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/ed74d115b7fb7026a22a4f816a8e3250f425e3b4/categories/01-core-development/ui-designer.md). Contexto, estados, movimiento, adaptación y handoff. Sustituir context-manager y progreso ritual por contrato de Code; no exigir porcentajes de cobertura o Storybook sin motivo.
- Wshobson: [frontend](https://github.com/wshobson/agents/blob/c96b5f6552dba32e4492307493ee613581430715/plugins/frontend-mobile-development/agents/frontend-developer.md) y [UI](https://github.com/wshobson/agents/blob/c96b5f6552dba32e4492307493ee613581430715/plugins/ui-design/agents/ui-designer.md). Estado, layout, interacción y arquitectura de componentes. Catálogo como referencia futura de skills, no stack fijo. El perfil cita FID; usar INP según fuente primaria vigente consultada.
- Anthropic: [frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md), blob a5333457c414d20d625f307df945842c0952ecc3; [licencia declarada por la skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/LICENSE.txt) no examinada, sin reutilización literal. Dirección visual específica al producto, tipografía y estructura con intención, movimiento proporcional. No imponer originalidad sobre fidelidad o usabilidad.
- Fuentes técnicas: [WCAG 2.2, recomendación 2024-12-12](https://www.w3.org/TR/2024/REC-WCAG22-20241212/), [ARIA APG](https://www.w3.org/WAI/ARIA/apg/) (guía de patrones, no certificación automática), [Web Vitals](https://web.dev/articles/vitals) (LCP, INP, CLS, datos de campo y laboratorio diferenciados). No inferir cumplimiento global por pruebas parciales.
**Base:** v0.1.0 tiene misión, reutilización y validación generales, pero carece de routing discriminante, método de diseño condicionado a encargo, tratamiento detallado de interacción y evidencia.
**Cambio:** Lumen integra diseño e implementación en el mismo rol para evitar handoffs internos innecesarios. Trabaja por objetivo, flujo, estados, identidad, componentes y validación real; no cambia arquitectura o contratos sin Code, ni inventa assets, endpoints o éxito. Se conserva permiso edit allow, bash ask, web/task deny; diseño/navegador MCP solo con exposición y autorización verificadas, F09 pendiente. Sin dependencias nuevas ni nuevos roles. Conectividad y plataforma activan criterios condicionales, no imposiciones tecnológicas.
**Evaluación:** L1–L5 en tests/F05-EQUIPO.md, incluyendo discriminación de routing, fidelidad y reutilización, interacción accesible, resiliencia, permisos y evidencia; sustituye caso genérico frontend conservando cobertura. Runtime NOT_RUN; no se demuestra superioridad ni velocidad por longitud del prompt.


## Perfil 03 — Nexo / team-backend
Consulta selectiva adicional del 2026-11-24: siete archivos de cuatro repositorios (secciones relevantes) fijados a los commits de la primera ronda y cuatro referencias técnicas. Síntesis original, sin importar prompts, herramientas, dependencias ni ejecución externa.
- Agency Agents: [backend architect](https://github.com/msitarzewski/agency-agents/blob/8ae6164602c95ca78828b148b9052460ee426885/engineering/engineering-backend-architect.md). Contratos, presupuesto temporal, fallos parciales y observabilidad; no asumir escalas, latencias, cloud ni apropiarse de arquitectura/datos.
- VoltAgent: [backend developer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/ed74d115b7fb7026a22a4f816a8e3250f425e3b4/categories/01-core-development/backend-developer.md) y [API designer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/ed74d115b7fb7026a22a4f816a8e3250f425e3b4/categories/01-core-development/api-designer.md). Validación de dominio, contratos, pruebas de autorización e integración; descartar context-manager obligatorio, cobertura/latencia arbitrarias, modelos y stack fijo.
- Wshobson: [backend architect](https://github.com/wshobson/agents/blob/c96b5f6552dba32e4492307493ee613581430715/plugins/backend-development/agents/backend-architect.md), [API design](https://github.com/wshobson/agents/blob/c96b5f6552dba32e4492307493ee613581430715/plugins/backend-development/skills/api-design-principles/SKILL.md) y [saga orchestration](https://github.com/wshobson/agents/blob/c96b5f6552dba32e4492307493ee613581430715/plugins/backend-development/skills/saga-orchestration/SKILL.md). Adaptar criterios de contrato, deduplicación y compensación condicional; no asumir que una saga equivale a transacción atómica, que compensar siempre funciona o que una entrega exactly-once implica efectos únicos. POST puede diseñarse idempotente por contrato, no lo es por semántica general HTTP.
- Awesome Claude Agents: [API architect](https://github.com/vijaythecoder/awesome-claude-agents/blob/2050f3c60fcfea497f7b6b3ec6566cc316367a7e/agents/universal/api-architect.md). Especificaciones independientes de tecnología y ejemplos verificables; no exigir agente aparte, web directo, nuevos archivos o SDK para cada cambio.
- Referencias primarias consultadas: [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) (semántica HTTP e idempotencia), [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) (detalle de errores, sustituye RFC 7807), [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) (autorización por objeto/propiedad/función y consumo de recursos), [AWS Builders Library](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) (reintento seguro, backoff, jitter y amplificación de carga; patrón independiente de proveedor, no estándar). No declarar conformidad global.
**Base:** v0.1.0 contempla contratos, validación, idempotencia y transacciones, sin método de dominio, criterios de concurrencia/fallo incierto ni routing detallado.
**Cambio:** Nexo convierte requisitos en invariantes, estados y operaciones verificables; conserva contratos, autoriza en servidor y protege efectos persistidos. Distingue transacción local, resultado remoto incierto y recuperación distribuida. Los patrones se activan solo cuando el caso los exige; no impone microservicios, colas, REST ni proveedor. Data posee almacenamiento/esquema, Atlas decisiones transversales, Nexo servicio y reglas; Code acuerda fronteras. Permisos intactos: edit allow, bash ask, web/task deny, MCP por capacidad autorizada.
**Evaluación:** N1–N5 de tests/F05-EQUIPO.md, discriminación de routing, reglas/autorización, concurrencia/duplicación, fallos e integraciones, compatibilidad y límites. Runtime NOT_RUN; no demostrar superioridad por texto más largo.


## Perfil 04 — Prisma / team-data
Consulta selectiva del 2026-11-24: seis archivos de tres repositorios fijados a commits de la primera ronda y cuatro páginas de fuentes técnicas. Una ruta adicional de skill SQL en Wshobson devolvió 404 y no se cuenta como fuente leída. No se ejecutaron herramientas externas ni se copiaron prompts.
- Agency Agents: [data engineer](https://github.com/msitarzewski/agency-agents/blob/8ae6164602c95ca78828b148b9052460ee426885/engineering/engineering-data-engineer.md). Adoptar procedencia, calidad, contratos y reejecución segura; no imponer lakehouse, soft deletes, auditoría por fila o métricas universales, ni experiencia ficticia.
- VoltAgent: [SQL pro](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/ed74d115b7fb7026a22a4f816a8e3250f425e3b4/categories/02-language-specialists/sql-pro.md), [DBA](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/ed74d115b7fb7026a22a4f816a8e3250f425e3b4/categories/03-infrastructure/database-administrator.md) y [data engineer](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/ed74d115b7fb7026a22a4f816a8e3250f425e3b4/categories/05-data-ai/data-engineer.md). Planes, restricciones, restauración y calidad; eliminar metas arbitrarias, context-manager obligatorio y responsabilidades operativas ajenas.
- Wshobson: [database architect](https://github.com/wshobson/agents/blob/c96b5f6552dba32e4492307493ee613581430715/plugins/database-design/agents/database-architect.md) y [database optimizer](https://github.com/wshobson/agents/blob/c96b5f6552dba32e4492307493ee613581430715/plugins/database-migrations/agents/database-optimizer.md). Modelado, trade-offs y rendimiento medible; no fijar motor, modelo, caché ni escalado.
- Fuentes técnicas consultadas: PostgreSQL 19 [restricciones](https://www.postgresql.org/docs/19/ddl-constraints.html) y [EXPLAIN](https://www.postgresql.org/docs/19/using-explain.html); [SQLite Backup API](https://www.sqlite.org/backup.html); [Local-first software (Ink & Switch, 2019)](https://www.inkandswitch.com/essay/local-first/). Adoptar invariantes en almacenamiento, evidencia de planes, respaldos consistentes y operación local con sincronización según contrato. Comprobar versión real del motor; CRDT es opción, no garantía universal de invariantes de negocio.
**Base:** v0.1.0 cubre esquema, índices, migraciones y local-first en general, sin metodología detallada de identidad, compatibilidad, recuperación demostrable o resolución de conflictos.
**Cambio:** Prisma posee almacenamiento e integridad, Nexo reglas y servicios, Atlas decisiones transversales, Platform operación. Prioriza protección de significado y procedencia, evolución segura, medidas comparables y conciliación; sin imponer motores ni dependencias. Permisos originales intactos; pruebas en fixture ficticio.
**Evaluación:** P1–P5 en tests/F05-EQUIPO.md: routing/modelado, migración y restauración, consultas, sincronización y límites. Runtime NOT_RUN; no demostrar superioridad por longitud.


## Perfil 05 — Forja / team-platform
Consulta selectiva del 2026-11-24: siete archivos de tres repositorios fijados a commits de la primera ronda y cinco referencias técnicas públicas localizadas y contrastadas mediante extractos de sus fuentes oficiales. Síntesis propia, sin importar prompts, ejemplos de código, dependencias ni ejecutar harness externos.
- Agency Agents: [DevOps Automator](https://github.com/msitarzewski/agency-agents/blob/8ae6164602c95ca78828b148b9052460ee426885/engineering/engineering-devops-automator.md). Automatización, repetibilidad, entrega y recuperación; descartar cloud/orquestación por defecto, despliegue automático a producción y experiencia ficticia.
- VoltAgent: [DevOps](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/ed74d115b7fb7026a22a4f816a8e3250f425e3b4/categories/03-infrastructure/devops-engineer.md), [Platform](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/ed74d115b7fb7026a22a4f816a8e3250f425e3b4/categories/03-infrastructure/platform-engineer.md), [SRE](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/ed74d115b7fb7026a22a4f816a8e3250f425e3b4/categories/03-infrastructure/sre-engineer.md) y [PowerShell 7](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/ed74d115b7fb7026a22a4f816a8e3250f425e3b4/categories/02-language-specialists/powershell-7-expert.md). Adoptar reducción de fricción, drift, medición, idempotencia, confirmación y manejo de errores; no imponer modelo, context-manager, portal, metas SLO ni caos en producción.
- Wshobson: [DevOps Troubleshooter](https://github.com/wshobson/agents/blob/c96b5f6552dba32e4492307493ee613581430715/plugins/incident-response/agents/devops-troubleshooter.md) y [GitHub Actions Templates](https://github.com/wshobson/agents/blob/c96b5f6552dba32e4492307493ee613581430715/plugins/cicd-automation/skills/github-actions-templates/SKILL.md). Diagnóstico por capas y separación de build/test/entrega; ejemplos con tags mutables, credenciales persistentes o triggers de producción no son configuración aprobada ni se copian.
- Referencias técnicas: Microsoft Learn [ShouldProcess](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-shouldprocess?view=powershell-7.6) y [manejo de errores](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_error_handling?view=powershell-7.6); [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use); [Docker build best practices](https://docs.docker.com/build/building/best-practices/); [Google SRE effective troubleshooting](https://sre.google/sre-book/effective-troubleshooting/). Transferir control de efectos, códigos nativos, mínimo privilegio, referencias verificables y diagnóstico por hipótesis; consultar versión real antes de usar capacidades específicas.
**Base:** v0.1.0 contiene límites operativos, simulación, compatibilidad y validación generales; falta método causal, diferenciación de entornos, cadena de suministro, propiedad/retirada y criterios de salud real.
**Cambio:** Forja posee preparación de entorno, automatización, empaquetado y operación autorizada; Atlas decisiones transversales, Prisma persistencia y consistencia de respaldo, Nexo/Lumen código de aplicación. Reutiliza lo existente, adapta a Windows/Linux y restricciones de conectividad, exige autorización de mutaciones sensibles y distingue diagnóstico/simulación/ejecución. Permisos originales intactos; no introduce herramientas nuevas.
**Evaluación:** FJ1–FJ5 en tests/F05-EQUIPO.md: routing/diagnóstico, automatización e idempotencia, recuperación/propiedad, CI y distribución, autorización. Runtime NOT_RUN; no confundir versión más extensa con superioridad.

## Próximas rondas, una por profesión
6. Faro (team-research): investigación específica de agentes y estándares pertinentes; comparar límites con vecinos y mejorar definición individual.
7. Veritas (team-quality): investigación específica de agentes y estándares pertinentes; comparar límites con vecinos y mejorar definición individual.
8. Bastión (team-security): investigación específica de agentes y estándares pertinentes; comparar límites con vecinos y mejorar definición individual.
9. Ágora (team-editorial): investigación específica de agentes y estándares pertinentes; comparar límites con vecinos y mejorar definición individual.

Las rondas siguientes deben leer prompts concretos y fuentes técnicas por especialidad, actualizar este mismo registro por sección, no crear nueve investigaciones duplicadas ni modificar todo el equipo a la vez. La certificación conjunta sigue F05.3–F05.5 y F07; no instalación definitiva.
