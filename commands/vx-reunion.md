---
description: Revisar actas y decisiones de reuniones VX globales de Kilo Code, sin automatización ni publicación
agent: plan
---

Reunión VX global (Kilo Code exclusivamente, independiente del proyecto abierto): $ARGUMENTS.

**Calendario confirmado:** reunión semanal lunes a las 09:00, en la zona horaria local del equipo Windows. Cierre mensual **primer lunes del mes siguiente**, a las **09:00**, en una **única sesión conjunta** con secciones independientes: primero mensual y después semanal. No preparar dos reuniones separadas ese lunes. **No existe scheduler ni notificaciones automáticas en V4.5.**

Usa el script global `python -I "$HOME/.config/kilo/harness/scripts/vx_evolution_core.py"`, sin modificar código de proyectos. Primero consulta `status --json` y `meeting-calendar --cadence weekly|monthly --json`. La consulta del calendario NO crea BD ni reuniones.

En bases SQLite v2, `meeting-migrate --json` genera backup y actualiza explícitamente a v3; después `joint-migrate --json` genera otro backup y actualiza a v4. **No migrar de forma automática**. Si es v1, hace falta `observer-migrate` primero. NO migrar en respuesta a una mera consulta.

- `meeting-preview --cadence weekly|monthly --json`: ventana histórica del calendario local, agenda pendiente, sin creaciones.
- `meeting-joint-calendar --json`: plan de una sesión mensual/semanal, sin escribir en HOME.
- `meeting-joint-prepare --json`: crea explícitamente una sola sesión y dos secciones de acta, sin propuestas duplicadas; requiere SQLite v4. Si existen actas individuales previas coincidentes, se detiene para revisión manual.
- `meeting-joint-view --id <uuid> --json`: devuelve ambas secciones y sus actas por separado dentro de una misma sesión.
- `meeting-joint-close --id <uuid> --json`: cierre indivisible con confirmación local, rechaza puntos sin decidir en cualquiera de las dos secciones.
- `meeting-prepare --cadence weekly|monthly --json`: crea borrador en SQLite GLOBAL únicamente si el usuario lo solicita. Conserva las cinco propuestas más prioritarias en una agenda por período. **En el primer lunes requiere `meeting-joint-prepare`**. No convoca a nadie.
- `meeting-view --id <uuid> --json`: muestra acta, notas, propuestas y decisiones.
- `meeting-note --id <uuid> --text <resumen-sin-secretos> --json`: registra nota explícita neutra, sin datos de cliente ni rutas privadas.
- `meeting-decide --id <uuid> --proposal <uuid> --decision approved|rejected|deferred|revision_requested --json`: requiere una TERMINAL LOCAL INTERACTIVA, con desafío tecleado deliberadamente por el operador. No se debe automatizar la respuesta, no usar modo sin TTY, ni marcar como humano un agente; la identidad sigue NO VERIFICADA. Las decisiones quedan auditadas pero **nunca despliegan** agentes/skills.
- `meeting-close --id <uuid> --json`: cierre con confirmación de terminal y cero puntos de agenda sin decisión. Nunca aprobación por silencio.

No inventes métricas de tokens, calidad, rendimiento de equipos o resultados de pruebas. Los contadores de VX Observer V4.4 son únicamente señales del runtime. Cada mejora de skill/agente necesita evidencia independiente y revisiones de V4.6/V4.7; un `approved` de V4.5 **NO** equivale a autorización técnica de publicación.

La programación semanal o mensual en Windows solo podrá activarse tras pruebas de V4.5 y **una aprobación explícita nueva y separada**. Si preguntan por el estado, responde `scheduled_meetings=false`. Documento: `docs/VX-REUNION-V4.5.md` en el repositorio del harness.

Para registrar notas y decisiones de la sesión conjunta utiliza `meeting-note` y `meeting-decide` con el `meeting_id` de cada sección devuelto por `meeting-joint-view`. Esto conserva responsabilidades independientes sin abrir dos sesiones. **Ninguna confirmación habilita el scheduler.**
