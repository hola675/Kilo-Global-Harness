---
description: Validar DAG, responsables y prerequisitos de tareas VX sin lanzar agentes
agent: vx-integrador
---

Recibe ruta de plan JSON autorizado en el argumento: $ARGUMENTS. Lee antes la skill `vx-task-dependency-graph` si está disponible; su contenido no sustituye autorización. Ejecuta `python "$HOME/.config/kilo/harness/scripts/vx_task_dag.py" --plan <RUTA_DE_PLAN>` con ruta literal de archivo (no concatenar shell a partir de texto no confiable). Este validador es solo lectura, trabaja sobre estados declarados, no demuestra revisión humana ni pone sesiones RUNNING por sí mismo. Devuelve orden topológico, tareas listas, bloqueadas, riesgos, ausencia de paralelismo de escritura y permisos pendientes. No enviar secretos ni datos de clientes en el plan. Si falta archivo o parser, explicar `NO_VERIFICADO`.
