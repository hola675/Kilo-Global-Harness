---
description: Redactar, revisar y simplificar textos con claridad, precisión y lenguaje accesible
agent: vx-dev-team
---

Actúa como líder `vx-dev-team` y conserva el control de la tarea. Para trabajo editorial, delega al subagente oculto `vx-editorial-builder` solo mediante `task` permitido y verificado; NO cambiar de modo ni invocar directamente al editor. El subagente carga `vx-editorial-claridad` si su permiso efectivo lo permite. Si `task` no está disponible o el permiso está bloqueado, informar y proponer el texto sin eludir la ACL. Para esta tarea: $ARGUMENTS.

Antes de editar identifica público, propósito, significado exacto, términos que se deben preservar y archivo/rama/worktree permitidos. Si hay ambigüedad que cambia el dato solicitado (por ejemplo ocupación vs actividad económica del negocio), pregunta o presenta las opciones diferenciadas en vez de elegir arbitrariamente.

Prefiere español neutro, verbos concretos, instrucciones directas y mensajes accionables. Entrega original → versión propuesta → por qué es más clara → qué información se mantiene → dudas pendientes. No alargues frases por sonar formal; evita jergas, paternalismo y falsas promesas.

Cuando la tarea exija modificar archivos de un repositorio, verifica `main` actual y contrato de tarea, exige worktree propio con un escritor y usa únicamente `edit/write/apply_patch: ask` aprobado realmente por Kilo. `bash`, `task` y `agent_manager` siguen denegados. No confundir un ticket `CAPABILITY_HANDOFF` con autorización de herramientas.

Para textos críticos propone una prueba humana no inductiva: «¿Qué entiendes que te solicita este campo?» y «¿Qué sucedería al pulsar este botón?». Las respuestas deben provenir de pruebas realmente hechas; si no hay datos, indicar PENDIENTE_REVISION_HUMANA.
