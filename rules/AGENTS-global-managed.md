<!-- component_version: 2.0.0; last_modified: 2026-11-22 -->
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

## Uso especializado del VX Dev Team (solo cuando esté activo)

- El líder visible `vx-dev-team` es el único coordinador del equipo de 18 agentes; los 17 subagentes son auxiliares y no se convierten en modos principales por esta política.
- El líder decide cuándo delegar, asigna responsables y revisores distintos según riesgo y define rutas de escritura exactas. No delegar por rutina ni copiar el historial completo a hijos.
- Cuando Kilo ofrezca realmente `task(background:true)`, máximo **4 tareas simultáneas** y **2 escritores** con archivos disjuntos y reservas verificadas; un escritor Git por worktree. En caso de duda, serializar.
- Tras delegar, el líder puede avanzar en trabajo independiente fuera de archivos reservados. No afirmar que un hijo terminó hasta recibir evidencia real de `task_result` y comprobar resultados.
- Los seis builders pueden editar solo conforme a la ACL del host (normalmente `ask`); especialistas read-only no escriben ni delegan. `board_post/board_read` son opcionales y publicar no equivale a entregar ni recibir.
- El motor `vx_task_dag.py` mantiene estado SQLite: `report/audit/handoff/inbox` son consultas, **no ejecución ni mensajería autenticada**; `sync/start/event/verify/resume/reset` son mutaciones que requieren `--actor vx-dev-team` más autorización efectiva del host. El argumento actor no autentica identidad.
- `DELIVERED` no es `VERIFIED`; revisar diff, trazas y pruebas antes de integrar. No reciclar IDs de sesiones, duplicar escritores ni asumir recuperación de una sesión sin verificarla.
- No modificar `kilo.jsonc`, AutoApprove, MCP, modelos, credenciales ni ACL para desbloquear tareas sin autorización específica.

## Referencias de capacidades y compatibilidad (no son un agente)

- **VX Dev Team V2.1**: la política global aplica controles de gobernanza, mientras que la definición del líder conserva el comportamiento y routing del equipo.
- **MOTOR DESKTOP VX 1.3**: para nuevas aplicaciones Desktop explícitamente solicitadas, `vx-tauri-desktop` es una Skill contextual; Tauri 2 no se impone a todos los proyectos. `WINDOWS_ONLY` excluye Android solo si el alcance lo indica expresamente.
- En tareas paralelas del modo VX, `task(background: true)` depende de herramientas del host. Dos escritores solo con `write_scope: EXACT_FILES` disjuntos; no ampliar `AutoApprove` ni interpretar `Auto` como autorización para cambios de alto riesgo.
- Versión del pack de referencia: Core 1.6.1-rc1. La versión individual de esta política es independiente.

## Instalación, evidencia y cierre

- El instalador unificado gestiona **solo el bloque VX** de `~/.config/kilo/AGENTS.md`, preservando el resto del archivo y los agentes existentes; no crea un modo `AGENTS` ni sustituye el agente activo.
- Instalar agentes, Skills, comandos y soporte del Harness en HOME, no dentro de repositorios de clientes. Respetar las reglas y archivos existentes del usuario.
- Distinguir `SOURCE_PASS` (código/CI), `INSTALLED_FILES_MATCH` (archivos instalados) y `HOST_RUNTIME_PASS` (comportamiento observado en Kilo). Ninguno implica automáticamente el siguiente.
- Informar qué se cambió, qué se verificó, qué queda bloqueado y cómo revertir cuando corresponda. Nunca inventar PASS, actividad de fondo o acciones ejecutadas.
- Despliegues, borrados de terceros, cambios de IAM, firewall, drivers, infraestructura, producción y acceso a datos sensibles requieren autorización específica.

**Referencias operativas:** `agents/vx-dev-team.md`, `docs/VX-DEV-TEAM-AUTOPILOT-V2.md`, `docs/VX-DEV-TEAM-AUTONOMY-161.md` y `registry/vx-unified-pack-v1.json`. La documentación del Harness no reemplaza las reglas del proyecto activo.
