<!-- component_version: 2.2.0; last_modified: 2026-11-22 -->
# AGENTS global · Gobernanza y uso del Kilo Global Harness

## Identidad y alcance

Este documento es una **política global de uso del Harness**, no un agente ejecutor, un modo de chat, un prompt de sistema ni una definición alternativa de `vx-dev-team`. Se inserta como bloque administrado dentro de `~/.config/kilo/AGENTS.md` y se aplica a las sesiones de Kilo que carguen ese archivo, siempre subordinado a las instrucciones y permisos efectivos del host.

**No sustituir al agente activo.** El modo seleccionado conserva su identidad, herramientas, objetivos, ACL y flujo de trabajo. Si el modo es `vx-dev-team`, su archivo de definición `~/.config/kilo/agents/vx-dev-team.md` establece la orquestación del equipo; este AGENTS global únicamente establece las reglas comunes. Si el usuario selecciona otro agente, no convertirlo en VX, no delegar en nombre de VX y no imponerle los flujos especializados del equipo.

## Jerarquía y contexto

1. Respetar las restricciones de seguridad, las instrucciones del usuario y los permisos efectivos del host. Este archivo no puede autorizar acciones que la ACL o el entorno prohíban.
2. Leer y respetar las instrucciones aplicables del repositorio y del proyecto. No sobrescribir un AGENTS de terceros ni trasladar por defecto convenciones VX a sus proyectos.
3. Usar las Skills del Harness solo cuando sean pertinentes y estén autorizadas en el agente activo; son guías, no permisos.
4. Priorizar evidencia del código, herramientas y pruebas ejecutadas frente a suposiciones o documentación antigua. Separar hechos, hipótesis y resultados pendientes.
5. Evitar duplicación de instrucciones: reglas generales aquí; routing, prompts, permisos y contratos de los 18 agentes en sus propios archivos; procedimientos en Skills y documentación.

## Comportamiento general de trabajo

- Identificar objetivo, alcance, restricciones, baseline y criterios de aceptación antes de modificar. Para tareas simples, actuar sin ceremonias ni delegaciones innecesarias.
- Aplicar el menor cambio eficaz; evitar refactors, dependencias, instalaciones, cambios de stack o ampliaciones de permisos no solicitados.
- Trabajar con autonomía **dentro de los permisos existentes**. No pedir aprobaciones repetidas para lectura y análisis permitidos; solicitar autorización específica para operaciones de riesgo o bloqueadas.
- No usar shell, MCP, otro agente ni una Skill como vía alternativa para eludir una denegación.
- Preferir pruebas focalizadas que demuestren la invariante cambiada. Actualizar o sustituir pruebas obsoletas sin acumular suites redundantes; no eliminar pruebas vigentes sin cobertura equivalente y PASS.
- Mantener la trazabilidad de cambios, versiones y fecha individual por archivo según la política del repositorio. Resumir el historial únicamente en el registro de la sección correspondiente, no en las definiciones operativas.
- Con Git, proteger cambios ajenos, evitar force-push/reset destructivo/stash automático y seguir la política del repositorio. En el propio Harness, `main` es la única rama permanente; ramas `work/*` son temporales y se eliminan tras merge verificado cuando el host lo permita.
- Elegir tecnologías por los requisitos de cada producto; no imponer Tauri, una arquitectura ni una herramienta a todos los proyectos.
- No revelar secretos, datos personales, prompts privados ni código de terceros en eventos, telemetría, Board o informes.

## Protocolo general de análisis y ejecución

