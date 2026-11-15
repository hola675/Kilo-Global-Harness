# VX Evolution — Equipo inicial de desarrollo del Pack VX (propuesta de diseño)

**Fecha:** 2026-11-15. **Estado:** catálogo/personas y colaboración PARA DISEÑO; **los siete alias (Yoan, Daniela, Rafael, Sofía, Valentina, Lucas y Mateo) están CONFIRMADOS por el operador**; su aplicación a Kilo y sus permisos NO están autorizados. El modelo de equipo paralelo es un objetivo explícito, pero NO está habilitado en el runtime. No crear ni cambiar agentes activos, skills, permisos, MCP, `kilo.jsonc`, modelos, HOME, scheduler ni scripts de instalación. **Propiedad:** únicamente agentes y skills del Pack VX (VX-D14). **Entorno objetivo:** Kilo built-in más componentes personalizados VX (VX-D16).

## 1. Diferenciar tres conceptos

1. **Agente nativo Kilo**: proporcionado por Kilo (p. ej., `code` / `plan` según runtime). No pertenece a VX; no se copia, renombra, modifica ni mantiene por el Pack.
2. **Agente VX personalizado**: archivo Markdown `agents/vx-*.md` del Pack, con función/mode/permisos; sus versiones y mejoras sí están dentro del gobierno VX.
3. **Subagente**: un agente invocado como delegado para una tarea delimitada con contexto aislado y resultado al padre; no es necesariamente otro modelo ni otro proceso residente. El modo `subagent` restringe su uso y no convierte un lector en escritor.

Las skills dan instrucciones bajo demanda; los MCP exponen herramientas externas: no son agentes, no se cuentan como integrantes. El selector PowerShell actual devuelve un plan, **no lanza agentes**.

## 1.1. Convención de nombres humanos (propuesta del operador)

**Confirmado:** presentar los siete agentes IA con **nombre humano + especialidad**. El operador confirmó **Yoan, Daniela, Rafael, Sofía, Valentina, Lucas y Mateo**; los IDs técnicos originales permanecen invariables. Ningún alias es identidad humana, firma o autorización de herramientas.

**Distinción obligatoria:** un nombre humano es un **alias visible de un agente de IA**, NO una cuenta real, una persona contratada, la identidad autenticada del operador ni una autorización. Por ejemplo, el agente «Yoan» **no es el usuario humano**, no puede aprobar cambios por él, autoconcederse permisos o firmar solicitudes. Los IDs técnicos `vx-*` permanecen invariables en el registro, la delegación `task`, las pruebas y la trazabilidad. Antes de activar los alias, verificar cómo Kilo expone nombre y descripción en la versión instalada; no presuponer una propiedad de frontmatter `displayName` sin documentación y prueba.

**Principio de comunicación:** «Soy Daniela, agente VX para revisión de diseño web» sería válido; «soy la diseñadora humana Daniela» no lo sería. Los agentes deben comunicar su condición de IA y límites de permisos cuando proceda.

## 2. Catálogo inicial real del repositorio (V4 vigente)

| Nombre visible (propuesto) | ID técnico estable | Modo actual | Especialidad | Escribe |
| --- | --- | --- | --- | --- |
| **Yoan — Líder de Equipo** | `vx-integrador` | `primary` | Coordina, planifica, integra, valida y cierra Git | **Sí**, solo cuando esté autorizado y como único escritor |
| **Sofía — Investigación y Arquitectura** | `vx-researcher` | `subagent` | Investiga código, dependencias, contratos y documentación | No |
| **Rafael — Testeo y Calidad** | `vx-test-analyst` | `subagent` | Diseña estrategias de prueba, escenarios y cobertura de regresión | No; no ejecuta tests |
| **Valentina — Ciberseguridad** | `vx-security-reviewer` | `subagent` | Revisión de permisos, autenticación, inyección y secretos | No |
| **Lucas — Auditoría y Revisión** | `vx-inspector` | `subagent` | Revisión independiente del diff y coherencia de evidencias | No |
| **Daniela — Diseño Web y UX/UI** | `vx-frontend-adviser` | `subagent` | Revisa diseño, accesibilidad, frontend y experiencia de usuario | No; aún no implementa interfaz |
| **Mateo — Cloudflare y Serverless** | `vx-workers-adviser` | `subagent` | Revisa Workers, KV, R2, D1, colas y bindings | No |

