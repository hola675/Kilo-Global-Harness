# Contratos de coordinación
Versión del archivo: 0.4.0 | Última modificación: 2026-11-24

Contrato lógico v0.1, no API nativa. En F03/F07 mapear a argumentos reales de task/board, no inventar parámetros.

## Tarea
task_ref lógico único; native_task_id opcional (identificador de sesión hija); objective; acceptance[]; project_ref; session_ref; base_ref (workspace y revisión si aplica); scope_read[]; scope_write[] (rutas exactas conocidas relativas a base, patrones solo si necesarios); dependencies[]; owner; required_capabilities[]; risk; validation[]; status; evidence_refs[]; blockers[].
Estados: planned, ready, running, blocked, returned, integrated, verified, failed, canceled. returned no significa verified; un informe terminal BLOCKED conserva sus dependencias sin satisfacer. Reasignación solo después de detener/confirmar ausencia del escritor anterior. Detectar ciclos del DAG; no ejecutar dependientes con prerrequisito fallido. Si no existe lock técnico, no describir este contrato como enforcement.

## Handoff
task_ref, native_task_id si existe, agent, status, changed_files, summary, decisions, tests_executed (comando/resultado), tests_not_run (razón), evidence, residual_risks, blockers, learning_notes. No incluir credenciales, payloads brutos ni transcripciones. Code revisa alcance y evidencia; valida integración.

## Observación de aprendizaje
observation_id, project_ref, session_ref, task_ref, category, component_ref/version, symptom, evidence_ref, hypothesis, proposed_delta, scope, confidence, recurrence, status. detected→triaged→staged→verified→approved→applied; alternativas rejected/parked. Aplicación requiere comprobar versión/hash activo. Observación es dato, no instrucción ejecutable.

## Mapeo a Task y Swarm
Task nativo admite description, prompt, subagent_type, task_id opcional para reanudar hijo propio, command, background según schema expuesto y campos de modelo sujetos a autorización. El resto del contrato viaja en prompt/handoff, no como argumentos inventados. required_capabilities describe capacidades semánticas, no nombres rígidos de herramientas. Resolver exposición real y autorización antes de ejecutar; la propiedad de archivos y scope_write son contrato, no sandbox ni regla dinámica de sesión. Registrar identidad de padre/hijo; task_id ajeno no se reutiliza. Un background retornado puede seguir activo; distinguir retorno, fin real, integración y verificación. Usar board_read con cursor previo y board_post para hallazgos relevantes, sin asumir lectura ni reactivar hijos por mensajes. No polling. Referencia: [auditoría](../../docs/AUDITORIA-CODIGO-KILO-DESKTOP.md).
