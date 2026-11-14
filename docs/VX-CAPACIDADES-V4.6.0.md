# VX Capacidades V4.6.0 — Auditoría global Kilo Code de solo lectura

**Estado:** primera subfase de VX Capacitación / Auditoría; no es una evaluación de desempeño ni una reorganización. **Solo este PC Windows**, sin sincronización entre equipos.

## Propósito

Establecer una línea base reproducible y privada de todos los **agentes y skills declarados** en la instalación global de Kilo, antes de formar especialistas, proponer un nuevo agente, asignar una jefatura o reestructurar equipos.

El script `scripts/vx_capability_audit.py` reutiliza la exploración de archivos globales del núcleo V4.5.1 y compara **metadatos de configuración**. Lee la definición JSONC de Kilo, el frontmatter de los agentes Markdown y el registro versionado de siete agentes de VX que el instalador coloca bajo HOME.

### Fuentes admitidas

| Fuente | Qué se consulta | Qué NO se consulta |
| --- | --- | --- |
| `~/.config/kilo/kilo.jsonc` | Nombres de agentes y presencia de mode, steps, permisos simples | Prompts, descripciones, credenciales, modelos, MCP, rutas externas |
| `~/.config/kilo/agents/*.md` | Nombres y frontmatter plano (campos seguros) | Cuerpo del agente, prompts o instrucciones |
| `~/.kilo/skills/*/SKILL.md` | Nombre de carpeta, existencia de frontmatter, hash | Cuerpo, instrucciones o datos |
| `~/.agents/skills/*/SKILL.md` | Fuente compatible con Kilo | Otros clientes o sus runtimes |
| `~/.kilocode/skills/*/SKILL.md` | Fuente heredada reconocida por Kilo | Repositorios/proyectos locales |
| `~/.config/kilo/harness/vx-agent-registry-v4.json` | Capacidades declaradas por VX y referencias de perfiles | Resultados de tareas o desempeño real |

**Importante:** una ruta compatible no es un plugin para otro asistente; se incluye únicamente porque Kilo acepta algunas rutas de skills heredadas o compartidas. Esta fase no controla el orden de prioridad efectivo de Kilo.

### Evidencia reciente confirmada por el usuario

Según el registro local del 14 de noviembre de 2026, el equipo Windows tiene **SQLite v4** con integridad correcta, **79 fuentes inventariadas por el motor V4.3**, VX Observer en modo `light`, calendario conjunto 7 de diciembre de 2026 a las 09:00, una sesión y dos secciones, scheduler desactivado. El instalador de Kilo mostró **21 agentes JSONC, 11 nombres presentes también en Markdown, 19 límites `steps` superiores a 400 y tres raíces de skills**. Estas cifras son *una fotografía de ese momento*, no resultados inventados de la nueva auditoría V4.6.0. La nueva auditoría podrá contar distinta cantidad porque compara definiciones y no el inventario persistido en SQLite.

El usuario confirmó el uso **exclusivo en este PC Windows** (VX-D08). No existe justificación para sincronización nube o SQLite multi-PC.

## Interfaz de solo lectura

Tras instalar la versión publicada en `main` con el instalador habitual:

```powershell
$audit = Join-Path $HOME '.config/kilo/harness/scripts/vx_capability_audit.py'
python -I $audit                         # resumen sin datos privados
python -I $audit --json                  # informe JSON, sin escribir SQLite
python -I $audit --steps-limit 400 --json
```

Comando global de Kilo: `/vx-capacidades`.

La operación **no requiere inicializar ni migrar** la base SQLite y no la abre. No escribe archivos ni en HOME ni en los repositorios. No crea actas, observaciones, propuestas, miembros de equipos, skills, jerarquías, backups nuevos, notificaciones o tareas programadas. La carga del núcleo vecino desactiva la escritura de bytecode para evitar archivos `__pycache__`.

## Contrato de salida

Esquema `vx-kilo-capability-baseline/1`; campos destacados:

- `counts`: conteos de definiciones y fuentes, duplicidades por nombre, límites `steps`, perfiles y capacidades del router declaradas.
- `agents[].sources`: procedencia y metadatos permitidos por fuente. `NO_VERIFICADO` para modo/steps que no puedan interpretarse; sin contenidos de prompt o descripción.
- `agents[].router_capabilities`: capacidades declaradas, **no probadas**. `capability_evidence = declaracion_del_router | SIN_DATOS`.
- `agent_source_overlaps`: coincidencias JSONC/Markdown; diferencia de `mode`, `steps` y permisos de nivel simple, cuando ambos están declarados. **No afirma cuál definición gana en Kilo**.
- `skill_source_overlaps`: el mismo nombre aparece en varias raíces; **no demuestra duplicidad semántica ni error**.
- `profile_skills_not_observed`: skills referenciadas por perfiles que no se hallaron en las tres raíces; no demuestra ausencia en el runtime.
- `steps_review`: límites por encima del umbral, **revisar sin cambiar**.
- `agent_performance = NO_MEDIDO`, `skills_actual_performance = NO_MEDIDO`, `effective_precedence_verified = false`.

Los valores `NO_MEDIDO`, `NO_VERIFICADO` y `SIN_DATOS` deben mantenerse hasta reunir pruebas independientes.

## Riesgos, limitaciones y controles

1. **Privacidad:** solo nombres de componentes estrictamente válidos, huellas parciales, fuentes relativas a HOME, estados de permisos simples y métricas declaradas; el script no imprime rutas absolutas, prompts, modelos, servidores MCP ni contenido de skills. No publicar informes reales con nombres privados sin revisarlos.
2. **Parser parcial:** frontmatter Markdown solo admite escalas simples. Si la sintaxis es compleja, declara `unknown` en lugar de interpretar YAML incorrectamente. Para la precedencia definitiva usar la comprobación V4.2 y validación en Kilo.
3. **Skills no equivalen a competencia:** tener un `SKILL.md` no demuestra que el agente pueda usarlo, que sea bueno o que haya superado una prueba.
4. **Agentes duplicados:** conservar fuentes JSONC/Markdown originales; nunca limpiar por nombre ni sobrescribir permissions.
5. **Rendimiento:** el análisis de metadatos no puede inferir costos, tokens, tasa de éxito, tiempos, nivel senior o aptitud para liderar.
6. **I/O:** procesa archivos globales locales únicamente. No ejecuta software listado ni abre proyectos; no agrega hooks ni procesos residentes.
7. **Cambios:** las propuestas futuras se registran solo por petición explícita; este informe no llama a `propose` ni `inventory-sync`, ya que ambos escriben SQLite.

## Pruebas y aceptación V4.6.0

- Fixture Windows con agentes en JSONC+Markdown, comentarios JSONC, diferencias de `mode`, `steps` y `permission.edit`.
- Skills repetidas por nombre en diferentes raíces y referencias de perfil que no aparecen, sin afirmaciones sobre runtime.
- Filtrado de credenciales de muestra y ausencia de rutas absolutas en la salida.
- Informe repetido determinista; cero cambios de hash; BD inexistente permanece inexistente.
- Symlinks a archivos fuera de HOME ignorados; JSONC corrupto rechazado sin mostrar contenido.
- Instalación y rollback globales sin añadir nada al repositorio activo ni modificar SQLite.
- CI Windows PASS de V4.3–V4.5.1 y nueva batería V4.6.0.

## Próximas fases

**V4.6.1:** matriz de capacidad con evidencias, puntuación defendible y casos de prueba; ningún nivel de agente se asigna sin revisión externa. **V4.6.2:** capacitación candidata y comparación con baseline; **V4.6.3:** auditoría organizativa, necesidades de jefes/subordinados y propuestas de reestructuración, con aprobación humana previa a cualquier cambio.

Reuniones de VX: lunes 09:00 hora local Windows y primera reunión mensual conjunta con dos secciones. **Scheduler, notificaciones y autopromociones siguen OFF**.

**Continuidad V4.6.1:** la matriz de competencias de solo lectura consume esta línea base sin alterar sus estados de verificación. Véase [VX Matriz V4.6.1](VX-MATRIZ-COMPETENCIAS-V4.6.1.md).
