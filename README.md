# Kilo Global Harness · VX Dev Team

**Fuente global para Kilo Desktop / Kilo Code (Windows).** La rama `main` mantiene un solo equipo operativo y un instalador unificado. Los archivos de este repositorio son **código fuente**, no prueba de que estén instalados o activos en tu Kilo.

## Estado canónico del paquete

| Elemento | Fuente vigente | Estado |
| --- | --- | --- |
| Versión del Core | `registry/vx-unified-pack-v1.json` | **1.6.2-rc1** |
| Coordinador | `agents/vx-dev-team.md` | Un solo líder visible, **VX Dev Team** (ID `vx-dev-team`) |
| Agentes | `agents/` y `runtime/dev-team-v2r/agents/` | **18**: líder + 17 subagentes ocultos |
| Skills | `skills/` y `runtime/dev-team-v2r/skills/` | **57** seleccionadas por el manifiesto; instalación local por verificar |
| Comandos activos del pack | `commands/vx-equipo.md`, `vx-dependencias.md`, `vx-editorial.md` | **3** |
| Archivos de soporte | `scripts/vx_task_dag.py` y manifiesto | **2** |
| Política global | `rules/AGENTS-global-managed.md` | **Reemplazo completo** de `~/.config/kilo/AGENTS.md` con respaldo |
| Instalación | `scripts/Instalar-DevTeam-Unificado.ps1` | Inventario, backup DPAPI, sustitución, migración SQLite, verificación y restauración |
| Validación de código | `.github/workflows/validar-harness.yml` | CI Windows; **no equivale a certificar Kilo runtime** |

El sistema mantiene un solo modo principal. Seis builders (Frontend, Backend, Datos, QA, Docs y Editorial) pueden editar exclusivamente mediante los permisos reales del host (`ask`). Los otros once especialistas son de solo lectura. **Swarm** (`board_read/post`) está autorizado únicamente en el líder y los seis builders; la disponibilidad efectiva depende de Kilo Desktop.

## Cómo se coordina VX Dev Team

El operador expresa el resultado deseado al líder mediante lenguaje natural o `/vx-equipo`. El líder establece criterios, rutas y dependencias; despacha `task(background: true)` solo cuando Kilo realmente soporte esa opción; continúa con trabajo independiente **fuera de los archivos reservados**; recopila hitos y verifica los resultados antes de integrar.

- Máximo cuatro subagentes en background; hasta dos escritores sobre archivos **exactos y disjuntos**. Un único escritor Git por worktree.
- La cola SQLite de `vx_task_dag.py` es privada, persistente y transaccional; el instalador aprovisiona su esquema v1 sin borrar datos existentes. **No ejecuta agentes ni crea worktrees**. Las tareas bloqueadas mantienen su reserva hasta cierre comprobado.
- `board_post` comparte avances dentro de una sesión Swarm cuando existe; no asegura que otro agente haya leído o aprobado el mensaje.
- El líder distingue `CLAIMED`, `DELIVERED` y `VERIFIED`; nunca declara pruebas runtime sin trazas reales.
- Sin scheduler ni vigilancia persistente: con Kilo cerrado, la cola conserva estado pero no trabaja.

Más detalles en [Autopilot V2](docs/VX-DEV-TEAM-AUTOPILOT-V2.md) y [política global](rules/AGENTS-global-managed.md). El documento AGENTS global establece gobernanza común y **no sustituye el modo/agente activo**; la orquestación especializada permanece en `agents/vx-dev-team.md`.

## Instalar en Windows

Cierra Kilo Desktop y VS Code, actualiza el repositorio y usa el **único instalador vigente**:

```powershell
Set-Location 'D:\Proyectos\Kilo-Global-Harness'
git switch main
git pull --ff-only origin main

pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Diagnostico
pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Simular
```

Solo después de comprobar el alcance, con Kilo cerrado, aplica si corresponde:

```powershell
pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 `
  -Modo Aplicar `
  -ConfirmarInstalacion `
  -ConfirmarRetirarVXLegacy `
  -ConfirmarKiloCerrado

pwsh -NoProfile -File .\scripts\Instalar-DevTeam-Unificado.ps1 -Modo Verificar
```