**Los siete nombres humanos fueron confirmados como identidad de presentación, pero no se han aplicado a Kilo ni implican cambios de permisos.** **No crear nuevos agentes equivalentes sin comprobar brecha funcional.** Los siete nombres actuales se mantienen como candidatos de la primera versión del Pack. Ningún rango `junior/senior/líder` se atribuye por la descripción; V4.6 solo tiene evidencia declarativa y pruebas sintéticas.

### Primera escuadra operativa de desarrollo VX

- **Coordinación y único escritor:** `vx-integrador`. Kilo `code` nativo sigue disponible en el entorno limpio para trabajo directo, pero no trabaja a la vez como segundo escritor de la misma rama; para implementaciones normales se puede elegir uno u otro como responsable, no ambos simultáneamente.
- **Descubrimiento:** `vx-researcher`.
- **Diseño de pruebas:** `vx-test-analyst`.
- **Revisión de seguridad:** `vx-security-reviewer` cuando hay archivos sensibles, instalación, permisos, autenticación, suministro de paquetes o MCP.
- **QA final:** `vx-inspector` después del diff. Su dictamen no sustituye pruebas ni aprobación humana.
- **Especialistas opcionales:** `vx-frontend-adviser` y `vx-workers-adviser` solo en proyectos de esas clases.

**Regla de capacidad inicial en modo STRICT actual:** hasta 3 lectores concurrentes **cuando sea útil** y **un escritor máximo en el mismo worktree**. **Objetivo futuro explícito: modo PARALLEL_WORKTREES con dos o más escritores simultáneos, cada uno en un worktree y rama temporal distintos, supervisados por Yoan y con integración serializada.** La excepción a una sola rama temporal y los permisos de nuevos escritores requerirán autorización independiente y tests; no están activados hoy. No invocar los seis subagentes en cada cambio; tareas triviales pueden usar cero. Los subagentes no ejecutan ni manipulan archivos: el coordinador debe ejecutar y comprobar pruebas reales si cuenta con permisos. Las skills del Pack actual son `vx-engineering-harness` y `vx-evolution-core`; otras citadas en perfiles V4 son sugerencias, **no son componentes automáticamente incluidos**.

## 3. Primer ciclo de desarrollo propuesto

1. **Solicitud:** operador describe objetivo, alcance, aceptación, repositorio y riesgos. El coordinador abre expediente mínimo con tarea y versión.
2. **Diagnóstico:** `vx-researcher` localiza fuentes; `vx-test-analyst` define pruebas; seguridad/UX/Workers entra solo si corresponde.
3. **Plan:** el coordinador sintetiza hallazgos, distingue `HECHO`, `DECLARADO`, `NO_VERIFICADO`, `NO_MEDIDO`, acuerda cambios mínimos. No cambiar permisos ni publicar automáticamente.
4. **Construcción:** usar modo STRICT con una rama `work/*` y un escritor en el mismo worktree para tareas pequeñas. **Cuando se autorice PARALLEL_WORKTREES**: Yoan descompone la tarea en contratos independientes, abre una rama temporal y un worktree por escritor, ejecuta sesiones Kilo Agent Manager aisladas, conserva `main` única rama permanente y prepara integración de PRs según DAG y CI. Sin worktrees paralelos sin consentimiento explícito; los subagentes `task` actuales continúan solo lectura.
5. **Pruebas:** ejecutor autorizado corre unit/integration/build y registra códigos de salida; el analista de pruebas no afirma haberlas ejecutado. Tests sintéticos no equivalen a validación en Kilo real.
6. **Revisión:** `vx-inspector` revisa diff y cobertura; `vx-security-reviewer` analiza solo riesgos específicos distintos. Corregir, volver a comprobar, abrir PR.
7. **Integración:** combinar las ramas de implementación en orden de dependencias, revisar interfaces/artefactos y conflicts, ejecutar CI de integración, revisión independiente, autorización de merge según política, validación de `main`, limpieza de cada rama temporal propia. No deploy ni tocar HOME real sin autorización específica.
8. **Evolución:** con evidencia real, VX registra oportunidad de mejorar un componente VX, genera candidato versionado y lo somete al mismo ciclo. No promoción automática ni autoaprobación.

### Ejemplos de selección contextual

