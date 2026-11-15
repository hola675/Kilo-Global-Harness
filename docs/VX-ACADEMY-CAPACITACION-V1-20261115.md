# VX Academy — Capacitación, catálogo de capacidades y aprendizaje verificable

**Versión:** 0.1.0-propuesta · **Fecha:** 2026-11-15 · **Estado:** diseño no ejecutable, `NO_ACTIVO`. No modificar Kilo HOME, agentes, skills, MCP, `kilo.jsonc`, SQLite real, permisos, modelos, tareas programadas ni instalador. Se integra en el roadmap conceptual bajo **VX-D22**, pendiente de consentimiento para cualquier implementación.

## 1. Objetivo

Diseñar una capa de capacitación **mínima, medible, versionada y escalable** para siete agentes VX propios, equipos y futuros departamentos. La capacitación se asignará **por tarea y necesidad**, no cargando en cada agente todas las herramientas o skills posibles. El modelo evita tres errores:

1. **Skill existente ≠ competencia demostrada.** Una skill en disco o metadatos Kilo no certifica un resultado.
2. **Herramienta disponible ≠ permiso concedido.** Un rol, nivel profesional, equipo, departamento, docente o mentee no puede ampliar `edit/bash/mcp/task/agent_manager` automáticamente.
3. **Capacidad del equipo ≠ suma de privilegios.** El equipo puede completar tareas distribuyendo responsabilidades sin que cada integrante reciba todos los permisos ni materiales.

**Scope C (VX-D14):** este motor evalúa, forma y versiona **solo agentes/skills propios VX**. Puede conocer referencias externas de documentación, herramientas nativas de Kilo y MCP existentes por compatibilidad; no administra, copia, evalúa rendimiento ni actualiza código/instrucciones de terceros automáticamente.

## 2. Modelo semántico: siete entidades distintas

| Entidad | Qué captura | Qué NO significa |
| --- | --- | --- |
| `capability` | Capacidad técnica atómica: `qa.regression-design`, `ui.accessibility-audit`, `coordination.handoff` | No concede permiso ni implica experiencia |
| `skill_artifact` | Skill VX versionada (fuente, hash y `SKILL.md`); o referencia externa `EXTERNAL_UNVERIFIED` | No significa que Kilo la haya cargado ni que el usuario la tenga instalada |
| `tool_requirement` | Herramienta nativa o MCP concreta, con operación y efectos | No significa que esté conectada/permitida |
| `entitlement` | Decisión explícita de `allow/ask/deny` de Kilo, validada en runtime | No se hereda de cargo ni seniority |
| `experience_record` | Intento observable de tarea con versión de agente/skill/herramienta, pruebas, resultado y revisor | Ni autodeclaración de PASS ni observación de errores equivalen a evaluación |
| `training_assignment` | Necesidad y currículo asignado por rol/tarea, motivado por brecha medida | No instala automáticamente skill/MCP ni cambia persona |
| `teaching_qualification` | Evidencia de enseñanza exitosa: un aprendiz mejora en pruebas independientes frente a línea base | El mentor no gana permiso para editar a otro agente |

El sistema debe separar **`DECLARADO`, `DISPONIBLE`, `PERMITIDO`, `EJECUTADO`, `VERIFICADO` y `NO_MEDIDO`**. No combinar esos estados en una puntuación inventada.

## 3. Catálogo por niveles: pack, departamento, equipo, agente y tarea

```text
Pack VX versionado
 ├─ Catálogo de capacidades, artefactos VX y referencias MCP
 ├─ Departamento virtual = currículo compartido, NO permiso
 │   └─ Equipo = objetivos y competencias necesarias para un proyecto
 │       └─ Agente VX = núcleo mínimo + especialidad + experiencia demostrada
 │           └─ Tarea = activar SOLO habilidades/herramientas elegibles necesarias
 └─ Historial privado = pruebas, evaluaciones y propuestas, sin conversaciones
```

El núcleo mínimo compartido es **la política de seguridad/trazabilidad** y no una copia de decenas de skills. Un currículo departamental describe lo que *puede aprenderse*, no lo que se inyecta a todos los agentes. Un agente perteneciente a dos equipos no obtiene la unión de todas las skills/todas las herramientas de ambos. La ejecución exige resolver el contexto **agente + tarea + permiso efectivo + instalación + disponibilidad + versión + evidencia**.

### Matriz curricular inicial por personas IA

