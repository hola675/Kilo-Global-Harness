# VX Dev Team Core Unificado — instalación V1.1 RC1

**Fecha:** 2026-11-21. **Estado:** SOURCE V1.1 RC1, pendiente CI/revisión e instalación local de esta mejora. El Core V1.0 anterior fue probado en Kilo Desktop por el operador; no confundirlo con certificación del nuevo background paralelo. **No instalado automáticamente.**

## Decisión

Unificar el Pack VX 0.4.0 y Dev Team 2.3.0 en una única instalación global. No ejecutar dos instaladores ni crear dos líderes. Instalar los componentes declarados en [el manifiesto unificado](../registry/vx-unified-pack-v1.json), no concatenar indiscriminadamente las dos listas históricas.

| Familia | Seleccionados | Rol |
| --- | ---: | --- |
| Líder visible | 1 | vx-dev-team, único agente principal del pack |
| Analistas especialistas | 10 | Dev Explorer, Architect, Frontend, Backend, Data, Platform, Reviewer, Quality, Security y Research; ocultos/read-only |
| Implementadores | 6 | Frontend, Backend, Data, QA, Docs y Editorial; ocultos, edit/write/apply_patch con ask |
| Cloudflare | 1 | vx-workers-adviser; oculto/read-only |
| **TOTAL** | **18** | **1 visible y 17 ocultos** |

### Skills

**43 skills**: 18 Dev CORE, más 25 VX complementarias seleccionadas por aportar una capacidad de ejecución o dominio que no se cubre solo con la estrategia CORE (TypeScript, Python, Cloudflare, SQL, E2E, Docs, Git/CI, performance, observabilidad, editorial, IDA, incidentes y colaboración, entre otras). La lista exacta y sus rutas únicas están en el manifiesto. Las skills se cargan bajo demanda: nunca las 43 simultáneamente.

Se conservan en Git las 26 Dev adicionales que aún eran propuestas y las 7 VX no incluidas. No se activan waves W2-W5 automáticamente ni se elimina la documentación de VX Evolution.

### Retiro explícito de duplicados

Se desinstalan solamente seis agentes VX anteriores: vx-integrador, vx-inspector, vx-researcher, vx-security-reviewer, vx-test-analyst y vx-frontend-adviser. Sus funciones pasan al líder y a especialistas Dev. Se retiran exclusivamente siete archivos SKILL.md previamente administrados por VX: vx-evolution-core, vx-self-improvement, vx-security-review, vx-architecture-decisions, vx-codebase-investigation, vx-supply-chain-review y vx-accessibility-review. Sus directorios, archivos extra y código versionado quedan intactos; un backup DPAPI conserva los originales.

**No tocar:** kilo.jsonc, MCP, modelos, credenciales, AutoApprove, skills de terceros, agentes inline externos, rutas de proyectos, bases de datos o otros archivos de nombres desconocidos. Si hay colisiones en fuentes externas, bloquear y reconciliar en vez de borrar.

## Un solo procedimiento de instalación en Windows

**No instalar hasta que el PR haya pasado CI y revisión y esté integrado a main.** Utilizar PowerShell 7 externo. En D:\Proyectos\Kilo-Global-Harness, con git limpio y main sincronizada:

### 1. Preflight sin escritura

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Diagnostico
    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Simular

La respuesta debe indicar READY, 18 agentes y 43 skills, sin bloqueos ni cambios a configuración. Revisar el número de archivos a retirar antes de confirmar.

### 2. Aplicación

Cerrar previamente VS Code, VSCodium y Kilo Desktop (y sesiones que estén modificando la configuración). El instalador verifica que main coincide con origin/main y que no hay cambios locales.

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Aplicar -ConfirmarInstalacion -ConfirmarRetirarVXLegacy -ConfirmarKiloCerrado

Crear respaldo DPAPI CurrentUser, verificar que puede descifrarse y comprobar los archivos antes de escribir. El motor instala archivos con escritura atómica y retira solo nombres de la allowlist legacy declarada. Ante un fallo intenta rollback conservador, sin eliminar directorios.

### 3. Verificación y pruebas funcionales

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Verificar

Verificar que el resultado declara SOURCE_FILES_MATCH_RUNTIME_NOT_VERIFIED. Reiniciar Kilo y comprobar en la interfaz/CLI que hay un líder visible, 17 subagentes ocultos, skill loading real y task efectivo. Probar lectura Explorer, un builder con permisos ask en fixture aislado, editorial y revisión independiente; no usar datos ni infraestructura reales.

### 4. Restauración