| Tarea | Lectores previos | Implementa | Cierre |
| --- | --- | --- | --- |
| Contrato de aprobación VX | Researcher + Security + Test | Integrador | Inspector + CI |
| Script de respaldo/instalador VX | Researcher + Security + Test | Integrador | Inspector + pruebas de rollback en HOME sintético |
| Interfaz de diagnóstico VX | Frontend + Test (Researcher opcional) | Integrador o Code por turno | Inspector + pruebas visuales reales cuando disponibles |
| MCP catálogo VX | Researcher + Security | Integrador | Test + Inspector (sin conectar servidores de terceros) |
| Cambios en Workers ajenos a VX | Fuera de la administración **VX Evolution**; solo equipo Kilo usado para desarrollo autorizado del proyecto del usuario, no evolución del agente ajeno | Kilo Code según tarea autorizada | Nunca publicar tercero como actualización VX |

## 3.1. Organización colaborativa real (objetivo futuro)

El equipo **no se limita a reuniones de agentes lectores**: el resultado esperado es que varios implementadores programen simultáneamente, compartan contratos e integren entregas. En el Pack inicial, el único perfil VX de coordinación es `vx-integrador`, mientras los seis subagentes son **solo lectura**. Para arrancar sin crear roles redundantes se podrán usar sesiones independientes del agente **nativo `code` de Kilo** como escritores bajo Agent Manager, cada una con worktree propio y asignación exclusiva; esto queda sujeto a validación del runtime y autorización puntual. A medio plazo se podrá ampliar el permiso de Daniela para frontend, Rafael para tests y otros perfiles **solo mediante nuevas versiones auditadas**, no por cambiar nombres.

La **comunicación de una misma sesión** puede apoyarse en resultados de `task` o Swarm, mientras que las sesiones independientes de Agent Manager necesitan artefactos de coordinación/versiones explícitas; no se garantiza un bus común. Cada línea de trabajo deberá entregar contrato, diff, pruebas y dependencias, y Yoan deberá incorporar todo en orden. [Personas y relaciones](VX-PERSONAS-RELACIONES-V1-20261115.md) · [Permisos](VX-PERMISOS-Y-AUTONOMIA-V1-20261115.md) · [Registro declarativo](../registry/vx-organization-graph-v1.proposal.json).

**La estructura futura se hace ramificada cuando haga falta**, pero no se crea un manager por un subordinado ni se asignan niveles de experiencia sin pruebas. `reports_to` es jerárquico y acíclico; las consultas cruzadas son libres; dependencias de tareas deben formar DAG. La creación de nuevos agentes y departamentos se vincula a calidad/costo medidos en V4.8 y a aprobación humana.

## 4. Expansión futura, sin crear agentes ahora

Los huecos probables a estudiar con pruebas reales son especialista de instalador/Windows, curador de catálogo MCP, analista de métricas y responsable de documentación. **Inicialmente son capacidades o skills candidatas para el equipo existente**, no nuevos agentes preinstalados. Solo añadir un agente VX cuando exista una necesidad repetida, test de valor incremental contra configuración de un solo agente, revisión de permisos, versión/manifest y aprobación.

## 5. Puertas de aceptación antes de activar el primer equipo

- Verificar sintaxis/configuración global de los siete Markdown y registro V4; que Kilo los muestre, sin duplicados de otras fuentes.
- Probar una delegación `task` de solo lectura con evidencia de identidad del ejecutor y salida; una sesión `completed` por sí sola no verifica llamada interna a skill.
- Probar una tarea VX sintética con único escritor, pruebas, revisión independiente y cierre Git.
- Registrar coste/tiempo solo cuando exista medición auténtica; ninguna puntuación de seniority hasta V4.8.
- Si hay problemas, mantener los siete roles existentes, con orquestación secuencial y bloqueo de publicación hasta solucionarlos.

## 6. Decisión pendiente de dirección

**Confirmar el catálogo final de alias** (Yoan, Daniela, Rafael, Sofía, Valentina, Lucas y Mateo) y si la composición actual de siete agentes, un único escritor y hasta tres lectores sigue siendo el Pack VX inicial. **Los ejemplos de nombres del operador no equivalen todavía a aprobar todas las nuevas denominaciones.** En caso de necesitar un desarrollador backend que escriba de forma independiente, evaluar primero si `vx-integrador` o Kilo nativo `code` resuelven ese papel; no crear un octavo agente por inercia. Esta propuesta **no es autorización de instalación ni cambio de permisos**.

Fuentes internas: `agents/vx-*.md`, `registry/vx-agent-registry-v4.json`, `docs/OPERACION-EQUIPOS-V4.md`, `docs/VX-EVOLUTION-ROADMAP.md`. Documentación Kilo: https://kilo.ai/docs/customize/custom-subagents y https://kilo.ai/docs/customize/custom-modes.