| Alias e ID | Capacidades nucleares por estudiar / mantener | Herramientas mínimas según configuración actual | Skill VX hoy o candidata | Aprender/enseñar/dirigir |
| --- | --- | --- | --- | --- |
| **Yoan** `vx-integrador` | `coordination.task-split`, `coordination.contracts`, `git.integration`, `evidence.verification` | `read/glob/grep/skill` declarados; `edit/bash/task` podrían heredarse: verificar antes de usar | **Actuales:** `vx-engineering-harness` y `vx-evolution-core` (esta última solo en tareas sobre VX). **Candidata:** `vx-parallel-integration` | Coordina; **no** tiene condición docente verificada ni derecho de aprobar |
| **Daniela** `vx-frontend-adviser` | `ui.semantic-audit`, `ui.accessibility-audit`, `ui.component-review` | `read/glob/grep/lsp`; `edit/bash/mcp/task` denegados en fuente | **Candidata:** `vx-ui-audit` (NO EXISTE) | Consultora UX; futura implementación o mentoring solo tras evaluación y permisos |
| **Rafael** `vx-test-analyst` | `qa.test-design`, `qa.negative-cases`, `qa.regression-analysis` | `read/glob/grep/lsp`; sin ejecutar tests ni editar | **Candidata:** `vx-qa-test-design` (NO EXISTE) | Diseña casos y enseña metodología únicamente al certificarse como mentor |
| **Sofía** `vx-researcher` | `research.source-verification`, `research.dependency-map`, `architecture.contracts` | `read/glob/grep/lsp`; sin terminal/MCP | **Candidata:** `vx-research-traceability` (NO EXISTE) | Puede proponer manuales técnicos con fuentes, no impartir capacitación certificada |
| **Valentina** `vx-security-reviewer` | `security.threat-model`, `security.auth-review`, `security.least-privilege` | `read/glob/grep/lsp`; sin explotación ni terminal | **Candidata:** `vx-threat-model-review` (NO EXISTE) | Revisa riesgos y currículos de seguridad; no concede permisos |
| **Lucas** `vx-inspector` | `review.diff-audit`, `review.false-positive-control`, `review.evidence-integrity` | Lectura + Git status/diff/log por allowlist declarada, resto denegado | **Candidata:** `vx-independent-review` (NO EXISTE) | Revisión independiente; no será auditor único de su propia capacitación |
| **Mateo** `vx-workers-adviser` | `cloudflare.bindings`, `cloudflare.retry-idempotency`, `cloudflare.dev-stage-review` | `read/glob/grep/lsp`; sin MCP/Wrangler/DEPLOY | **Candidata:** `vx-workers-audit` (NO EXISTE) | Asesor de infraestructura; demostraciones con entorno sintético antes de ampliar herramientas |

**Importante:** las seis skills candidatas están nombradas para explorar necesidades; **no se generan ni instalan en esta fase**. La fuente principal contiene exactamente **dos** skills propias VX en `skills/`. Los nueve perfiles de `registry/vx-agent-registry-v4.json` citan nombres como `frontend-design`, `wrangler` o `verification-before-completion`: son **recomendaciones de origen externo o disponibilidad NO_VERIFICADA**, no assets que deba empaquetar VX o instalar sin consentimiento.

### Currículos de equipo y departamento

| Unidad potencial | Programa compartido (catálogo, no carga) | Certificación que exigiría |
| --- | --- | --- |
| Coordinación / Delivery | Estimación, división de tareas, Git integración, pruebas, gestión de bloqueo | Tarea integrada y revisada sin cambios no autorizados |
| Ingeniería / Diseño | Accesibilidad, design systems, contratos UI/backend | Código/documento visual contrastado con aceptación |
| Calidad | Diseño de pruebas, falsos positivos, regresiones, evidencias | Reproducir y corregir casos ciegos positivos y negativos |
| Seguridad | Riesgos, privilegios, autenticación, revisión de dependencias | Hallazgos correctos y ausencia de falsos positivos graves |
| Arquitectura / Investigación | APIs, contratos, procedencia, lectura de repositorios | Veracidad y pertinencia de fuentes, dependencias coherentes |
| Plataforma | Workers/bindings/MCP, migraciones, ensayos DEV | Validación segura de fixtures; sin confundir plan con deploy |

Los departamentos son **plantillas futuras**, no entidades que se activan al crear el catálogo. Cursos compartidos no equivalen a acceso de todos los integrantes.

## 4. Integración con el comportamiento REAL de Kilo

**Fuentes oficiales:** https://kilo.ai/docs/customize/skills ; https://kilo.ai/docs/customize/agent-permissions ; https://kilo.ai/docs/automate/mcp/using-in-kilo-code

