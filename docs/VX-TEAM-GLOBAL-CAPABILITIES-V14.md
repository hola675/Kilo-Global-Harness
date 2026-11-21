# VX Core 1.4 — inicio, skills globales y trabajo simultáneo

**Estado:** SOURCE candidato; falta CI, revisión independiente, merge y actualización de Kilo Desktop. No afirmar runtime paralelo ni instalación en el PC antes de comprobarlos.

## Evolución VX Progress V1 — Core VX 1.5 (SOURCE 2026-11-21)

**Propósito:** aprovechar las herramientas nativas Kilo para que el equipo actual comparta hitos, bloqueos e interfaces estables mientras desarrolla en paralelo, **sin un segundo líder, scheduler, MCP ni servidor de mensajería**. Se añade el contrato `vx-progress-event/1` a la skill `vx-agent-collaboration`, `vx-team-bootstrap`, el líder `vx-dev-team` y los seis builders existentes. Ninguna nueva Skill ni agente; no aumenta los 18/57 activos del manifiesto.

**Herramientas verificadas en la documentación oficial Kilo:**
- `task(background: true)`: subagente real que comparte el workspace y regresa el resultado al líder sin bloquearlo; **no crea worktree**. Si la tool no expone `background`, fallback foreground sin afirmar simultaneidad.
- Kilo Swarm: `board_post` / `board_read` permite comunicar hitos entre sesión principal y descendientes `task`, no entre sesiones top-level separadas de Agent Manager. Los posts se almacenan pero no prueban entrega/lectura; nunca autorizan operaciones.
- Agent Manager (extensión VS Code): worktrees/sesiones aisladas para ramas independientes. El líder Kilo Desktop mantiene `agent_manager: deny`; no se activa con este cambio.

**Canales y estados:** el ledger de progreso vive únicamente en la sesión del líder. Eventos `STARTED`, `CONTRACT_READY`, `MILESTONE`, `BLOCKED`, `DELIVERED`, `CORRECTION`. El líder emite `VERIFIED` solo después de comprobar tool trace, diff y pruebas focalizadas. En laboratorio sin Git, `GIT_NOT_APPLICABLE`; sin ID real usar referencia local asignada y no inventar ID de Kilo. Evitar porcentajes o estimaciones de progreso sin medición.

**Puerta de permisos actual:** `board_read: deny` y `board_post: deny` en el líder. Esta fase mantiene las ACL exactas, el modo Auto, Kilo Desktop y `kilo.jsonc` **sin cambios**. Mientras persista `deny`, `PROGRESS_CHANNEL_DENIED` y avances solo por `task_result` del hijo al líder; **no existe mensajería en tiempo real validada**. Para habilitar la pizarra posteriormente hace falta aprobar el cambio puntual de ACL, reinstalar el paquete actualizado y verificar las herramientas en sesiones reales.

**Prueba focal posterior (no ejecutada todavía):** dos builders con archivos HTML/JSON distintos en un laboratorio; llamadas `task(background: true)` observadas y solapadas mientras el líder investiga un tercer archivo; al terminar, contrastar `task_result`, herramienta que escribió cada uno, ausencia de edición cruzada y verificación independiente. Solo después de aprobar `board_read/post`, añadir prueba con `MILESTONE` publicado, lectura del otro participante y evidencia de entrega/recepción separadas. No repetir RT-01/RT-02: eran foreground, y RT-02 carecía de traza de autoría del hijo.

**Referencias:** https://kilo.ai/docs/automate/agent-manager · https://kilo.ai/docs/automate/agent-manager-workflows · https://kilo.ai/docs/automate/tools · https://kilo.ai/docs/customize/agent-permissions .

## Objetivo final

Un único agente principal `vx-dev-team` clasifica tareas, carga la skill de arranque solo si hace falta, delega implementación de código a builders con permisos efectivos y mantiene actividad útil mientras dos subagentes independientes trabajan. Integrar los resultados sin modificar accidentalmente archivos compartidos y sin crear skills ligadas a marcas o repositorios.

## Cómo se inicia

1. El operador selecciona `vx-dev-team` en Kilo Desktop y conserva `Auto`; puede usar `/vx-equipo` para activar el flujo. El comando carga las instrucciones del líder; **no ejecuta por sí mismo procesos, ni un scheduler, ni un modelo adicional**.
2. El líder identifica el tipo de tarea, el stack, la raíz, el HEAD (o `GIT_UNBORN_HEAD`), reglas locales `AGENTS.md`, contratos y prioridad; si el trabajo es complejo, carga `vx-team-bootstrap` desde su allowlist.
3. Selecciona una o más skills globales **por necesidad técnica**, no por marca. Se pueden combinar SaaS, inventario, flujos y ERP si el proyecto contiene esas capacidades. La documentación local estricta prevalece.
4. Para cambios simples resuelve directamente; para cambios independientes prepara `task_id`, dueño, `allowed_paths` exactos, `depends_on`, contrato estable y aceptación. Lanza los hijos mediante `task(background: true)` si lo expone la herramienta de Kilo Desktop. No simular background en texto ni usar el DAG como ejecutor.
5. Mientras dos escritores editan archivos distintos, el líder investiga otros módulos o prepara el siguiente contrato; nunca edita ni valida como definitiva una ruta en escritura. La barra de sincronización recopila cambios, lee archivos finales, integra archivos compartidos con un único owner, ejecuta pruebas focalizadas, revisa y cierra PR/CI.
6. Retomar con `HOLD_RECHECK` si hay interrupción; no duplicar subagentes por retrasos. Reconciliar `origin/main` solo al cerrar la fase y con un escritor Git por worktree. Solo se borran ramas propias tras PR/CI, mediante procedimiento de respaldo.

