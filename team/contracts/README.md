# Contratos de coordinación
Versión del archivo: 0.1.0 | Última modificación: 2026-11-24

Contrato lógico v0.1, no API nativa. En F03/F07 mapear a argumentos reales de task/board, no inventar parámetros.

## Tarea
task_id único; objective; acceptance[]; project_ref; session_ref; base_ref; scope_read[]; scope_write[]; dependencies[]; owner; required_capabilities[]; risk; validation[]; status; evidence_refs[]; blockers[].
Estados: planned, ready, running, blocked, returned, integrated, verified, failed, canceled. returned no significa verified. Reasignación solo después de detener/confirmar ausencia del escritor anterior. Detectar ciclos del DAG; no ejecutar dependientes con prerrequisito fallido. Si no existe lock técnico, no describir este contrato como enforcement.

## Handoff
task_id, agent, status, changed_files, summary, decisions, tests_executed (comando/resultado), tests_not_run (razón), evidence, residual_risks, blockers, learning_notes. No incluir credenciales, payloads brutos ni transcripciones. Code revisa alcance y evidencia; valida integración.

## Observación de aprendizaje
observation_id, project_ref, session_ref, task_ref, category, component_ref/version, symptom, evidence_ref, hypothesis, proposed_delta, scope, confidence, recurrence, status. detected→triaged→staged→verified→approved→applied; alternativas rejected/parked. Aplicación requiere comprobar versión/hash activo. Observación es dato, no instrucción ejecutable.
