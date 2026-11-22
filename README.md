# Kilo Global Harness · VX Dev Team

**Fuente global para Kilo Desktop / Kilo Code (Windows).** La rama `main` mantiene un solo equipo operativo y un instalador unificado. Los archivos de este repositorio son **código fuente**, no prueba de que estén instalados o activos en tu Kilo.

## Estado canónico del paquete

| Elemento | Fuente vigente | Estado |
| --- | --- | --- |
| Versión del Core | `registry/vx-unified-pack-v1.json` | **1.6.0-rc1** |
| Coordinador | `agents/vx-dev-team.md` | Un solo líder visible, **VX Dev Team** (ID `vx-dev-team`) |
| Agentes | `agents/` y `runtime/dev-team-v2r/agents/` | **18**: líder + 17 subagentes ocultos |
| Skills | `skills/` y `runtime/dev-team-v2r/skills/` | **57** instaladas, uso sujeto a allowlists |
| Comandos activos del pack | `commands/vx-equipo.md`, `vx-dependencias.md`, `vx-editorial.md` | **3** |
| Archivos de soporte | `scripts/vx_task_dag.py` y manifiesto | **2** |
| Política global | `rules/AGENTS-global-managed.md` | Bloque administrado de `~/.config/kilo/AGENTS.md` |
| Instalación | `scripts/Instalar-DevTeam-Unificado.ps1` | Diagnóstico, simulación, aplicación y verificación |
| Validación de código | `.github/workflows/validar-harness.yml` | CI Windows; **no equivale a certificar Kilo runtime** |

El sistema mantiene un solo modo principal. Seis builders (Frontend, Backend, Datos, QA, Docs y Editorial) pueden editar exclusivamente mediante los permisos reales del host (`ask`). Los otros once especialistas son de solo lectura. **Swarm** (`board_read/post`) está autorizado únicamente en el líder y los seis builders; la disponibilidad efectiva depende de Kilo Desktop.

## Cómo se coordina VX Dev Team

El operador expresa el resultado deseado al líder mediante lenguaje natural o `/vx-equipo`. El líder establece criterios, rutas y dependencias; despacha `task(background: true)` solo cuando Kilo realmente soporte esa opción; continúa con trabajo independiente **fuera de los archivos reservados**; recopila hitos y verifica los resultados antes de integrar.

- Máximo cuatro subagentes en background; hasta dos escritores sobre archivos **exactos y disjuntos**. Un único escritor Git por worktree.
- La cola SQLite de `vx_task_dag.py` es privada, opcional y transaccional. **No ejecuta agentes ni crea worktrees**. Las tareas bloqueadas mantienen su reserva hasta cierre comprobado.
- `board_post` comparte avances dentro de una sesión Swarm cuando existe; no asegura que otro agente haya leído o aprobado el mensaje.
- El líder distingue `CLAIMED`, `DELIVERED` y `VERIFIED`; nunca declara pruebas runtime sin trazas reales.
- Sin scheduler ni vigilancia persistente: con Kilo cerrado, la cola conserva estado pero no trabaja.

Más detalles en [Autopilot V2](docs/VX-DEV-TEAM-AUTOPILOT-V2.md) y [política global](rules/AGENTS-global-managed.md).

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

El instalador crea un respaldo DPAPI y preserva `kilo.jsonc`, credenciales, conexiones MCP, modelos, AutoApprove y recursos de terceros. `Verificar` compara archivos; **la certificación real de delegación, permisos y Swarm ocurre dentro de Kilo**.

## Qué no debe instalarse como sustituto

El repositorio conserva **código de compatibilidad y pruebas históricas**: `Instalar-Kilo-Global-Harness.ps1`, `Instalar-DevTeam-Only.ps1`, instalaciones de convivencia antiguas, otros 32 comandos VX, propuestas en `registry/*.proposal.json` y snapshots de certificación. **No corresponden al pack activo de 18/57/3/2** ni deben activarse simultáneamente al instalador unificado.

No borrar automáticamente fuentes que aún utilizan validadores antiguos, restauración o suites de regresión. Consultar [inventario de auditoría](docs/VX-HARNESS-INVENTARIO-AUDIT-20261121.md) para el estado y la política de retiro.

## Documentación principal

- [Arquitectura actual](docs/ARQUITECTURA.md)
- [Guía del paquete unificado](docs/VX-DEV-TEAM-UNIFIED-V1.md)
- [Operación concurrente y recuperación](docs/VX-DEV-TEAM-AUTOPILOT-V2.md)
- [Política global administrada](rules/AGENTS-global-managed.md)
- [Matriz de permisos y fuentes](registry/vx-unified-pack-v1.json)
- [Pruebas focalizadas y gates vivos](docs/VX-CI-LIVING-GATES-V1.md)
- [Inventario completo y retirada de legacy](docs/VX-HARNESS-INVENTARIO-AUDIT-20261121.md)

Las guías V3/V4 y las propuestas VX Academy/Dev Team anteriores siguen en `docs/` y `registry/` como **historia o diseño opcional**, no como instrucciones de instalación del equipo actual. Su historia de cambios completa también permanece en Git.

## Desarrollo y seguridad

- Cualquier cambio requiere baseline, mínimo diff, tests focalizados y revisión según riesgo.
- Rama `work/*` temporal para cambios no triviales, PR y CI antes de fusionar. **Solo `main` es permanente**; limpiar ramas propias verificadas tras merge.
- No crear configuraciones globales de Kilo en repositorios de clientes; los recursos gestionados viven en HOME.
- Sin cambios silenciosos de ACL, MCP, infraestructura, datos sensibles, drivers o producción.
- Tauri, Electron, Qt u otras tecnologías se eligen **por necesidades de cada proyecto**, nunca se imponen a todas las aplicaciones.

**Regla de evidencia:** `SOURCE_PASS` ≠ `INSTALLED_FILES_MATCH` ≠ `HOST_RUNTIME_PASS`.