- Kilo descubre metadatos `name/description/path` de skills al iniciar la sesión y lee `SKILL.md` **bajo demanda**. En el sistema actual el pool es compartido: etiquetar una skill como «solo Daniela» en nuestro JSON **NO la oculta** de otros agentes. Para control estricto de exposición por rol haría falta investigar una API/ruta soportada, crear perfiles realmente aislados o mejorar la selección sin forzar falsas garantías.
- Publicar cientos de skills VX, aunque no se carguen completas, **aumenta el catálogo de metadatos en contexto**. Mantener pocas skills precisas; documentación larga en `references/`, plantillas en `assets/`, y evitar duplicidad.
- Skills globales de fuente confiable **pueden incluir comandos de shell** que disparan una petición de permisos al cargarse. Auditar referencias/scripts, evitar autoejecución, no tratar skills descargadas como seguras y estudiar `KILO_DISABLE_SKILL_SHELL` antes de cualquier empaquetado que incluya shell.
- Los MCP existentes permanecen intactos (VX-D17). La capa Academy solo referenciará identidad de capacidades y disponibilidad. Un MCP configurado puede estar desconectado (`needs_auth/failed`); el permiso de una herramienta MCP es distinto del permiso de conexión y del conocimiento del agente. Nunca activar, instalar ni configurar MCP sin aprobación individual.
- Los permisos de Kilo son `allow/ask/deny`, con prioridad de patrones de último match. Para toda elevación de `edit/bash/task/mcp/agent_manager`, verificar permisos efectivos y riesgos de herencia en el runtime real; el catálogo de Academy **no** es un sistema de seguridad que pueda sobreescribir los controles de Kilo.

## 5. Ciclo de formación y evaluación (tres puertas independientes)

1. **Diagnosticar:** tarea concreta fallida o brecha demostrada, evidencia independiente, versiones y alcance. Comparar si falta skill, herramienta, permiso, contexto, fuente vigente o si es simplemente un caso demasiado difícil. Cualquier inferencia sobre un modelo debe quedar `HIPOTESIS`.
2. **Proponer currículo:** competencia objetivo, material VX o referencias, docente candidato (si cumple requisitos), skill/version, herramienta necesaria, tiempo/costo cualitativo, riesgos y prueba antes/después. Solo se propone; no edita perfiles.
3. **Ensayar aislado:** misma batería de criterios con casos diferentes equivalentes, incluyendo casos negativos y novedad; registrar resultado del agente, hash de artefactos y revisión externa. No copiar código privado ni conversaciones. Una skill cargada no equivale a ejecución verificada.
4. **Comparar:** resultados objetivos antes/después: éxito sobre tareas representativas, precisión/falsos positivos, regresiones, latencia/tokens cuando estén disponibles, invocaciones de skills y herramientas, errores de coordinación. Marcar muestras insuficientes como `NO_MEDIDO`/`EVIDENCIA_INSUFICIENTE`. Ninguna promoción por fixture público.
5. **Aprobar candidato:** revisor distinto de autor/mentor, consentimiento del operador para incorporar **nueva versión de componente VX**. No copiar conocimientos externos protegidos ni reescribir skills o agentes sin autorización.
6. **Publicar solo cuando V4.7 esté habilitado:** la versión candidate pasa por preview, autorización efectiva, backup y rollback. Hoy `approval_granted=false` / `apply_supported=false`, por lo que **no se instala nada**.
7. **Monitorear solo señales autorizadas:** observar regresiones en actividades reales sin guardar prompts/output privados. Revertir si se demuestra degradación y la operación futura de rollback está autorizada.

## 6. Cuándo un agente puede enseñar a otro

Una identidad líder no se convierte automáticamente en docente; `teaching_qualification` se concede solo a una **competencia específica**, con versión y alcance:
- **EXPERTISE_VERIFICADA:** resultados positivos y negativos con casos nuevos y revisión independiente, no por autodeclaración.
- **MATERIAL_AUDITADO:** guía, ejemplo sintético, rúbrica y fallos frecuentes versionados, sin secretos ni contenidos privados; marca licencia/procedencia.
- **TRANSFERENCIA_MEDIDA:** el aprendiz supera una evaluación posterior independiente frente a su línea base. Repetir en un segundo escenario para descartar simple memorización; umbrales numéricos exactos se fijarán tras piloto, nunca inventar métricas.
- **REVIEWER_SEPARADO:** no puede ser simultáneamente mentor, único juez y aprobador. Fallo de la enseñanza no degrada automáticamente al aprendiz.
- **SIN_PERMISO_TRANSFERIDO:** enseñar no puede conceder herramientas, escribir el prompt global del aprendiz, cambiar departamento, ascender ni alterar la instalación de Kilo. Mentoría es una propuesta versionada.

Un agente puede **dirigir** un equipo solo si tiene capacidad organizativa evaluada y se crea la relación aprobada en el DAG `reports_to`; **no** por tener permiso `task`, por saber un framework, por el título «senior» o por enseñar una skill. La delegación `task` está controlada en Kilo y el destinatario conserva sus permisos.

## 7. Registro de experiencia — privacidad, procedencia y anti-gaming

