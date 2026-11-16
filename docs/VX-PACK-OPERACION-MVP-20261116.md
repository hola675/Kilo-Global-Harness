# VX Pack 0.2.2 — Base operativa multiagente para Kilo Code (16-11-2026)

**Estado:** Pack 0.2.2 preparado para instalación supervisada en Windows; autorizado por el operador (2026-11-16), todavía sin validación real de HOME ni del runtime Kilo. 12 agentes, 31 skills y 6 MCP candidatos. Primero diagnóstico/simulación y Kilo cerrado. [Procedimiento actualizado](VX-INSTALACION-PACK-0.2.2-WINDOWS.md). Alcance: un PC Windows; global Kilo, sin directorios de configuración dentro de proyectos.

## Contenido real

- 7 agentes VX originales y 5 builders adicionales (frontend, backend, QA, datos, docs); 31 skills VX nativas bajo demanda.
- Instalador V4 reparado: sigue siendo reversible, realiza copia previa de los destinos VX que modifica, copia los componentes VX y preserva `kilo.jsonc`, MCP, modelos, credenciales y permisos ajenos.
- `vx_pack_doctor.py`: diagnóstico **solo lectura**, inventaría componentes esperados, solapamientos de nombre y presencia de MCP (no conectividad).
- Catálogo de seis MCP candidatos con fuentes oficiales. **No instala ni conecta ninguno**; requiere decisión individual y validación de permisos.
- `/vx-pack`, `/vx-equipo` y `/vx-dependencias` para revisar preparación y seleccionar tareas. No hay nuevo scheduler.

## Preparación (PowerShell 7, desde el repositorio)

```powershell
git status --short
git switch main
pwsh -NoProfile -File .\scripts\Validar-Registro-V4.ps1
python -I -m unittest discover -s tests -v
pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness.ps1 -Modo Diagnostico
pwsh -NoProfile -File .\scripts\Instalar-Kilo-Global-Harness.ps1 -Modo Simular
python .\scripts\vx_pack_doctor.py --json
```

**No usar `-Modo Aplicar` hasta superar Windows CI, revisar el listado de destinos y decidir la instalación.** Para instalar, el operador ejecutará el mismo script con `-Modo Aplicar` en su PC; el backup real queda en el perfil Windows, no se sube a GitHub. Después: `-Modo Verificar`, `/reload`, prueba de selección de un agente VX y una delegación `task` con salida real. Un test sintético NO demuestra que Kilo haya iniciado agentes.

## Operación inicial de equipo

1. `vx-integrador` recibe objetivo y descompone entregables, archivos, dependencias y criterio de aceptación.
2. Hasta tres lectores independientes por `task`, según perfil; sin escritura concurrente en el mismo worktree.
3. Elegir un builder VX por perfil solo como opción explícita; sus herramientas `edit/bash: ask` pueden exigir interacción directa con Kilo. Si la tarea delegada no puede pedir aprobación, se bloquea y devuelve plan.
4. Revisión del diff por inspector, seguridad/QA según alcance y ejecución auténtica de pruebas, nunca un PASS autorreportado.
5. Trabajo paralelo con escritura únicamente mediante Agent Manager worktrees **después de autorización concreta por tarea**; las sesiones no comparten automáticamente el tablero Swarm.

## MCP y sustitución progresiva

Mantener **todos** los MCP existentes. Usar Kilo Settings > Agent Behaviour > MCP Servers para revisar cada candidato; conectar solo el faltante elegido, OAuth de mínimo privilegio y verificación explícita. El doctor no lee encabezados, tokens ni valores de claves; solo nombres configurados. Ningún MCP es requisito global para preguntar, editar o ejecutar tests locales.

