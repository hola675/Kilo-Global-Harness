---
description: Revisar actas y decisiones de reuniones VX globales de Kilo Code, sin automatización ni publicación
agent: plan
---

Reunión VX global (Kilo Code exclusivamente, independiente del proyecto abierto): $ARGUMENTS.

**Calendario confirmado:** reunión semanal lunes a las 09:00, en la zona horaria local del equipo Windows. Cierre mensual **primer lunes del mes siguiente**, para revisar el mes anterior; su hora sigue **PENDIENTE**. Ambas sesiones pueden coincidir; el criterio para fusionarlas o separarlas requiere decisión humana. **No existe scheduler ni notificaciones automáticas en V4.5.**

Usa el script global `python -I "$HOME/.config/kilo/harness/scripts/vx_evolution_core.py"`, sin modificar código de proyectos. Primero consulta `status --json` y `meeting-calendar --cadence weekly|monthly --json`. La consulta del calendario NO crea BD ni reuniones.

En bases SQLite v2, `meeting-migrate --json` genera un backup y actualiza explícitamente a esquema v3 solo cuando el operador autorice la migración. Si es v1, hace falta `observer-migrate` primero. NO migrar en respuesta a una mera consulta.

- `meeting-preview --cadence weekly|monthly --json`: ventana histórica del calendario local, agenda pendiente, sin creaciones.
- `meeting-prepare --cadence weekly|monthly --json`: crea borrador en SQLite GLOBAL únicamente si el usuario lo solicita. Conserva las cinco propuestas más prioritarias en una agenda por período. No convoca a nadie.
- `meeting-view --id <uuid> --json`: muestra acta, notas, propuestas y decisiones.
- `meeting-note --id <uuid> --text <resumen-sin-secretos> --json`: registra nota explícita neutra, sin datos de cliente ni rutas privadas.
- `meeting-decide --id <uuid> --proposal <uuid> --decision approved|rejected|deferred|revision_requested --json`: requiere una TERMINAL LOCAL INTERACTIVA, con desafío tecleado deliberadamente por el operador. No se debe automatizar la respuesta, no usar modo sin TTY, ni marcar como humano un agente; la identidad sigue NO VERIFICADA. Las decisiones quedan auditadas pero **nunca despliegan** agentes/skills.
- `meeting-close --id <uuid> --json`: cierre con confirmación de terminal y cero puntos de agenda sin decisión. Nunca aprobación por silencio.

No inventes métricas de tokens, calidad, rendimiento de equipos o resultados de pruebas. Los contadores de VX Observer V4.4 son únicamente señales del runtime. Cada mejora de skill/agente necesita evidencia independiente y revisiones de V4.6/V4.7; un `approved` de V4.5 **NO** equivale a autorización técnica de publicación.

La programación semanal o mensual en Windows solo podrá activarse tras pruebas de V4.5 y **una aprobación explícita nueva y separada**. Si preguntan por el estado, responde `scheduled_meetings=false`. Documento: `docs/VX-REUNION-V4.5.md` en el repositorio del harness.
