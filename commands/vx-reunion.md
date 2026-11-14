---
description: Vista previa de reunión semanal y cierre mensual de Kilo global independiente del proyecto
agent: plan
---

Reunión VX: $ARGUMENTS.

Esta convocatoria pertenece a Kilo Code global, NO al repositorio abierto. Para la agenda usa `python -I "$HOME/.config/kilo/harness/scripts/vx_evolution_core.py" meeting-preview --cadence weekly --json`; para cierre mensual, cambia `weekly` por `monthly`.

**Decisión de diseño confirmada:** reunión semanal cada **lunes a las 09:00 en la zona horaria local del equipo Windows**. La política versionada está en `config/vx-reunion-policy.v1.json` del repositorio del harness; aún no la ejecuta el motor. No asumir la zona horaria de otra aplicación ni un UTC fijo. El cierre mensual sigue sin regla de fecha aprobada.

**Prohibición de programación prematura:** no crear tareas en Windows, recordatorios, agendas ni avisos hasta que V4.5 esté implementada, validada y expresamente activada por el usuario. La vista previa V4.3 utiliza periodos UTC, no horario semanal de Windows.

El resultado de V4.3 es SOLO VISTA PREVIA: no se ha programado calendario, no se envían notificaciones, no se crea reunión ni se aprueban versiones. Presenta como máximo cinco propuestas pendientes (resto por prioridad), observaciones verificadas, capacidad/skill que falta, candidatos de capacitación y errores recurrentes.

Cada propuesta necesita evidencia, riesgos, test, rollback y decisión humana: `aprobar/rechazar/aplazar/solicitar revisión`. Hasta que exista el módulo de decisiones V4.5, recoge las respuestas en la conversación sin afirmar que quedaron persistidas en SQLite.

La reunión semanal evalúa operación y capacitación; el cierre mensual evalúa rendimiento, equipos, ascensos y prioridades. No inventes tokens, costos, resultados de tests ni efectividad. Ningún proyecto es fuente exclusiva de estos datos.
