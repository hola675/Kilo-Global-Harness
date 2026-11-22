# VX Dev Team — Contrato de autonomía y colaboración
<!-- document_revision: 2; updated: 2026-11-22; status: SOURCE_IMPLEMENTED_RUNTIME_NOT_CERTIFIED -->

## Objetivo
Aumentar autonomía operativa sin ampliar permisos indiscriminadamente: el líder toma decisiones rutinarias, selecciona equipo mínimo, reparte archivos exactos y verifica resultados. Ningún texto de política eleva las ACL efectivas de Kilo.

## Contrato común de los 18 agentes
Cada agente conserva su ID, rol, permisos del frontmatter y competencias. En toda tarea comunica: `task_id`, `contract_version`, `base_sha` cuando exista, `allowed_paths`, `dependencies`, `acceptance`, `evidence_ref`, `state`. Los agentes no inventan trazas, no leen secretos, no alteran permisos, MCP, AutoApprove ni configuración de terceros. Las skills son guías, nunca concesiones de privilegios.

### Líder (1)
- `vx-dev-team`: propietario del plan, DAG, registro de cola, delegación nativa `task`, integración Git y aceptación final. Puede implementar con autorización `ask` y fuera de reservas ajenas. No delega en cascada. Responsable único de las transiciones SQLite; un revisor distinto del escritor aporta evidencia.

### Especialistas de análisis (11)
- `vx-dev-explorer`: entradas, dependencias, impacto y símbolos.
- `vx-dev-architect`: interfaces, límites, ADR y decisiones.
- `vx-dev-frontend`: flujos, accesibilidad, estados y contratos UI.
- `vx-dev-backend`: API, validación, dominio y fallos.
- `vx-dev-data`: esquemas, SQL, migración y consistencia.
- `vx-dev-platform`: CI, runtime, empaquetado y despliegue propuesto.
- `vx-dev-reviewer`: revisión independiente de cambios y regresiones.
- `vx-dev-quality`: criterios de aceptación, pruebas y oráculos.
- `vx-dev-security`: fronteras de confianza, secretos y riesgos.
- `vx-dev-research`: documentación y estándares verificables.
- `vx-workers-adviser`: Workers, D1, KV, R2 y contratos serverless.
Todos permanecen sin escritura, sin delegación y sin acceso directo a la cola. Su entrega vuelve al líder por `task_result`.

### Implementadores (6)
- `vx-frontend-builder`: componentes UI, accesibilidad y estados.
- `vx-backend-builder`: API, servicios, contratos y validación.
- `vx-data-builder`: esquemas y migraciones solo en entornos autorizados.
- `vx-qa-builder`: tests y fixtures focalizados.
- `vx-docs-builder`: documentación, ADR y ejemplos.
- `vx-editorial-builder`: claridad textual, formularios y contenido.
Edición `ask` únicamente sobre archivos literales asignados; `task: deny`. Board permitido solo si la herramienta existe en Kilo. Nunca escriben directamente en la cola SQLite. Devuelven diff, archivos, pruebas y riesgos al líder.

## Orquestación rápida y precisa
1. Clasificar SIMPLE/MEDIA/COMPLEJA; evitar delegaciones ceremoniales.
2. Establecer baseline y contratos mínimos antes de lanzar escritores.
3. Planificar dependencias acíclicas y registrar `sync` cuando la complejidad lo justifique.
4. Máximo 4 hijos background y 2 escritores. Por defecto un escritor por worktree; excepción de 2 únicamente con `EXACT_FILES` disjuntos, contratos estables y ausencia de operaciones Git compartidas.
5. Usar `task(background:true)` solo tras verificar soporte del host. No confundir propuesta SQLite con ejecución ni con lock de filesystem.
6. Cada builder reporta `STARTED`, `CONTRACT_READY`, `MILESTONE`, `BLOCKED`, `DELIVERED` o `CORRECTION` por Board cuando disponible; fallback `task_result`.
7. El líder reconcilia `host_task_id` real con la cola; `DELIVERED` no equivale a `VERIFIED`.
8. Revisor independiente, tests focalizados, integración de un solo propietario Git y reporte final con evidencia.
9. Tras interrupción: consultar host antes de `resume` o `reset`; nunca duplicar escritor ni reutilizar ID retirado.