Guardar la ruta absoluta de BACKUP DPAPI impresa al instalar, **no compartirla ni subirla a GitHub**. Con Kilo cerrado:

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Restaurar -CarpetaRespaldo RUTA_REAL_BACKUP -ConfirmarRestauracion -ConfirmarKiloCerrado

El rollback rechaza sobrescribir archivos modificados desde la instalación; investigar y recuperar de forma dirigida, no forzar.

### Instalación interrumpida antes de confirmar INSTALLED

Si hubo un corte de energía o un error de PowerShell tras crear un respaldo DPAPI, el recibo puede quedar en `BACKED_UP` aunque algunos archivos se hayan actualizado. La restauración normal **rechaza** ese estado; usar recuperación extraordinaria, explícita y con Kilo cerrado, **con la ruta real de ese respaldo**:

    pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Restaurar -CarpetaRespaldo RUTA_REAL_BACKUP -ConfirmarRestauracion -RecuperarInstalacionInterrumpida -ConfirmarKiloCerrado

La recuperación verifica para todos los destinos la allowlist de archivos administrados, el respaldo DPAPI y los hashes `before/after`. Si un archivo tiene un tercer valor inesperado, **se detiene sin sobrescribir**: conservar el respaldo y revisar el conflicto manualmente. Nunca aplicar esta opción para omitir colisiones o modificar archivos ajenos.

### Skills de terceros y colisiones de identidad

El preflight comprueba el ID tanto del directorio como del campo `name` del frontmatter de cada skill externa bajo `~/.kilo/skills`, `~/.agents/skills`, `~/.kilocode/skills` y `~/.claude/skills`. Una skill ajena cuyo archivo esté en otro directorio pero declare un nombre del Core provoca `BLOCKED`. No se elimina ni renombra automáticamente la skill externa.

## Política operativa de menor burocracia

Para tareas ordinarias el líder determina automáticamente Git root, branch, SHA y archivos por inspección. No exigir formularios ni tickets manuales si el entorno es suficiente. Elegir el mínimo de especialistas; el líder puede resolver tareas sencillas sin delegar. Los seis implementadores pueden editar proyectos con consentimiento de Kilo; no se convierten en modos principales.

Conservar salvaguardas necesarias: no elevar ACL por falta de herramienta, un escritor por worktree, no producción ni cambios destructivos sin autorización, no publicar ni fusionar sin evidencias, no declarar runtime PASS solo por hashes iguales.

## Changelog

- V1.0 RC1 (2026-11-20): 18 agentes únicos, 43 skills seleccionadas, un solo instalador reversible, seis agentes y siete skills históricas retirables, pruebas de instalación/rollback en suite viva; source aún no equivale a runtime instalado.

## Comandos compatibilizados (V1.0 RC1)

La instalación única gestiona también tres comandos globales: **/vx-equipo**, **/vx-dependencias** y **/vx-editorial**. Sus rutas apuntan al único líder `vx-dev-team`; los dos primeros ya no invocan al antiguo `vx-integrador`. El comando experimental histórico `/vx-p2` se retira del HOME con respaldo DPAPI porque seleccionaba directamente a `vx-docs-builder`, que ahora debe ser subagente oculto. El fuente `commands/vx-p2.md` permanece versionado para trazabilidad. Los demás comandos del usuario se conservan, sin borrados por nombre o coincidencias amplias.

**Inventario final bajo gestión del instalador:** 18 agentes, 43 skills, 3 comandos y un bloque de política global VX. Se pueden retirar exactamente seis agentes, siete skills y un comando históricos, si existen; todo el material anterior cambiado se respalda antes de mutar. La existencia de otros comandos o recursos ajenos no convierte su funcionalidad en certificada.

- V1.0 RC1 ajuste de seguridad: recuperacion explicita de respaldo `BACKED_UP` y bloqueo de colisiones por `name:` en skills ajenas globales; casos negativos agregados a la suite viva.

## Integración DAG e inline (corrección RC1)

El instalador único distribuye además **dos archivos de soporte** sin abrir otra instancia: `~/.config/kilo/harness/scripts/vx_task_dag.py` y `~/.config/kilo/harness/vx-unified-pack-v1.json`. `/vx-dependencias` llama al validador con `--registry` apuntando al registro unificado, no al registro histórico; el script admite también el formato legacy solo para compatibilidad, sin activar agentes retirados.

