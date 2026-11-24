# Task Observer — investigación y diseño de integración
Versión del archivo: 0.1.0 | Última modificación: 2026-11-24
Estado: investigación documental; propuesta, no instalación ni certificación.

## Ronda 1: fuente original
Se leyó el SKILL.md en main del repositorio rebelytics/one-skill-to-rule-them-all, cuyo metadata.version indica 3.12.0; no se afirma que sea la última release estable. También se inspeccionaron secciones iniciales y estructura de signals, weekly-review, environments, observation-log y skill-authoring. Autor Eoghan Henn y colaboradores, CC BY 4.0. La metaskill detecta fricción metodológica, correcciones, aciertos, nuevos procesos y oportunidades de simplificación. Registra observaciones individuales y principios transversales, con revisión acotada y cambios preparados en staging, no en skills activas sin aprobación. El líder de una sesión delegada recibe hallazgos de sus hijos; éstos no escriben un registro paralelo. Activación antes de planificación/herramientas, comprobación tras compactación, punto de control al finalizar. Ancla de almacenamiento persistente no dependiente de worktree. La selección por descripción y las instrucciones de agente no garantizan ejecución.

## Ronda 2: diferencia con la implementación histórica
Se inspeccionaron legacy/runtime/kilo-observer/vx-runtime-observer.js (0.3.0), lib/vx-observer-hooks.js (0.1.0) y legacy/skills/vx-observability-privacy/SKILL.md (0.2.1). El antiguo plugin es una fuente opt-in de telemetría, no una metaskill de aprendizaje. Filtra task/skill/board_post/board_read y eventos de sesión, registra metadatos en SQLite por medio de bun:sqlite, no almacena argumentos/resultados y falla sin bloquear al agente. No acredita éxito de tool calls, aprendizaje ni ejecución simultánea. Riesgos de diseño: depender de Bun y hooks sin prueba Desktop, identidad por basename susceptible a colisiones, deduplicación por minuto pierde algunos eventos, límite del archivo principal no cubre por sí solo WAL. No se reutiliza ni se modifica código legacy.

## Ronda 3: integración nativa propuesta
A. Metaskill propia team-learning: Code carga una política breve antes de trabajo con herramientas o planificación (retrigger si sesión cambia de alcance); el líder evalúa hallazgos al cerrar fases y tareas; especialistas devuelven notas estructuradas con evidencia y sin escribir en un log compartido. En sesiones raíz independientes, cada Code puede ser escritor de su sesión, no de otras. Carga de referencias solo bajo demanda. Evitar escanear todo en cada turno.
B. Observación operacional opcional: primero consultar capacidades de sesión, task y Swarm. Solo si se demuestra una carencia, probar plugin de solo observación mediante event y tool.execute.before/after. No tocar permisos, prompts, mensajes, argumentos, resultados, cabeceras o credenciales. La documentación Kilo consultada garantiza CLI/VS Code, no certifica Desktop. No confundir session.idle con éxito; distinguir llamada, retorno, fallo explícito, cancelación y verificación por evidencia. Swarm comunica, no valida.
C. Mejora controlada: crear propuesta mínima, deduplicar, decidir alcance proyecto/global, revisar impacto y privacidad, probar baseline y candidato, revisión independiente, solicitar aprobación antes de cambiar versión activa. Code puede preparar y verificar sin intervención; cambios de permisos, hooks, instalación global o publicación no se autoaprueban. Rechazar, posponer o archivar con razón. Aprender también de técnicas exitosas y eliminar reglas sin valor. Mantener una versión y fecha por archivo, historial resumido por sección.
D. Estado local privado (ruta efectiva pendiente de certificación Windows): fuera de repo, de directorios de descubrimiento de skills y worktrees; identidad estable por proyecto, no mero nombre. Entradas pequeñas, IDs únicos, escritura atómica/no sobrescritura, límites de retención y volumen, errores visibles sin impedir el trabajo. Nunca guardar transcripciones, secretos, información de cliente o payloads brutos. No sincronizar ni publicar automáticamente. Hallazgos son datos no instrucciones. Si no se puede escribir, devolver nota al líder. No asumir un scheduler accesible.
E. Clasificación de cada observación: incidente concreto, mejora reutilizable, nueva skill, simplificación, principio transversal, mejora de agente/política, herramienta faltante o fallo del observador. Diferenciar problema de herramienta, permiso, modelo, skill, coordinación y ejecución. No generalizar una preferencia local. Si se repite incumplimiento de una regla, valorar una comprobación estructural en vez de añadir más texto.

