---
description: Implementación autónoma con cambios mínimos y evidencia verificable
agent: code
---

Usa `vx-engineering-harness`. Revisa estado real de Git y dependencias. Para cambios no triviales aplica `/vx-git-ciclo`: rama temporal, pruebas, revisión y cierre. Selecciona solo skills necesarias, delega subagentes solo para tareas independientes y conserva AutoApprove sin eludir permisos. Si el cambio añade o modifica contratos entre Backend/Frontend/Data, documenta su identificador, rutas reales y dependencias; tras integrar a main aplica el protocolo `docs/VX-TEAM-CAPABILITY-HANDOFF-V1.md` para proponer tickets a los builders VX relevantes y al QA, reutilizando su rama activa reconciliada. No declarar un enrutador PLAN_ONLY como dispatcher activo; confirmar permisos host por tarea. No crees archivos de configuración Kilo dentro del repositorio. Valida y entrega resumen basado en resultados ejecutados. Tarea: $ARGUMENTS.