## SQLite: acceso y protección
- Motor: `~/.config/kilo/harness/scripts/vx_task_dag.py`.
- Estado: `~/.config/kilo/harness/state/vx-team-queue.sqlite3`.
- Tablas: `tasks`, `events`, `project_config`; SQLite WAL, transacciones `BEGIN IMMEDIATE`.
- El líder usa CLI `sync/report/start/event/verify/resume/reset` mediante shell autorizado por Kilo. El acceso no es un permiso SQL por agente; se basa en el control del host y el procedimiento.
- `report` es lectura; el resto son mutaciones. Los hijos no reciben ruta de escritura ni una API de cola.
- No instalar servidor SQL, daemon, scheduler, puente MCP ni servicio Windows como requisito del Core.
- No registrar prompts, secretos, contenido de código ni datos personales en eventos.
- Una referencia de evidencia en la BD no autentica su origen; el líder debe contrastar `task_result`, trazas y diff.

## Instalación y diagnóstico
Prerequisitos: Windows, PowerShell 7, Python con sqlite3 y DPAPI CurrentUser, Git, checkout limpio de `main`; Kilo cerrado para aplicar. Ejecutar `Diagnostico`, `Simular`, `Aplicar`, `Verificar` con el instalador unificado existente. Mantener copia cifrada y restauración. Comprobar runtime aparte: herramientas disponibles, permisos efectivos, skill loading, task background, Board, SQLite y dos escritores sin colisión.

## Versionado y trazabilidad
- La versión global del Harness procede exclusivamente de `registry/vx-unified-pack-v1.json`; el `displayName` del líder en el selector de modos debe mostrar esa versión publicada.
- Cada agente (incluido el líder) mantiene su propia versión SemVer y última fecha de modificación en **dos comentarios YAML dentro del frontmatter**: `# component_version:` y `# last_modified:`. Estos comentarios no añaden claves al esquema de Kilo.
- No incluir historial, bloques de evolución ni changelogs en las definiciones de agentes. El único historial resumido por sección está en `registry/AGENTS-VERSIONS.md`; Git conserva el detalle.
- La versión individual del líder **no** se muestra en el selector de modos. Modificar un agente no implica subir la versión global ni renombrar el líder.
- La versión del Harness solo cambia por decisión explícita de release y tras validación; entonces se sincroniza el nombre visible del líder con el manifiesto.
- Para Skills, scripts y políticas: un registro resumido por sección y metadatos mínimos compatibles con su formato, sin contaminación de contenido operativo.
- Un cambio documental no modifica automáticamente la versión del manifiesto distribuido. Solo subir Core tras actualizar assets y pasar CI + pruebas Windows.
- Changelog 1.6.1-rc1 (2026-11-21): contrato de autonomía, responsabilidades de 18 agentes, acceso a SQLite, límites de concurrencia y checklist de certificación; **solo documento propuesto**.


## Estado de implementación de la fase 1.6.1-rc1 (2026-11-22)
- 18 agentes y 57 skills mantienen metadatos individuales; el nombre visible del líder usa la versión del manifiesto.
- CI Windows compila y ejecuta el verificador de metadatos; las pruebas focalizadas cubren fechas y rutas inválidas.
- Cola SQLite: la CLI de mutación exige `--actor vx-dev-team`; es un guardarraíl declarativo, **no autenticación**, y no impide que otro proceso con permisos de archivo escriba en la base.
- La ejecución de agentes, el aislamiento de worktrees, los permisos efectivos del host y el canal Board siguen sujetos a comprobación real en Kilo Desktop. No atribuirles certificación por CI de source.
- No activar instalación global ni declarar runtime certificado sin validación del equipo Windows y aprobación de los gates del instalador.