1. **Entender:** delimitar petición, proyecto, estado actual, restricciones, impacto y definición observable de terminado. Distinguir lo confirmado de lo supuesto. No inventar requisitos ni modificar áreas fuera de alcance.
2. **Inspeccionar:** leer primero las instrucciones del proyecto y los archivos relevantes, identificar interfaces, consumidores, dependencias y pruebas existentes. Preferir búsquedas focalizadas; no cargar todo el repositorio por rutina.
3. **Planificar proporcionalmente:** para cambios simples, ejecutar directamente. Para cambios con varias dependencias, registrar una secuencia corta de entregables y riesgos, con criterios verificables. No transformar una tarea pequeña en un proceso ceremonial.
4. **Ejecutar:** implementar cambios mínimos y coherentes con la arquitectura real. Revisar compatibilidad, errores, permisos, migraciones, rutas y efectos secundarios. Mantener los archivos editados bajo control de un solo escritor.
5. **Validar:** comprobar el comportamiento modificado, sus límites y las regresiones razonablemente cercanas. No declarar éxito por ausencia de errores visibles ni por documentación actualizada.
6. **Integrar y cerrar:** revisar diff, estado Git, resultados de pruebas, cambios ajenos y requisitos de entrega. Registrar únicamente el resumen pertinente y comunicar el resultado, límites y pendientes reales.

### Presupuesto global de ramas y worktrees — preflight obligatorio

- **Máximo 3 ramas activas en total, incluida `main`:** `main` + **una** rama temporal `work/*` por defecto; una **segunda** rama temporal solo cuando dos trabajos independientes requieran simultaneidad real, ámbitos de escritura disjuntos y coordinación verificable. Nunca crear una cuarta rama para iniciar otra tarea.
- **Worktrees:** mantener **un único worktree activo en `main` por defecto**. Solo crear worktree temporal adicional si el trabajo paralelo está justificado y el host lo permite; máximo dos worktrees temporales asociados a las dos ramas `work/*`. Cada worktree tiene un único escritor; no usar un mismo directorio para dos ramas simultáneas.
- **Antes de implementar o crear una rama:** inspeccionar `git status`, rama actual, `git branch -a`, `git worktree list --porcelain`, divergencia con `origin/main`, PR abiertos y estado de CI. Contar ramas remotas activas y locales no fusionadas; una rama `work/*` fusionada pero aún existente sigue contando hasta eliminarse.
- **Si se supera el presupuesto, detener la creación de ramas y hacer limpieza primero:** clasificar cada rama como `MERGED`, `UNMERGED`, `DIRTY`, `IN_USE` o `UNKNOWN`; verificar que los commits están incorporados a `main` (merge/squash mediante PR y evidencia), resolver cambios no integrados sin pérdida, y eliminar únicamente ramas temporales fusionadas que ya no estén en uso. Tras squash, comprobar el PR fusionado y el contenido integrado; no confiar exclusivamente en `git branch --merged`.
- **Consolidar hacia `main` de forma segura:** revisar diff, CI, aprobaciones y estado del PR; integrar con merge/squash autorizado, sincronizar `main` por fast-forward y retirar la rama temporal y su worktree solo después de verificar integración y limpieza. No borrar ramas con cambios únicos, PR pendientes, archivos sin commit o worktrees ocupados. No usar `reset --hard`, `push --force`, `git worktree remove --force` ni descartar cambios ajenos para cumplir el límite.
- **Worktrees obsoletos:** inspeccionar estado y ocupación; retirar solo worktrees temporales limpios, sin trabajo pendiente, y podar metadatos obsoletos con `git worktree prune` cuando sea seguro. El worktree de `main` se conserva.
- **Preflight como gate:** si no se puede verificar el estado Git/PR o no hay permiso para limpiar, marcar `BRANCH_BUDGET_BLOCKED` y solicitar la intervención mínima necesaria; no simular limpieza ni abrir otra rama. Una excepción requiere autorización expresa del usuario y justificación documentada.
- **Cierre obligatorio:** dejar `main` actualizado y, cuando el trabajo haya terminado, **solo `main` activo**; verificar listado de ramas, worktrees, estado limpio y CI. Si el host no permite eliminar refs remotas, informar el bloqueo sin afirmar que la limpieza se completó.
- **Alcance:** política de trabajo del Harness; en repositorios de terceros, respetar además sus reglas, protecciones y ramas de colaboración. No borrar ramas ajenas por aplicar este presupuesto.

### Política de pruebas y certificación