**El doctor no desactiva, borra ni mueve componentes antiguos.** El bootstrap Windows `scripts/vx_pack_bootstrap.py` (integrado desde el diseño de PR #30 en la PR #31) sí permite una sustitución explícita de agentes y skills Markdown del perfil global, pero únicamente con preflight, backup cifrado DPAPI CurrentUser, verificación y confirmación. Rechaza agentes inline, rutas adicionales de skills y directorios de compatibilidad poblados. Ningún estado de CI es autorización para ejecutarlo en HOME real. En rollback conserva modificaciones a plugin/SQLite y detiene la restauración si aparecieron archivos nuevos después de instalar.

## Puertas de seguimiento

- P0: validar PowerShell del instalador/validador y CI Windows, corregir defectos, abrir PR.
- P1: instalar Pack VX en HOME autorizado y probar subagentes/skills en la extensión.
- P2: seleccionar MCP faltantes individualmente, medir herramientas disponibles y coste de contexto.
- P3: introducir contratos máquina-a-máquina y DAG de dependencias, mensajes entre sesiones Agent Manager y evaluaciones independientes.
- P4: autenticación efectiva pendiente tras integrar contratos V4.7.2 y migración de archivos legacy solamente tras pruebas y autorización; scheduler sigue OFF.

**Límites:** el instalador V4 es incremental y no archiva componentes ajenos; el bootstrap DPAPI tiene otras reglas de sustitución. Ninguno resuelve automáticamente duplicados inline del JSONC. `approval_granted=false` y `apply_supported=false` de la propuesta V4.7.2 continúan sin ser autorizaciones efectivas.

## Especialización V0.2 (20 skills VX añadidas)

La matriz `registry/vx-skill-dependencies-v1.json` contiene 31 skills, dependencias acíclicas, perfiles, fases y responsables/revisores distintos. `vx_skill_router.py` propone una selección **sin ejecución** y devuelve prerequisitos; no sustituye al tool `skill` de Kilo ni garantiza carga automática. Ejemplos:

```powershell
python .\scripts\vx_skill_router.py --validate-only
python .\scripts\vx_skill_router.py --profile cloudflare --phase build --task "D1 Queues"
python .\scripts\vx_skill_router.py --profile frontend --phase verify --task "Playwright E2E"
```

Cobertura nueva: requisitos, DAG de tareas, ADR, codebase, APIs, TypeScript, Python, Workers, D1/KV/R2/Queues, SQL, colaboración, Git CI, supply chain, E2E, WCAG, rendimiento, privacidad/observabilidad, MCP, release y respuesta a incidentes. No se afirma ausencia absoluta de huecos: capacidades se certifican con pruebas de runtime y resultados reales; ampliar solo por brecha medida. Guía técnica original VX, referencias oficiales en cada SKILL.md.

## Grafo de dependencias de tareas VX 0.1

El validador nativo `scripts/vx_task_dag.py` recibe un plan JSON externo con `schema=vx-task-plan/1`, `mode=STRICT` y tareas con `id`, `owner`, `reviewer`, `depends_on`, `state`, `writer`, `worktree` y `allowed_paths` si escribe. Rechaza referencias a agentes inexistentes, revisores iguales al autor, ciclos, escritores concurrentes y tareas RUNNING sin prerequisitos. Una tarea `VERIFIED` exige referencias `review_ref` y `test_report`, pero estas **son declaraciones del plan y no verificación criptográfica**. La herramienta no ejecuta agentes ni habilita modo paralelo.

## Dos vías de instalación (no intercambiar respaldos)

**Incremental V4:** `Instalar-Kilo-Global-Harness.ps1` conserva agentes/skills heredados y aplica solo destinos del pack VX; posee manifiesto propio por archivo. Es útil para probar convivencia antes de sustitución.

**Sustitución limpia DPAPI V0.2:** `vx_pack_bootstrap.py` es independiente y **solo Windows**. Inventaría las configuraciones `kilo.jsonc`, `kilo.json` y `config.json`; preserva nombres MCP y sus valores byte a byte; respalda archivos existentes en un ZIP cifrado DPAPI CurrentUser no portable a otro usuario Windows. Su `restore` exige manifiesto de instalación, comprueba hashes y bloquea si aparecieron archivos nuevos no cubiertos; no sobrescribe datos ajenos que el pack no modificó. Debe cerrarse Kilo antes de manipular su perfil y revisarse una simulación del HOME real antes de `apply`. Un perfil con inline agents o skills externas activas se **bloquea**, no se migra a la fuerza.

```powershell
python .\scripts\vx_pack_bootstrap.py --mode diagnose
python .\scripts\vx_pack_bootstrap.py --mode simulate
```

La instalación del Pack VX en HOME está autorizada por el operador **solo tras** preflight limpio, snapshot DPAPI y Kilo cerrado. No autoriza activar MCP, V4.7.2, scheduler ni modificar credenciales.

## Gobierno de permisos MCP y delegación — V0.2

La ACL de cada agente VX inicia con `"*": deny` para herramientas desconocidas; después concede lectura, búsqueda y uso de skills por rol. Esto importa porque **Kilo nombra las herramientas MCP como `servidor_herramienta`**: no considerar `mcp: deny` una barrera suficiente. Ninguna skill amplía permisos; los builders requieren `edit/bash: ask`, salvo bash denegado en documentación. El revisor `vx-inspector` no ejecuta terminal y recibe un diff comprobado por el coordinador. El coordinador solo delega a seis lectores/revisores VX explícitos, no a agentes legacy con permisos desconocidos.

Fuentes: https://kilo.ai/docs/customize/agent-permissions y https://kilo.ai/docs/automate/mcp/using-in-kilo-code. Estas son garantías de la **configuración fuente**; comprobar precedencia y permisos efectivos en Kilo real antes de afirmar aislamiento definitivo.

## Restricción de restauración forzada

Incluso con `--force-restore`, el bootstrap DPAPI **rechaza** restaurar si detecta agentes o skills nuevos posteriores al respaldo; primero deben preservarse en una copia independiente y revisarse. Force no es un permiso genérico para eliminar archivos ajenos. La restauración nunca debe ejecutarse durante sesiones activas de Kilo; la integración de PR #30 en PR #31 ya está fusionada en main, pero no constituye una migración aprobada.

## Integridad entre backup y sustitución

Antes del primer borrado, `vx_pack_bootstrap.py` vuelve a listar agentes y skills, y coteja sus nombres y SHA256 con el contenido del snapshot DPAPI recién creado. Si otro proceso añadió o modificó cualquier archivo tras el respaldo, aborta la sustitución y mantiene los archivos intactos. Esto reduce la ventana de pérdida accidental; por seguridad también se debe cerrar Kilo antes de aplicar cambios reales. El comando `simulate` sigue sin escribir archivos.

## Extensión IDA MCP (Pack 0.2.1)

La skill `vx-ida-mcp-reverse-engineering` y comando `/vx-ida` pertenecen al perfil `reverse-engineering`. El catálogo incorpora el MCP oficial Hex-Rays como sexto **candidato opt-in**, `enabled_by_default:false`, sin modificar `kilo.jsonc` ni instalar servidores. El flujo de investigación es read-only por defecto y exige datos observables, separación de revisor, autorización individual para herramientas que editan IDB o ejecutan código. `ida-hcli` no debe instalarse hasta verificar cuál Python ejecuta IDA 9.4.

```powershell
python .\scripts\vx_skill_router.py --validate-only
python .\scripts\vx_skill_router.py --profile reverse-engineering --phase discover --task "IDA Pro MCP pseudocodigo y xrefs"
python .\scripts\vx_pack_bootstrap.py --mode simulate
```

La CI prueba contratos e inventario, no la conexión a IDA ni disponibilidad de decompilación en el Windows del operador.

## Preflight de la entrega 0.2.2

Los destinos globales rechazan symlinks, junctions y otros reparse points también en carpetas intermedias, incluidos `commands`, `rules` y `harness/scripts`. El preflight publica bloqueos antes de escribir; la comprobación se repite antes de sustituir. Los marcadores duplicados en `AGENTS.md` provocan bloqueo conservador. El nuevo `scripts/Instalar-Pack-VX-V022.ps1` orquesta diagnóstico, simulación, aplicación autorizada con DPAPI y verificación. No sustituye silenciosamente la migración limpia por el instalador V4 incremental. [Guía](VX-INSTALACION-PACK-0.2.2-WINDOWS.md).

## Compatibilidad y coexistencia V0.2.3

El HOME reportado contiene 19 agentes inline y skills de compatibilidad externas. El instalador limpio DPAPI 0.2.2 continúa bloqueando esa situación; no se deben borrar los agentes ni las skills para instalar VX. La ruta recomendada es scripts/Instalar-Pack-VX-Convivencia-V023.ps1, que realiza un preflight de colisiones por nombre, conserva JSONC/MCP/perfiles externos y crea un backup DPAPI específico para destinos VX. Si hay colisión, NO aplicar ni renombrar automáticamente. [Procedimiento](VX-INSTALACION-CONVIVENCIA-0.2.3-WINDOWS.md).