Si `kilo.jsonc` define en línea a cualquiera de los seis agentes legacy retirables (por ejemplo `vx-integrador`), la simulación devuelve `BLOCKED`: eliminar el archivo Markdown no elimina un agente inline. **No editar automáticamente `kilo.jsonc` ni deshabilitar configuración del usuario**; resolver esa colisión por el procedimiento de gestión explícito del host, con respaldo independiente. Comprobar la ausencia del segundo líder antes de aplicar el instalador.

**Inventario completo administrado:** 18 agentes, 43 skills, tres comandos, dos archivos de soporte y un bloque global de política. El número máximo de archivos legacy retirables sigue siendo 14 (seis agentes, siete SKILL.md y un comando); otros recursos globales no se eliminan.

## VX-RT-02C — Contrato adaptable para builders (V1.0.1)

**Evidencia:** en Kilo Desktop Windows, el operador configuró el modo Auto. VX-RT-02A mostró `apply_patch` realizado por el líder; no certifica escritura del builder. VX-RT-02B devolvió `NO_CHANGE_NEEDED`, sin tarea de escritura. VX-RT-02C invocó a `vx-frontend-builder`, pero este devolvió `BLOCKED` por exigir metadatos de Git no proporcionados para un laboratorio no Git. La inspección local confirmó `VX_RT02C_FILE_NOT_CREATED`. Estos resultados son runtime, no un defecto de `ask` demostrado.

**Corrección de source:** para los seis builders ocultos y las skills de colaboración/handoff, el contrato obligatorio se hace proporcional. Para un proyecto Git real, comprobar HEAD/branch, alcance de mutación, dependencias y un escritor por worktree. En un laboratorio local aislado sin Git, autorizado explícitamente por el operador con archivo y contenido exactos, declarar `GIT_NOT_APPLICABLE` sin inventar SHA/branch ni crear un repositorio Git artificial. El ID de tarea puede inferirse; no bloquear por metadatos opcionales si el objetivo y la ruta están identificados. El modo Auto del host no equivale a ampliar ACL; escrituras siguen siendo `ask` en source. Se mantiene la protección de secretos, producción, rutas fuera de alcance y múltiples escritores.

**Ensayo focalizado tras actualización global:** el operador comprobará primero que el archivo `vx-rt02c-frontend-builder.html` sigue ausente; invocará al líder `vx-dev-team` para asignar por `task` la creación exacta de ese único archivo al hijo `vx-frontend-builder`; no puede escribir el líder ni añadir herramientas de escape. La certificación exige evento `Created`/`Edited` dentro de la transcripción del hijo y comprobación independiente del contenido; si el host deniega escritura, `TOOL_UNAVAILABLE`/`BLOCKED_PERMISSION`. No repetir pruebas si la precondición dejó de cumplirse. No crear nuevos archivos de test en el repo; ampliar la suite viva `tests/test_vx_unified_pack_v1.py`.

**Estado:** código propuesto hasta PR/CI/revisión/merge, actualización local del operador y evidencia de Kilo Desktop. No reclamar `BUILDER_WRITE_PASS` antes de esas pruebas.


## VX 1.1 — Delegación paralela de Kilo Desktop sin convertirlo en VS Code

### Evidencia técnica y límite del host

Kilo Desktop se apoya en el motor CLI de Kilo. Según la documentación oficial de Kilo, `task` permite `background: true`: una tarea independiente continúa en una sesión hija mientras la sesión padre sigue trabajando. El resultado llega después. **Esto debe verificarse en la versión concreta de Kilo Desktop del operador; SOURCE no es RUNTIME.**

**No equivale a Agent Manager de VS Code:** `task` hereda el mismo directorio/worktree; no crea una rama o checkout aislado. `agent_manager` permanece denegado. Swarm/Board no se habilitan automáticamente ni se requiere para que `task` devuelva resultados.

Documentación del proveedor:
- https://kilo.ai/docs/automate/agent-manager
- https://kilo.ai/docs/customize/custom-subagents
- https://kilo.ai/docs/desktop/overview

### Protocolo del líder

