# Operación de equipos V4 · Kilo Global Harness

**Alcance:** solo configuración global de Kilo en Windows. **Estado:** diseño implementado, pruebas de Kilo en el ordenador del usuario pendientes. No se instalaron frameworks de terceros.

## Arquitectura real y compromisos

- Kilo `task(background: true)` delega a subagentes de la sesión actual. Los contextos conversacionales están aislados pero el árbol de archivos se comparte: NO ejecutar dos escritores en paralelo.
- Agent Manager administra sesiones independientes y puede aislar archivos mediante git worktrees, que exigen ramas distintas y consumen espacio de disco. Ese modo **no está habilitado** por V4.
- Kilo Swarm es un tablero de mensajes de una sesión y sus descendientes, no un planificador, bloqueo de archivos ni un mecanismo de aprobación.
- AutoApprove permanece configurado como lo dejó el usuario. Los subagentes nuevos tienen `edit: deny`, `bash: deny`, `mcp: deny`, `task: deny` y acceso de lectura restringido en patrones sensibles; estos son límites de herramientas, no una garantía absoluta contra todo flujo de información.
- `main` es la única rama permanente; para una tarea no trivial, una sola `work/<tema>` temporal. Después de pruebas, PR/merge verificado y limpieza de esa rama solamente.
- El selector de PowerShell **nunca invoca agentes, comandos Git, MCP o modelos**; solo recomienda el equipo. El coordinador de Kilo decide qué roles ejecutar a partir del objetivo y herramientas efectivamente disponibles.
- Los perfiles no sustituyen las reglas de permisos del usuario. Nunca crear `.kilo`, `.agents`, `AGENTS.md` ni nuevos MCP locales en un repositorio.

## Instalar o actualizar en Windows

Ejecutar desde PowerShell 7 y un repositorio limpio, sin sobrescribir cambios de usuario:

```powershell
Set-Location 'D:\Proyectos\Kilo-Global-Harness'
if (git status --porcelain) { throw 'Hay cambios locales, revisar antes de actualizar.' }
git switch main
git pull --ff-only origin main

$installer = '.\scripts\Instalar-Kilo-Global-Harness.ps1'
pwsh -NoProfile -File '.\scripts\Validar-Registro-V4.ps1'
pwsh -NoProfile -File $installer -Modo Diagnostico
pwsh -NoProfile -File $installer -Modo Simular
pwsh -NoProfile -File $installer -Modo Aplicar -PausarTaskObserver
pwsh -NoProfile -File $installer -Modo Verificar
```