Cada actualización produce automáticamente informes `install-report.md` (legible) e `install-report.json` (detallado) dentro del backup DPAPI, con operaciones archivo por archivo, versiones anteriores y nuevas y resultado de SQLite. Consulta un backup histórico con `-Modo Informe -CarpetaRespaldo 'RUTA_ABSOLUTA'` sin reinstalar. El instalador inventaría el checkout, los worktrees, los archivos seleccionados ya existentes y hasta 14 rutas legacy VX explícitamente aprobadas; no elimina ramas, worktrees, archivos de proyecto ni recursos ajenos. Crea respaldo DPAPI de archivos y de la cola SQLite (snapshot consistente con WAL), migra aditivamente su esquema cuando procede, valida integridad y preserva las tareas/eventos existentes. Preserva `kilo.jsonc`, credenciales, conexiones MCP, modelos, AutoApprove y recursos de terceros. `Verificar` compara archivos y exige SQLite aprovisionada; **la certificación real de delegación, permisos y Swarm ocurre dentro de Kilo**.

## Qué no debe instalarse como sustituto

El árbol actual mantiene **solo los archivos del Core 1.6 que se instalan, sus dependencias directas, las pruebas esenciales y la documentación necesaria**. Los instaladores, agentes y comandos VX anteriores, catálogos de propuestas y suites de versiones pasadas se retiraron de la rama de trabajo después de sustituir sus dependencias operativas y de CI.

**Excepción consciente:** `scripts/vx_pack_coexist_v023.py` y `scripts/vx_pack_bootstrap.py` tienen nombres históricos, pero siguen siendo dependencias *efectivas* del instalador vigente para inspección segura de HOME, cifrado DPAPI y restauración. Las 14 rutas legacy que el instalador puede retirar del perfil están fijadas en su motor, aunque sus archivos fuente antiguos ya no estén presentes. Todo lo eliminado permanece recuperable mediante el historial Git.

Consultar [registro de depuración](docs/VX-HARNESS-INVENTARIO-AUDIT-20261121.md) para el alcance exacto y los criterios de retención.

## Documentación principal

- [Arquitectura actual](docs/ARQUITECTURA.md)
- [Guía del paquete unificado](docs/VX-DEV-TEAM-UNIFIED-V1.md)
- [Operación concurrente y recuperación](docs/VX-DEV-TEAM-AUTOPILOT-V2.md)
- [Política global administrada](rules/AGENTS-global-managed.md)
- [Matriz de permisos y fuentes](registry/vx-unified-pack-v1.json)
- [Pruebas actuales de instalación, permisos y cola](tests/test_vx_unified_pack_v1.py)
- [Inventario completo y retirada de legacy](docs/VX-HARNESS-INVENTARIO-AUDIT-20261121.md)

Las propuestas y guías V3/V4 que ya no forman parte del Core solo permanecen en el historial Git, no dentro del paquete distribuido.

## Desarrollo y seguridad

- Cualquier cambio requiere baseline, mínimo diff, tests focalizados y revisión según riesgo.
- Rama `work/*` temporal para cambios no triviales, PR y CI antes de fusionar. **Solo `main` es permanente**; limpiar ramas propias verificadas tras merge.
- No crear configuraciones globales de Kilo en repositorios de clientes; los recursos gestionados viven en HOME.
- Sin cambios silenciosos de ACL, MCP, infraestructura, datos sensibles, drivers o producción.
- Tauri, Electron, Qt u otras tecnologías se eligen **por necesidades de cada proyecto**, nunca se imponen a todas las aplicaciones.

## Observabilidad y limpieza segura (fases R3/R6)

El observador experimental de Kilo se mantiene exclusivamente como fuente en `runtime/kilo-observer/` y no se instala ni activa automáticamente. Sus pruebas offline validan la privacidad, idempotencia de eventos y tolerancia a errores; los eventos observados se guardan, solo tras doble opt-in y comprobación del host, en SQLite aparte de la cola DAG. No equivalen a tareas completadas o verificadas.

Para preparar un proyecto de prueba aislado bajo TEMP, sin instalar el plugin globalmente, utiliza `pwsh -NoProfile -File .\scripts\Probar-Observador-Kilo.ps1 -Modo Preparar`. La ejecución de Kilo se realiza posteriormente y **solo por decisión manual**; la prueba Bun del CI valida escritura SQLite en una base temporal y no inicia Kilo. Para consultar si existe una base de observaciones: `python -I scripts/vx_task_dag.py --observer-report`. Para validar los hooks offline: `node --test tests/test_vx_observer_contract.mjs`.

La limpieza de ramas Git se realiza únicamente de forma manual mediante `scripts/Eliminar-RamasFusionadas.ps1`, que por defecto **solo simula**. Antes de borrar una rama `work/*` verifica PR fusionado, último commit histórico de ese PR, HEAD remoto, worktrees, estado Git y lease de referencia. `main` nunca se elimina.

**Regla de evidencia:** `SOURCE_PASS` ≠ `INSTALLED_FILES_MATCH` ≠ `HOST_RUNTIME_PASS`.