1. Dividir la petición en contratos de resultados independientes y dependientes, **sin delegar por ritual**. Un simple arreglo puede resolverlo el líder.
2. Determinar estado Git (incluido `GIT_UNBORN_HEAD`), permisos y rutas exactas. Asignar dueño por archivo y separar los cambios de archivos comunes (config, imports centrales, package-lock, tests/snapshots compartidos).
3. Para subtareas que no dependen unas de otras, el líder usa realmente `task(background: true)` si aparece en la tool. **Máximo 4** background activos y **máximo 2** subagentes escritores. Si la tool no admite background, usar foreground y declararlo, sin simular paralelismo.
4. **Por defecto un escritor por worktree.** En un mismo workspace pueden trabajar dos builders simultáneamente **solo** con `write_scope: EXACT_FILES`, listas `allowed_paths` literales y totalmente disjuntas, permiso de edición efectivo, sin escrituras sobre archivos compartidos y sin ninguna operación Git concurrente. Para cambios solapados, serializar. Para ramas/commits independientes, usar worktrees Git reales **verificados**, no suponer que `task` los abrió.
5. Mientras los hijos trabajan, el líder puede analizar otros módulos, preparar contrato estable, revisar material ya terminado y delegar lectores independientes. No editar ni leer como definitivo un archivo todavía en escritura; no duplicar la tarea por falta de respuesta.
6. Esperar finalización real, inspeccionar diff/rutas del hijo, comprobar pruebas y pedir revisión independiente según riesgo. El líder integra en un **punto de sincronización**; no hacer commits/PR antes de esa barrera.
7. Si se corta una sesión, `HOLD_RECHECK`: comprobar el estado real antes de reanudar por `task_id` recuperable. No reiniciar a ciegas ni reescribir archivos de otro hijo.
8. Mantener Kilo Desktop **Auto** como lo eligió el operador, sin cambiar permisos, modelos, MCP, `kilo.jsonc` ni HOME para conseguir concurrencia.

### Planificador DAG (no despachador)

El soporte instalado `scripts/vx_task_dag.py` conserva el `mode: STRICT` original y añade el opt-in `mode: PARALLEL_SAFE`. Lee únicamente un JSON local explícito; valida dependencias, rutas literales y capacidades declaradas. No usa red, no ejecuta agentes ni reserva archivos.

Ejemplo de **dos implementaciones independientes** sobre el mismo workspace, editando archivos exclusivos y sin operaciones Git simultáneas (ejemplo ilustrativo, sustituir nombres/paths por el código real):

```json
{
  "schema": "vx-task-plan/1",
  "mode": "PARALLEL_SAFE",
  "max_background_tasks": 4,
  "max_parallel_writers": 2,
  "allow_shared_worktree_exact_files": true,
  "tasks": [
    {
      "id": "api-catalog",
      "owner": "vx-backend-builder",
      "reviewer": "vx-dev-reviewer",
      "state": "PENDING",
      "writer": true,
      "worktree": "workspace-actual",
      "write_scope": "EXACT_FILES",
      "allowed_paths": ["src/backend/catalog.py"],
      "depends_on": []
    },
    {
      "id": "ui-profile",
      "owner": "vx-frontend-builder",
      "reviewer": "vx-dev-reviewer",
      "state": "PENDING",
      "writer": true,
      "worktree": "workspace-actual",
      "write_scope": "EXACT_FILES",
      "allowed_paths": ["src/frontend/profile.tsx"],
      "depends_on": []
    }
  ]
}
```

El resultado `background_candidates` propone tareas paralelas, `parallel_deferred` explica bloqueos y `file_lease_proposals` enumera el ownership declarado. Los indicadores `file_leases_enforced: false`, `worktree_identity_verified: false`, `background_tool_verified: false` y `actions_executed: 0` **no cambian** al recibir un plan válido: el host y el líder deben demostrar la ejecución real. En modo compartido, una ruta glob, un solapamiento padre/hijo o ausencia de opt-in bloquea el segundo escritor. El DAG no certifica si las instrucciones del hijo se cumplen; el líder coteja cambios reales al terminar.

### Validación runtime focalizada (una sola vez)

En laboratorio aislado existente y **sin modificar instalaciones adicionales**, proponer dos tareas de edición de archivos sintéticos distintos con aceptación conocida y sin dependencia. Abrir en Kilo Desktop el líder `vx-dev-team`; verificar en el historial que se iniciaron dos hijos con `task(background: true)` y que el líder realizó una tercera actividad independiente mientras estaban activos. Comprobar los eventos de escritura dentro de cada hijo, que ninguna ruta se superpuso y que el padre esperó la barrera antes de probar. Si no se observan sesiones solapadas, registrar `BACKGROUND_RUNTIME_NOT_VERIFIED` y seguir operando foreground; **no crear más pruebas decorativas**.

### Changelog

- **V1.1 RC1 (2026-11-21):** delegación `task(background: true)` condicionada al host de Kilo Desktop, parent-work-while-children-run, dos writers con archivos exactos y disjuntos, DAG `PARALLEL_SAFE` plan-only, barrera de integración, fallback foreground y tests ampliados en la suite viva; ACL y AutoApprove intactos.
