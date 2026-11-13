---
description: Validacion de cierre y consolidacion Git automatica segura
agent: code
---
Usa `verification-before-completion`. Verifica pruebas, diff, staged files, secretos
expuestos y consistencia de la rama de trabajo. Si pasa, sigue la politica global
Git del Harness V3: merge/PR a main, push confirmado, borrar SOLO rama creada
para esta tarea y comprobar main remota. Autonomia autorizada para este flujo,
pero NO sortear aprobaciones del runtime, controles de main ni fallos de CI.
Si algo falla, conserva la rama y explica el bloqueo. Entrega evidencias de pruebas,
commit SHA, estado local/remoto y acciones realmente realizadas. No desplegar.
