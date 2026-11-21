---
name: vx-desarrollo-escalonado
description: "Organizar cualquier proyecto software por objetivo final, fases incrementales, dependencias, entregas comprobables y trabajo multiagente paralelo sin burocracia ni pruebas acumulativas."
metadata:
  version: "1.1.0"
  origin: "vx-unified"
---

# VX — Desarrollo escalonado con objetivo final continuo

**Ámbito:** TODO proyecto de software autorizado (web, backend, ERP, móvil, desktop, industrial, herramientas, automatización). **No presupone Tauri** ni cambia de stack. La invoca `vx-dev-team` cuando la tarea requiere varios pasos, fases, dependencias o entregas continuas. Una tarea sencilla no necesita fases artificiales.

## Selección del método de ingeniería (Core 1.5 SOURCE)

Al entrar en una tarea de mutación, aplicar primero el gate `V0_BASELINE` de `vx-version-governance` (vía `vx-team-bootstrap` si la nueva Skill aún no está allowlistada). Un microcambio requiere versión/rama/estado verificable, **no** una ceremonia de planificación.

| Intención | Secuencia proporcional |
| --- | --- |
| `BUGFIX` | reproducir → causa raíz → corrección mínima → prueba de regresión |
| `FEATURE` | aceptación → contrato → vertical slice → incrementos |
| `REFACTOR` | invariantes existentes → mínima refactorización → equivalencia |
| `INTEGRATION` | contrato productor/consumidor → ownership → prueba de enlace |
| `DATA_MIGRATION` | compatibilidad/backup → ensayo aislado → gate R3 si aplica |
| `HOTFIX` | baseline/alcance → fix mínimo → smoke → análisis posterior |
| `NEW_PRODUCT` | objetivo/plataformas → tecnología elegida justificadamente → fases |
| `TECH_CHANGE` | conservar stack actual salvo justificación y autorización de cambio |

Cada fase hereda `change_ids`, versión observada, decisiones y tests `UPDATE|REPLACE|ADD`; la decisión `RELEASE_VERSION` sucede en el gate de release, no en cada edición. La preferencia Tauri 2 **solo se evalúa para un nuevo producto explícitamente Desktop**. Mantener Qt/PySide6/.NET/Electron y plataformas existentes en proyectos ya iniciados salvo migración encargada. El listado anterior describe métodos, no lanza subagentes ni concede ACL.

## Fuente de verdad: una meta final, progreso verificable

Antes de implementar, deducir de la conversación/repositorio los siguientes datos; no pedir formulario si son inferibles:

- `FINAL_GOAL`: una frase de resultado que el usuario pueda comprobar, no una lista de tareas técnicas.
- `CURRENT_BASELINE`: repo/branch/HEAD real, versión, funciones existentes y restricciones; `GIT_UNBORN_HEAD` o `GIT_NOT_APPLICABLE` cuando corresponda.
- `PLATFORM_SCOPE`: web, servidor, escritorio, Android, industrial, etc., **solo lo que pidió el operador**. No inferir Tauri para una web; si desktop explícito, evaluar la política del producto sobre Windows/Android.
- `ACCEPTANCE`: escenarios de usuario con resultado claro (p. ej. “sin conexión a Internet, Android controla la sesión autorizada en el PC”). Distinguir lo medido, lo propuesto y lo bloqueado.
- `DEPENDENCIES/RISKS`: arquitectura, hardware, herramientas, permisos, privacidad, compatibilidad, build.
- `ROADMAP_LIVE`: etapa vigente, evidencia previa, pasos siguientes y decisión pendiente; **una sola fuente viva** del proyecto, no archivos o pruebas históricos acumulativos.

## Etapas incrementales — orden lógico, no burocracia

| Fase | Salida verificable | Criterio para avanzar |
| --- | --- | --- |
| 0. Contexto / diagnóstico | Alcance y baseline real, objetivo final y restricciones | Dependencias y puntos peligrosos identificados |
| 1. Contratos / arquitectura | Interfaces, datos, seguridad y mapa mínimo de fases | No hay contradicciones o brechas críticas sin dueño |
| 2. Vertical slice | Una operación completa real desde interfaz hasta dominio/almacenamiento/red | Funciona con test focalizado y evidencia observable |
| 3. Funciones por prioridad | Incrementos de alto valor en lotes pequeños; UX/error/permisos | Cada incremento satisface aceptación y no rompe el anterior |
| 4. Integración por plataforma | Dependencias entre módulos, hardware, conexión/red o empaquetado según alcance | Contratos probados; cambios compartidos integrados en barrera |
| 5. Validación de entrega | Tests existentes focalizados, seguridad, UX, CI, builds reales | Salidas reales o bloqueo preciso, revisión distinta del autor cuando impacta |
| 6. Entrega / cierre | Documentación breve de uso, versión/changelog, PR/merge y rollback según política | `FINAL_GOAL` satisfecho o bloqueos explícitos, sin falsa declaración de listo |