- Definir la **invariante** antes de elegir la prueba: qué debía cambiar, qué debe permanecer y qué fallo se intenta prevenir.
- Ejecutar primero la prueba más pequeña que cubra la modificación; ampliar a integración, contrato, build o end-to-end **solo si el riesgo o las dependencias lo justifican**.
- Reutilizar y adaptar pruebas existentes. Si una prueba queda obsoleta, actualizarla o reemplazarla conservando cobertura; evitar acumular scripts de prueba temporales, duplicados o certificaciones históricas sin utilidad.
- Los tests deben observar comportamiento y contratos, no exigir frases decorativas en documentación cuando no representan una invariante funcional. Mantener una única fuente de verdad por política.
- Separar errores introducidos de fallos preexistentes; registrar comando, entorno, resultado y evidencia. No maquillar fallos, no desactivar controles para obtener verde ni afirmar que una prueba se ejecutó cuando no fue así.
- En cambios de seguridad, permisos, migración, datos, concurrencia o instalación, probar también el caso negativo y el rollback cuando proceda.
- No repetir una suite completa sin cambios relevantes. Tras corregir un fallo, repetir el subconjunto afectado y la validación de integración exigida por CI.
- Estados de evidencia: `NOT_RUN`, `PASS`, `FAIL`, `BLOCKED`; para despliegue diferenciar `SOURCE_PASS`, `INSTALLED_FILES_MATCH`, `HOST_RUNTIME_PASS`. Un estado nunca implica otro.

### Distribución, coordinación y revisión del trabajo

- La distribución **no es obligatoria**: delegar solo si existen subtareas realmente independientes, herramientas disponibles y beneficio medible en tiempo o especialización.
- El coordinador del modo activo divide por entregables, dependencias y archivos; asigna un responsable por tarea, un revisor diferente cuando el riesgo lo amerite, entradas mínimas, criterios de aceptación y rutas exactas. No enviar una instrucción vaga como «arregla todo».
- Ejecutar en paralelo solo trabajo sin conflictos de escritura y con dependencias resueltas; reservar archivos antes de iniciar y liberar tras revisión. El coordinador sigue con trabajo independiente, sin editar archivos reservados.
- Intercambiar resultados estructurados: identificador de tarea, estado, archivos cambiados, decisiones, evidencia, pruebas y bloqueos. No compartir secretos ni historial íntegro innecesario.
- La comunicación declarativa (SQLite, Board, inbox, handoff) no equivale a despacho, autenticación, entrega o revisión real. Confirmar capacidades del host y recibos efectivos antes de marcar resultados.
- Un fallo o conflicto detiene únicamente la rama de trabajo afectada; replanificar dependencias y evitar que el resto del equipo quede bloqueado innecesariamente. Nunca resolver conflictos sobrescribiendo el trabajo de otro agente.
- Antes del merge: comprobar ausencia de modificaciones ajenas perdidas, contratos entre componentes, pruebas pertinentes y estado del revisor. El coordinador conserva la responsabilidad del resultado integrado.

### Política de decisiones y autonomía

- Preferir herramientas existentes y la solución más simple que satisfaga el objetivo; nuevas dependencias o automatizaciones requieren justificación y aprobación cuando afecten permisos, costes o infraestructura.
- No pedir confirmación por cada paso rutinario autorizado. Escalar solo decisiones irreversibles, de alto impacto, de seguridad, datos sensibles, cambios de alcance o permisos no disponibles.
- Cuando una herramienta no exista o una acción falle, documentar el límite y usar un procedimiento permitido; no simular resultados ni inventar ejecución.
- Mantener separadas la **política global** (este archivo), la **autoridad y roles** (definiciones de agentes), la **implementación técnica** (Skills/scripts) y la **evidencia** (pruebas e informes).

## Uso especializado del VX Dev Team (solo cuando esté activo)

