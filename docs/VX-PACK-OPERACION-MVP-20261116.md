# VX Pack 0.1 — Base operativa multiagente para Kilo Code (16-11-2026)

**Estado:** propuesta implementada en Git, NO instalada en el HOME Windows. No fusionar ni instalar hasta que CI Windows y revisión del diff sean satisfactorios. Alcance: un PC Windows; global Kilo, sin directorios de configuración dentro de proyectos.

## Contenido real

- 7 agentes VX originales y 5 builders adicionales (frontend, backend, QA, datos, docs); 10 skills VX nativas bajo demanda.
- Instalador V4 reparado: sigue siendo reversible, realiza copia previa de los destinos VX que modifica, copia los componentes VX y preserva `kilo.jsonc`, MCP, modelos, credenciales y permisos ajenos.
- `vx_pack_doctor.py`: diagnóstico **solo lectura**, inventaría componentes esperados, solapamientos de nombre y presencia de MCP (no conectividad).
- Catálogo de cinco MCP candidatos con fuentes oficiales. **No instala ni conecta ninguno**; requiere decisión individual y validación de permisos.
- `/vx-pack` y `/vx-equipo` para revisar preparación y seleccionar tareas. No hay nuevo scheduler.

## Preparación (PowerShell 7, desde el repositorio)

```powershell
git status --short
git switch work/vx-team-pack-operational-20261116
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

Agentes/skills personalizados antiguos: el doctor cuenta coexistencias, pero **no los desactiva, borra ni mueve**. Un perfil limpio futuro exige inventario global y `kilo.jsonc`, respaldo privado completo verificable, simulación de archivos a archivar fuera de rutas descubiertas, restauración ensayada y aprobación específica. No se declara sustituido un componente sin hacerlo y verificarlo.

## Puertas de seguimiento

- P0: validar PowerShell del instalador/validador y CI Windows, corregir defectos, abrir PR.
- P1: instalar Pack VX en HOME autorizado y probar subagentes/skills en la extensión.
- P2: seleccionar MCP faltantes individualmente, medir herramientas disponibles y coste de contexto.
- P3: introducir contratos máquina-a-máquina y DAG de dependencias, mensajes entre sesiones Agent Manager y evaluaciones independientes.
- P4: aprobación fuerte V4.7.2 en PR #29 y migración de archivos legacy solamente tras pruebas y autorización; scheduler sigue OFF.

**Límites:** `-Modo Aplicar` de V4 no archiva componentes ajenos ni resuelve duplicados inline en JSONC. `approval_granted=false` y `apply_supported=false` de la propuesta V4.7.2 continúan sin ser autorizaciones efectivas.
