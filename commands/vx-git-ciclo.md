---
description: Ejecutar ciclo Git controlado con rama temporal y main permanente
agent: code
---

Trabaja sobre el repositorio Git realmente abierto. Primero comprueba `git status --porcelain`, `git branch --show-current`, remotos y `main`; NO sobrescribas cambios preexistentes del usuario. Para una tarea no trivial inicia una sola rama propia `work/<resumen>` desde `main` actualizada. Revisa los cambios, ejecuta pruebas adecuadas y documenta PASS/FAIL. Usa PR si existe requisito de revisión o CI. Cuando la integración a `main` esté confirmada en el remoto, elimina exclusivamente la rama temporal creada para esta tarea si no tiene cambios sin integrar. Nunca borres otras ramas, nunca force push ni uses `reset --hard`. Si falta autorización, protecciones GitHub o controles de CI, comunica el bloqueo. No crear archivos de configuración de Kilo dentro del repo. Usa argumentos de esta ejecución: $ARGUMENTS.