Etapas pueden solaparse **solo** si sus dependencias están estables. Reutilizar hechos y artefactos previos: no repetir la fase 0 o pruebas de humo sin cambios de comportamiento. Actualizar la evidencia viva, no crear una “certificación” nueva por cada edición.

## Ejecución continua como equipo

1. El líder decide **qué cambia ahora** respecto al objetivo final; crea mini-contratos por funcionalidad, con `owner`, `allowed_paths` exactos, `depends_on`, interfaz estable y `acceptance`.
2. Delegar al especialista mínimo. En Kilo Desktop, `task(background: true)` solo si la herramienta real lo expone. Máximo cuatro tareas independientes en background y dos writers en archivos **exactos, exclusivos y disjuntos**; para proyectos Git un solo escritor de operaciones Git por worktree.
3. Mientras los hijos trabajan, el líder puede preparar el siguiente contrato, investigar otra dependencia o revisar material terminado. No escribir los archivos asignados ni consumir resultados incompletos. No hacer polling innecesario ni duplicar hijos por tardanza.
4. **Barrera de integración:** esperar resultados, verificar diff real/rutas, resolver discrepancias y ejecutar **solo pruebas focalizadas**. Hijo `DONE` ≠ entregable `VERIFIED`. La autorización Kilo Auto no equivale a permisos permanentes o producción.
5. Si el cambio introduce fallo, diagnosticar con el test existente, reparar la causa, actualizar/reemplazar test obsoleto y revalidar alcance. Evitar suites ad hoc crecientes, archivos `test_v1/test_v2/test_final`, evidencias ficticias y ramas huérfanas.
6. Tras incremento aceptado: registrar en el **mismo** roadmap vivo `DONE / NEXT / BLOCKED` con decisión técnica y razón; seguir la próxima fase directamente si el permiso/tarea lo permite. Archivar/eliminar ramas temporales solo después de merge/CI y respaldo verificado, nunca a ciegas.
7. Si cambia una premisa del usuario, **actualizar primero FINAL_GOAL, PLATFORM_SCOPE y decisiones dependientes**. No continuar una ruta ya invalida por inercia.

## Escalas de rigor proporcionales

- **Microcambio:** implementación directa, prueba localizada, cierre; sin comité ni fases auxiliares.
- **Módulo:** contrato + builder + revisión/QA puntual; usar la suite ya existente.
- **Sistema multi-plataforma:** vertical slice y matriz por plataforma/hardware, integración incremental; paralelismo solo en archivos seguros.
- **Industrial/seguridad/producción:** aprobaciones, drivers/certificaciones, contratos y rollback obligatorios; nunca saltar requisitos por ritmo.
- **Sin red/energía/herramienta:** preservar avance local, estados precisos y siguiente paso ejecutable; no fingir build ni dispositivo conectado.

## Seguimiento de avance sin inventar porcentajes

Medir unidades funcionales **completadas y aceptadas**, no número de prompts, agentes, archivos o tests creados. No reportar "% completado" si no hay backlog ponderado y aprobado. Reporte compacto:

`{final_goal, stage, completed_capabilities_with_evidence, in_progress, blocked_with_cause, next_critical_action, dependencies, runtime_tests_done, risks, branch_and_ci_status, release_readiness}`.

Ejemplo: **“Meta: aplicación Windows+Android que se comunica sin Internet. Fase 2: enlace LAN validado en PC y teléfono; Fase 3: reconexión y emparejamiento seguro pendientes; Bluetooth: no verificado; siguiente: prueba de dos dispositivos.”**

## Política transversal

No instalar herramientas, modificar Kilo HOME/MCP/AutoApprove, abrir firewall, subir secretos, cambiar stack, publicar APK/EXE ni migrar datos de producción sin una tarea autorizada que lo requiera. La skill organiza trabajo, no concede ACL ni capacidades al agente. Para proyectos de conectividad añadir `vx-conectividad-dispositivos` bajo demanda; para escritorio Tauri usar `vx-tauri-desktop` **solo** si ese es el motor del proyecto.