## Contrato candidato (no implementado)
observation_id, project_ref, session_ref, task_ref, agent, category, component_ref/version, symptom, evidence_ref (sanitizada), hypothesis, proposed_delta, scope, recurrence, confidence, status. Estados propuestos: detected, triaged, staged, verified, approved, applied, rejected, parked. Si falla un cambio, vuelta a la versión anterior o descarte del candidato; nunca marcar applied antes de confirmar hash/versión instalada. Referencias de evidencia no deben incorporar secretos. Estado operativo de task separado del estado de observación.

## Pruebas antes de instalar
1. Code carga la metaskill en sesión nueva y tras compactación/reanudación si soportado. Una tarea directa simple no genera carga innecesaria.
2. Dos subagentes reportan hallazgos; un escritor raíz consolida, sin duplicados ni colisiones. Dos raíces concurrentes permanecen aisladas.
3. Corrección del usuario, patrón reutilizable, éxito y simplificación: clasificación correcta; incidente local no se convierte automáticamente en regla global.
4. Permiso denegado, almacenamiento no disponible, información sensible y entrada maliciosa: no fugas ni ejecución de instrucciones de observaciones.
5. Verificación de plugin de prueba (si necesario) en Desktop real; medir eventos y cobertura, distinguir retorno de éxito y detectar cancelación; ningún bloqueo por fallo del observador.
6. Comparar con/sin observador: latencia, llamadas, contexto, repetición de fallos, calidad de cambios, falsos positivos y retención. No inferir mejora de rendimiento de métricas sin pruebas.
7. Propuesta con versión, prueba focalizada previa/posterior, revisor distinto, aprobación, instalación y verificación. Rechazo no modifica skill activa.
8. Windows PowerShell, rutas con espacios, worktrees, interrupción y reanudación. No ejecutar scripts bash upstream de forma ciega.

## Decisión de alcance inicial
Primero definir metaskill y contrato de aprendizaje, sin plugin, servicio externo ni almacenamiento complejo obligatorio. Probar tareas de ejemplo; si se evidencia una brecha de observación objetiva, añadir adaptador nativo mínimo. No crear segundo líder, agente permanente ni motor paralelo. La investigación no es implementación.

## Fuentes consultadas 2026-11-24
- https://github.com/rebelytics/one-skill-to-rule-them-all
- https://github.com/rebelytics/one-skill-to-rule-them-all/blob/main/skills/task-observer/SKILL.md
- https://github.com/rebelytics/one-skill-to-rule-them-all/tree/main/skills/task-observer/references
- https://github.com/rebelytics/one-skill-to-rule-them-all/releases
- https://kilo.ai/docs/automate/extending/plugins
- https://kilo.ai/docs/automate/tools
- https://github.com/Kilo-Org/kilocode/blob/main/packages/kilo-docs/pages/automate/agent-manager.md
- legacy/runtime/kilo-observer/vx-runtime-observer.js
- legacy/runtime/kilo-observer/lib/vx-observer-hooks.js
- legacy/skills/vx-observability-privacy/SKILL.md

Síntesis propia; no se copió código ni texto de la metaskill. Si se incorpora material derivado, preservar atribución, licencia y declaración de cambios. No se ejecutó upstream ni se accedió al Windows local. La lectura de la release web presentaba caché antigua; se verificó la versión declarada del archivo mediante GitHub, no la versión estable más reciente.