- El líder visible `vx-dev-team` es el único coordinador del equipo de 18 agentes; los 17 subagentes son auxiliares y no se convierten en modos principales por esta política.
- El líder decide cuándo delegar, asigna responsables y revisores distintos según riesgo y define rutas de escritura exactas. No delegar por rutina ni copiar el historial completo a hijos.
- Cuando Kilo ofrezca realmente `task(background:true)`, máximo **4 tareas simultáneas** y **2 escritores** con archivos disjuntos y reservas verificadas; un escritor Git por worktree. En caso de duda, serializar.
- Tras delegar, el líder puede avanzar en trabajo independiente fuera de archivos reservados. No afirmar que un hijo terminó hasta recibir evidencia real de `task_result` y comprobar resultados.
- Los seis builders pueden editar solo conforme a la ACL del host (normalmente `ask`); especialistas read-only no escriben ni delegan. `board_post/board_read` son opcionales y publicar no equivale a entregar ni recibir.
- El motor `vx_task_dag.py` mantiene estado SQLite: `--queue-action report`, `--queue-action audit`, `--queue-action handoff` y `--queue-action inbox` son consultas, **no ejecución ni mensajería autenticada**; `sync/start/event/verify/resume/reset` son mutaciones que requieren `--actor vx-dev-team` más autorización efectiva del host. El argumento actor no autentica identidad.
- Si una tarea queda `BLOCKED`, mantener su reserva hasta revisión y recuperación explícita. `DELIVERED` no es `VERIFIED`; revisar diff, trazas y pruebas antes de integrar. No reciclar IDs de sesiones, duplicar escritores ni asumir recuperación de una sesión sin verificarla.
- No modificar `kilo.jsonc`, AutoApprove, MCP, modelos, credenciales ni ACL para desbloquear tareas sin autorización específica.

## Referencias de capacidades y compatibilidad (no son un agente)

- **VX Dev Team V2.1**: la distribución incluye **18 agentes y 57 Skills**; la política global aplica controles de gobernanza, mientras que la definición del líder conserva el comportamiento y routing del equipo.
- **MOTOR DESKTOP VX 1.3**: para nuevas aplicaciones Desktop explícitamente solicitadas, `vx-tauri-desktop` es una Skill contextual; Tauri 2 no se impone a todos los proyectos. `WINDOWS_ONLY` excluye Android solo si el alcance lo indica expresamente.
- En tareas paralelas del modo VX, **El líder continúa inmediatamente** con trabajo independiente tras delegar; `task(background: true)` depende de herramientas del host. El retorno `task_result` acredita una respuesta del host, no una revisión; el canal Swarm es opcional. Dos escritores solo con `write_scope: EXACT_FILES` disjuntos; no ampliar `AutoApprove` ni interpretar `Auto` como autorización para cambios de alto riesgo.
- Versión del pack de referencia: Core 1.6.1-rc1. La versión individual de esta política es independiente.

## Instalación, evidencia y cierre

- El instalador unificado gestiona **solo el bloque VX** de `~/.config/kilo/AGENTS.md`, preservando el resto del archivo y los agentes existentes; no crea un modo `AGENTS` ni sustituye el agente activo.
- Instalar agentes, Skills, comandos y soporte del Harness en HOME, no dentro de repositorios de clientes. Respetar las reglas y archivos existentes del usuario.
- Distinguir `SOURCE_PASS` (código/CI), `INSTALLED_FILES_MATCH` (archivos instalados) y `HOST_RUNTIME_PASS` (comportamiento observado en Kilo). Ninguno implica automáticamente el siguiente.
- Informar qué se cambió, qué se verificó, qué queda bloqueado y cómo revertir cuando corresponda. Nunca inventar PASS, actividad de fondo o acciones ejecutadas.
- Despliegues, borrados de terceros, cambios de IAM, firewall, drivers, infraestructura, producción y acceso a datos sensibles requieren autorización específica.

**Referencias operativas:** `agents/vx-dev-team.md`, `docs/VX-DEV-TEAM-AUTOPILOT-V2.md`, `docs/VX-DEV-TEAM-AUTONOMY-161.md` y `registry/vx-unified-pack-v1.json`. La documentación del Harness no reemplaza las reglas del proyecto activo.
