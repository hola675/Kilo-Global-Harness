---
name: vx-team-bootstrap
description: "Inicio del pack unificado: seleccionar capacidades técnicas globales, comprobar instrucciones locales, distribuir permisos por rol y coordinar fases y resultados paralelos con un único líder visible."
metadata:
  version: "1.5.0"
  last_modified: "2026-11-21"
  origin: "vx-unified"
---

# VX — Inicio, sincronización y gobierno del equipo

**Solo `vx-dev-team` es principal visible.** Esta skill gobierna la primera decisión de cada tarea; no lanza automáticamente procesos, subagentes, Git, MCP ni cambios de permiso. Las skills no elevan la ACL del host. El modo Auto sigue siendo elección del operador; `ask` permanece en escritura y shell según rol.

## Gate V0 — versión y contexto antes de implementar (Core 1.5 SOURCE)

Antes de cualquier mutación, incluso para microcambios, el líder registra `BASE_SHA` o `GIT_UNBORN_HEAD`, rama/worktree, paths sucios, origen de la versión y alcance X/Y/Z. Si no puede observar la base, comunica `BASELINE_UNVERIFIED`; no toca rutas con modificaciones ajenas. No crear tags, version bumps ni releases por rutina: distinguir cambio de código de publicación. **La política se aplica desde este bootstrap ya allowlistado**, aunque `vx-version-governance` aún no tenga `permission.skill` en runtime.

Seleccionar por stack real y `TASK_INTENT`, no por marca, utilizando la matriz de `vx-context-routing` como **referencia source**, no como invocación concedida. Prioridad: permisos efectivos → petición expresa → reglas locales estrictas → stack existente → política global. `vx-technology-fit` se consulta solo cuando hay elección tecnológica real; `vx-skill-quality` solo al revisar Skills. **No editar ACL para cargar estas nuevas Skills**, no cambiar `kilo.jsonc` ni instalar nada en HOME hasta autorización aparte.

## Inicio proporcional y mínimo

1. **Intención:** detectar si es consulta, revisión, microcambio o desarrollo por fases. Para microcambio, leer lo indispensable, aplicar una modificación y probar; **no** invocar todo el equipo ni generar un roadmap artificial.
2. **Contexto del trabajo:** leer raíz, `AGENTS.md`, dependencias, estructura y guía del proyecto solo mediante tools permitidas. Seleccionar **capacidades genéricas** desde `routing.capability_routing` por el **tipo verificable de tarea y stack real** (SaaS multitenant, ERP local-first, redes Windows, inventario, flujos empresariales o control industrial). **Nunca enrutar skills por el nombre de un cliente, marca o repositorio**: la adaptación concreta se obtiene de las instrucciones locales. No cargar todas las skills al inicio.
3. **Precedencia:** restricciones del usuario y reglas del proyecto (AGENTS, GOVERNANCE, STATUS, documentación canónica) prevalecen sobre recomendaciones generales de este pack cuando son más específicas o estrictas. Global-only se refiere a instalación de agentes/skills en HOME; **no** borrar ni reemplazar instrucciones propias de proyectos ya existentes.
4. **Meta y plataforma:** `FINAL_GOAL`, `PLATFORM_SCOPE`, `BASELINE`, entregable inmediato, criterio de aceptación y permiso disponible; para trabajo complejo cargar `vx-desarrollo-escalonado` si está en la ACL.
5. **Ruta de especialización:** cada builder carga su skill de dominio únicamente si está autorizada por su **allowlist exacta**. El líder no necesita cargar todas las skills; pasa el perfil, fuentes locales y evidencia conocida en el handoff.
6. **Contexto compartido ligero:** líder conserva **un ledger de tarea**, no una base de datos persistente: `goal, capability_profile, base_sha|GIT_UNBORN_HEAD|GIT_NOT_APPLICABLE, phase, task_id, owner, allowed_paths, depends_on, contract_version, state, evidence`. Se comparte con los hijos solo el fragmento mínimo para su trabajo. **No guardar secretos, clientes, credenciales, contenido privado ni correos**.
7. **Delegación operativa:** identificar primero tareas independientes y lanzar **sus subtareas reales mediante `task(background: true)`** si esa opción existe en el host; máximo cuatro hijos activos y dos escritores de rutas exactas disjuntas (o worktrees aislados verificados). Lanzar los escritores independientes antes de iniciar la investigación propia, sin esperar a cada uno innecesariamente. Mientras los hijos editan, el líder **continúa trabajando en contratos, análisis, tareas de lectura y pruebas de módulos estables fuera de sus archivos**. El DAG `PARALLEL_SAFE` es asesor, NO ejecuta tareas ni reserva rutas. Si el host no expone `background`, foreground secuencial sin declarar paralelismo. Si un contrato depende de otro aún inestable, esperar a la barrera.
8. **Propiedad efectiva:** `task` no crea worktrees ni locks. No compartir cambios Git/lockfiles, dependencias o scripts que muten directorios ajenos entre escritores; no permitir que líder o QA toquen archivos reservados mientras la fase está activa. El permiso `ask` puede ser resuelto por Auto sin diálogo; eso **no** autoriza firewall, secretos, despliegues, migraciones, borrados o cambios de ACL.
9. **Handoff:** el hijo responde `status, task_id, files_changed, tests_executed, contract_version, evidence, blockers`. Solo líder actualiza ledger; `DONE` es entrega del hijo, nunca `VERIFIED`. Al recibir varios resultados, cotejar diff real y versiones de contrato antes de ejecutar tests focalizados.
10. **Barrera y continuación:** al terminar escritores, resolver imports/archivos compartidos mediante un único dueño, probar, revisar independientemente cuando hay riesgo, integrar con reglas Git del proyecto y marcar `VERIFIED` solo con evidencia. Tras un avance, actualizar el roadmap **vivo**, no crear reportes acumulativos. Ante interrupción: `HOLD_RECHECK`; no invocar de nuevo hijos de forma ciega.