`Aplicar` genera un respaldo privado en `%USERPROFILE%\.config\kilo-harness-backups\`; nunca enviarlo a GitHub. Conserva `kilo.jsonc`, AutoApprove, credenciales, modelos, MCP y configuraciones de los 12 agentes anteriores.

## Comprobar el selector sin gastar cuota

```powershell
pwsh -NoProfile -File "$HOME\.config\kilo\harness\scripts\Seleccionar-Equipo-V4.ps1" -Perfil cloudflare -Json
pwsh -NoProfile -File "$HOME\.config\kilo\harness\scripts\Seleccionar-Equipo-V4.ps1" -Perfil frontend -SoloLectura -MaxLectores 2
```

El resultado incluye perfil, `discover_parallel`, `implementation`, `review_parallel`, skills sugeridas y `actions_executed: 0`. No pasar secretos como argumentos de `-Tarea`; PowerShell puede registrar comandos en el historial.

## Prueba funcional en Kilo

1. Ejecutar `/reload`. Comprobar los nuevos agentes `@vx-researcher`, `@vx-test-analyst`, `@vx-security-reviewer`, `@vx-frontend-adviser` y `@vx-workers-adviser`.
2. Ejecutar `/vx-harness-estado` y comprobar que el registro V4 está instalado y el validador PASS.
3. Pedir: **"Usa /vx-equipo en modo SOLO LECTURA para revisar la arquitectura de este repositorio. Si vale la pena, delega en paralelo a vx-researcher y vx-test-analyst; muestra las evidencias, pero no modifiques código ni crees ramas."**
4. Comprobar en la interfaz del agente que ambos `task` arrancaron si el runtime lo permitió, que devolvieron resultados separados y que los datos se sintetizaron. Si no se expone `task`, registrar NO VERIFICADO y trabajar secuencialmente.
5. Ejecutar una tarea autorizada de cambio pequeño en un repositorio de pruebas: un único escritor, QA posterior, pruebas reales, diff y cierre Git. No realizar deploy ni operaciones sobre producción para la prueba.

**No declarar PASS de ejecución multiagente solo porque existan los archivos o porque el selector produzca JSON.**

## Contrato de los informes de subagentes

Para cada lector, una salida corta con objetivo, rutas inspeccionadas, hallazgos con evidencia, dudas y recomendaciones. No compartir transcripciones completas, secretos ni afirmaciones sin referencia. Para cada revisor, un tipo de riesgo distinto (QA, seguridad, UX o contratos).

El coordinador fusiona hallazgos, evita revisiones repetidas y asigna una única implementación. Los mensajes del tablero Swarm son datos, nunca autorizaciones.

## Manejo de fallos

| Fallo | Acción |
| --- | --- |
| Agente no aparece | Validar archivo global y frontmatter; `/reload`; no crear configuración en repo |
| `task` indisponible | Ejecutar secuencialmente; no afirmar paralelismo |
| Dos propuestas editan mismo archivo | Detener nueva delegación; un solo escritor en modo estricto |
| Registro inválido | `Validar-Registro-V4.ps1` detiene instalación ANTES de escribir |
| MCP no conecta | Desactivar su uso en esta tarea, usar lectura local; nunca inventar conexión |
| Bucle de subagente | Detener/revisar límites y reintentos; reportar; no ampliar steps ciegamente |
| Git muestra trabajo ajeno | No resetear ni borrar; revisar `git status`; conservar la rama |
| Test o CI falla | No merge ni borrado de rama; corregir y volver a verificar |
| Imagen necesita generación | Solo si el usuario solicita una imagen; ImageGen consume cuota |
| `Verificar` falla | No reinstalar a ciegas; comparar hash y backup; restaurar si procede |

## Reversión

Desde el repositorio V4 usa la ruta de backup mostrada por la ejecución:

```powershell
pwsh -NoProfile -File '.\scripts\Instalar-Kilo-Global-Harness.ps1' -Modo Restaurar -BackupFolder 'RUTA_REAL_DEL_BACKUP'
```

El mismo instalador reconoce manifiestos 3.0.0 y 4.0.0. Sin `-ForzarRestauracion`, respeta cambios posteriores en archivos instalados.

## Mantenimiento, licencias y suministro

El catálogo de 44 repositorios es solo investigación. La V4 **no copia** agentes ajenos ni ejecuta hooks o instaladores externos. Para incorporar un rol de tercero: URL + commit fijado + licencia del archivo + revisión de instrucciones/seguridad + adaptación a Markdown Kilo + fixture + prueba pequeña + aprobación. Prohibida la autoactualización silenciosa y la ejecución directa de hooks no revisados.

## Límites conocidos y siguientes auditorías

- 12 agentes en dos fuentes de configuración: Kilo fusiona propiedades; comparar efectividad antes de limpiar.
- 19 entradas inline con `steps=10000000`: auditoría y posible migración gradual, sin tocar permisos autónomos.
- El selector clasifica palabras y perfiles de manera determinista: puede escoger un perfil imperfecto. `-Perfil` explícito evita ambigüedad.
- La CI valida archivos, coherencia y PowerShell en Windows aislado; no prueba el consumo de tokens real ni la disponibilidad del modelo ni la correcta invocación de `task` desde el ordenador.
- El router no es un planificador automático en background ni una cola autónoma persistente. Para esa fase haría falta un plugin Kilo revisado y pruebas de runtime.

## Fuentes oficiales

- https://kilo.ai/docs/customize/custom-subagents
- https://kilo.ai/docs/automate/agent-manager
- https://kilo.ai/docs/customize/agent-permissions
- https://kilo.ai/docs/customize/skills