`experience_record` propuesto: `record_id`, `agent_id`, `agent_version`, `capability_id`, `skill_id/version/sha?`, `tool_operation?`, `case_id`, `suite_version`, `difficulty`, `outcome`, `verification_method`, `independent_reviewer_id?`, `artifact_hash?`, `run_id?`, `started_at/finished_at?`, `confidence`, `source=DECLARED|RUNNER_VERIFIED|INDEPENDENTLY_REVIEWED`. Nunca prompt, código de terceros, contenido cliente, tokens/API keys, transcripciones ni rutas absolutas; usar IDs opacos/HMAC local si hace falta.

- El agente **no escribe notas propias en su certificado** ni selecciona casos/revisor para promocionarse.
- El motor anterior V4.6.1/2 solo genera datos **declarativos/sintéticos**. No migrarlos a `INDEPENDENTLY_REVIEWED` ni a PASS real por cambiar de esquema.
- Evidencia de enseñanza: `teacher_id`, `learner_id`, `capability_id`, `lesson_version`, `baseline_suite_hash`, `transfer_suite_hash`, `result`, `reviewer_id`; no crear relación docente/subordinado por deducción.
- Se fija la versión de modelo/contexto/herramientas para comparar sin atribuir una mejora a una skill si otros factores cambiaron. Evitar `N` o porcentajes ficticios en el informe.
- Guardar localmente con política de mínimo dato y aprobación de retención todavía pendiente; sin cloud, sin scheduler y sin observación invasiva.

## 8. Selección y control de carga — algoritmo futuro, NO implementado

Dado `task_contract`, el selector construirá `eligible_capabilities` desde rol, tarea, versiones aprobadas y evidencia; recomendará solo **1–3 skills relevantes (umbral inicial a medir)** y el conjunto mínimo de herramientas necesarias. `resolved_tools = installed_and_connected ∩ runtime_allowed ∩ task_approved ∩ role_need`; una recomendación nunca vence un `deny`. Si falta herramienta, generar `NEEDS_APPROVAL` o `BLOCKED`, nunca autoañadir MCP.

Para medir si realmente evitamos sobrecarga: capturar **solo si están disponibles** nombre/version de skills elegidas, invocación observada, redundancias, tasa de tareas completadas, conflictos de herramientas, regresiones, tokens y tiempo. Distinguir **costo del catálogo de metadatos** de **costo de cargar skill completa** y **costo de inyectar instrucciones MCP**. Las métricas de tokens/costo permanecen `NO_MEDIDO` hasta disponer de origen verificable. Comparar el selector con el método simple para no crear un «academia» que cuesta más de lo que ahorra.

## 9. Gobierno de versiones y grafo de dependencias

`pack_version` → `organization_version` → `curriculum_version`; cada `agent_version`, `skill_artifact_version+sha` y `teaching_qualification_version` es independiente. En una actualización, reconstruir compatibilidad y versiones antes de publicar; detectar ciclos de prerrequisitos formativos, duplicados y permisos implícitos. **No copiar todas las skills del departamento al agente**. Mantener `reports_to` acíclico, `prerequisite_of` acíclico y `collaborates_with` bidireccional permitido.

## 10. Pruebas de aceptación del futuro motor

- El catálogo falla con IDs inexistentes, skills duplicadas, referencias o prerequisitos cíclicos, tipos inesperados y versiones inválidas.
- Nunca declarar `CERTIFICADO` sin evidencia de runner y revisión separada.
- Curso en `team/department` no modifica permisos ni crea carga automática por agente.
- No permitir docencia y verificación de la misma actividad por el mismo individuo agente; impedir autoascenso.
- Skills VX se limitan a propias; las herramientas MCP existentes son referencias externas, no activos bajo control de Academy.
- Un `deny` real bloquea una herramienta aunque el catálogo de curriculum la mencione.
- Evaluar skill candidata vs baseline con pruebas positivas/negativas y versión fija de prompt/modelo.
- Ensayos en HOME y worktrees sintéticos sin afectar credenciales, agentes globales o datos privados; pruebas de CLI y Kilo reales separadas.

## 11. Decisiones pendientes y relación con el roadmap

**Confirmación pendiente:** nombre «VX Academy», regla de recomendación de 1–3 skills por tarea, perfil de exposición/aislamiento de skills de Kilo, mínimos de evidencia para docencia/promoción, retención local de historial formativo, catálogo de herramientas por equipo y cómo elegir currículos opcionales. La política de permisos de Kilo, el alcance C y el estado no ejecutable no se reabren.

**Próximas fases propuestas:** V4.8 diseñar pruebas reales, diagnósticos de brechas y sistema de experiencia; V4.8.x diseñar catálogos y asignación sin permisos; V4.9 (etiqueta provisional) docencia/supervisión/eficacia comparada; V5.0 crecimiento organizativo gobernado. La numeración es una **propuesta**, no release ni autorización.