## Skills del nuevo pack

| Habilidad global | Cuándo cargarla | No hacer |
| --- | --- | --- |
| `vx-team-bootstrap` | Coordinación del líder, inicio y selección de especialidades | No convertirse en scheduler/dispatcher |
| `vx-saas-multitenant-cloud` | SaaS web, SSR, edge, membresías y aislamiento tenant | No usar DB de producción para tests |
| `vx-erp-localfirst-modular` | ERP, dominios, multi-sede, sync offline, perfiles de despliegue | No imponer stack sin benchmark |
| `vx-windows-network-systems` | Proxy, VPN autorizada, WFP, TLS y servicios Windows | No instalar drivers sin firma |
| `vx-inventory-reconciliation` | Stock, combustible, custodia, ledger, importación TPV y cuadres | No confundir backoffice con TPV |
| `vx-enterprise-workflows` | RRHH, planes, acuerdos, actas, aprobaciones, consolidación | No inventar jerarquías o datos reales |
| `vx-industrial-control-safety` | PLC/PCC, supervisión industrial, adaptadores, metrología | No manipular equipos reales sin gate |

Las skills anteriores `vx-tauri-desktop`, `vx-conectividad-dispositivos`, `vx-desarrollo-escalonado`, las capacidades de Frontend/Backend/QA/Datos y las de seguridad se conservan; total **18 agentes y 53 skills**. No hay skills especiales llamadas `vx-vecidya`, `vx-multinexo`, etc. Ejemplo: un proyecto como Vecidya puede combinar **SaaS + Frontend/UX + Cloudflare + Editorial**, tomando su versión y gobernanza de su repo, sin que la skill dependa de su nombre.

## Roles, permisos y niveles

- Un líder visible; 17 hijos ocultos: asesores read-only y seis builders (Frontend, Backend, Datos, QA, Docs y Editorial).
- ACL de `skill` por builder: `"*": deny` y allowlist exacta de capacidades compatibles con el rol. **Skill no concede bash, MCP o edit por sí misma**.
- Builders: `edit/write/apply_patch: ask`; `task: deny`; `agent_manager: deny`. Editorial además `bash: deny`. Kilo Desktop `Auto` puede aprobar `ask` en runtime; no equivale a permisos de infraestructura o producción.
- R0 lectura y análisis; R1 código y tests; R2 rama/PR/CI; R3 producción, datos/firmas/firewall/drivers requiere autorización adicional específica. Nunca ampliar a R3 mediante un permiso R1.
- Por defecto un escritor por worktree Git. La excepción para **dos escritores simultáneos** en un mismo workspace requiere archivos literales exactos, listas disjuntas, `write_scope: EXACT_FILES`, contratos independientes y ninguna operación Git concurrente. Hasta cuatro subagentes background en total. Los lockfiles/config/migraciones compartidas se integran tras la barrera.
- `scripts/vx_task_dag.py` evalúa `PARALLEL_SAFE`, pero solo devuelve `PROPOSED_NOT_DISPATCHED`, sin ejecutar agentes ni reservar archivos. Las conversaciones `task` son la evidencia real de concurrencia.

## Desktop: Tauri siempre preferido

Para cualquier **nuevo proyecto Desktop explícito**, Tauri 2 es la **primera opción y motor preferido**: UI web TypeScript, lógica nativa Rust, controles de seguridad por capacidades. Si el alcance incluye Android, planificar UX móvil independiente y APK junto al EXE; si el usuario especifica `WINDOWS_ONLY`, Android queda `OUT_OF_SCOPE`. Una aplicación web/API no se convierte en Desktop. Proyectos existentes pueden requerir análisis de migración; preferir Tauri no autoriza borrar una implementación funcional o ignorar drivers/compatibilidad.

## Certificación real pendiente

- CI estática: manifest íntegro, permisos y controles por rol, cambio incremental/rollback del instalador y tests de DAG sobre rutas disjuntas o conflictivas.
- Prueba Kilo Desktop: líder inicia dos builders en background que cambian archivos distintos de un laboratorio; **mientras ambos siguen activos** el líder analiza un tercer archivo sin editar los reservados; después recoge resultados y ejecuta una prueba focalizada. Validar timestamps/host tool traces y rutas. Si `task` no tiene background en esa instalación, no declarar concurrencia.
- Nunca crear múltiples laboratorios, suites y reportes históricos por rutina: actualizar la evidencia viva cuando cambie el contrato.

## Changelog

- 1.4 RC1 (2026-11-21): arranque dirigido por capacidades globales, seis skills generales, permisos de skills por builder, dueño de archivos, coordinación background con barrera y Tauri-first Desktop. No altera `kilo.jsonc`, MCP, AutoApprove ni instalaciones del operador.