## VX Progress V1 — coordinación durante ejecución

Para tareas realmente concurrentes, mantener un **ledger mínimo en la sesión del líder**: `task_id_or_local_ref, owner_agent, allowed_paths, contract_version, depends_on, phase, evidence, last_material_event`. Solo el líder decide estados `VERIFIED` e integración. No guardar el ledger en un repositorio público, lanzar un demonio ni crear archivos permanentes por rutina.

El líder despacha tareas independientes mediante `task(background: true)` **solo si la herramienta disponible lo admite** y no edita los archivos reservados. Mientras trabajan, preparar contratos posteriores, inspeccionar archivos estables y comunicar al usuario avances comprobados. Recuperar resultados por la notificación de finalización de Kilo, no mediante polling ni tarea duplicada. Si no hay background, foreground con estado `BACKGROUND_UNAVAILABLE`.

El contrato de progreso se define en `vx-agent-collaboration`: eventos breves `STARTED / CONTRACT_READY / MILESTONE / BLOCKED / DELIVERED / CORRECTION` más `VERIFIED` reservado al líder. Kilo Swarm puede compartir hitos **solo si `board_post` y `board_read` aparecen y están permitidas para cada participante**. El líder y los seis builders tienen en el nuevo source `board_read/post: allow`, sin afectar a los lectores; si el host no ofrece Board, fallback `task_result` con estado `PROGRESS_CHANNEL_UNAVAILABLE`. Un mensaje del tablero no entrega ni confirma la recepción por otro agente y jamás concede autorización.

Para sesiones de Agent Manager creadas aparte en VS Code, Swarm no se comparte entre sesiones independientes; coordinar por contratos Git/PR y worktrees aislados. No intentar invocar `agent_manager` desde Kilo Desktop si está denegado.

## VX Dev Team V2 — un solo objetivo y gestión de cola

Un usuario solo indica **qué producto, problema o resultado quiere**. El líder deriva `FINAL_GOAL`, stack, riesgos y aceptación del repositorio y la petición; descompone en tareas concretas con `depends_on` y responsables. No obliga a rellenar formularios ni solicita datos que ya pueda observar. Ordena primero prerequisitos e interfaces compartidas y después lanza 1–2 builders independientes en background cuando el host los admita; el resto queda en cola hasta recibir evidencia. La carga simultánea no justifica crear tareas falsas.

**Persistencia opcional por complejidad:** para tareas que crucen sesiones o tengan numerosas dependencias, usar el mismo `vx_task_dag.py` instalado por el pack: `--queue-action sync|report|start|event|verify|resume|reset`; nunca registrar prompts completos o secretos en el archivo SQLite privado. `report` devuelve estados declarados y `ready_queue` por prioridad, no arranca un worker. `start` se registra solo después de un ID de Kilo observado al invocar `task`. El líder comunica hitos con Swarm cuando exista; no tratar un `board_post` como confirmación de lectura ni usarlo para elevar privilegios. Sin Board o sin permiso de bash, continuar en memoria con `task_result`.

**Autonomía realista:** dentro de la sesión activa tomar decisiones de reparto, seguir con trabajo independiente, analizar cambios, actualizar progreso al llegar eventos, verificar entrega y despachar la siguiente wave. Cuando Kilo Desktop se cierre, no prometer actividad en segundo plano: la cola durable conserva estado, pero no ejecuta tareas sin un host. No programar watchers, cron ni redes externas para simular una capacidad faltante.

## Ruta operativa V2.1: el líder no queda esperando

Para trabajo independiente demostrado, el líder establece un contrato por hijo con `write_scope: EXACT_FILES` para cualquier escritor concurrente y despacha las llamadas `task(background: true)` de la primera wave antes de esperar una respuesta. El propio líder **continúa productivamente** con lectura de módulos estables no reservados, contratos de futuras waves, riesgos, evidencias finalizadas y preparación de verificaciones que no escriban archivos compartidos. Ninguna actividad del líder puede modificar las rutas de builders activos, lockfiles, salida generada o estado Git compartido.

Al llegar `task_result` o un hito Swarm auténtico, verificar quién ejecutó las herramientas, estado de tareas y dependencia, no aprobar por mensaje. Si una sesión está `BLOCKED`, mantener sus reservas de archivo/plaza mientras conserve el `host_task_id`, hasta cierre comprobado; usar `resume/reset` según el motor vigente. Sin background auténtico, no simular simultaneidad: ejecutar en foreground y reportar. La cola SQLite no despacha por sí misma y ningún proceso sigue trabajando con Kilo cerrado.

## Escalones de autorización

| Nivel | Ejemplos | Regla |
| --- | --- | --- |
| R0 lectura | localizar, comparar, proyectar cambios | Permitido solo si la herramienta efectiva lo permite; no leer secretos |
| R1 código y pruebas | editar `allowed_paths` exactos y ejecutar tests específicos | Builder `edit/write/apply_patch: ask`, shell `ask` si lo necesita; Auto lo resuelve según host |
| R2 integración Git | rama/commit/PR/CI del proyecto autorizado | Solo integrador dueño del checkout y reglas específicas del repo; no forzar push ni borrar ramas ajenas |
| R3 infraestructura o datos sensibles | producción, permisos IAM, DNS/firewall, D1 remota, migración destructiva, driver Windows, firma, pagos | Necesita autorización específica adicional, evidencia, evaluación de riesgo y rollback; un R1 no la sustituye |
| R4 no permitido | exfiltración, secretos en logs, evadir un bloqueo del host, impersonación, alterar ACL o MCP para terminar tarea | BLOQUEADO |

## Sincronización con `main`

Un `MAIN_ADVANCED` comprobado es **señal de reconciliación**, no autorización de rebase ni trigger de escritura. El líder pausa las tareas afectadas en punto seguro, verifica rama y diff, decide actualizar contratos y pruebas, y retoma solo con base coherente. Un hijo no debe cambiar la rama compartida mientras otro trabaja. Solo el dueño autorizado archiva y elimina su rama después de verificar merge, CI y copia histórica requerida.

## Estado honesto

`BOOTSTRAP_SOURCE_READY` significa que existen estas instrucciones; no demuestra `BACKGROUND_RUNTIME_PASS`, locks de archivos, coordinación intersesión ni instalación en el PC. No generar timers o monitorizadores sin pedido expreso.
