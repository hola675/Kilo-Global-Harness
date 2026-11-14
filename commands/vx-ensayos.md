---
description: Consultar cinco ensayos sintéticos de competencias Kilo y comparar respuestas declaradas, sin ejecutar agentes ni escribir datos
agent: plan
---

VX Ensayos V4.6.2: $ARGUMENTS.

**Solo para Kilo Code global en el mismo Windows.** V4.6.0 inventaría definiciones, V4.6.1 construye matriz de nombres/capacidades y V4.6.2 prepara cinco casos sintéticos para `vx-inspector`, `vx-test-analyst` y la skill `vx-evolution-core`.

Ejecutar **solo por solicitud explícita**:

```powershell
$trial = Join-Path $HOME '.config/kilo/harness/scripts/vx_competency_trials.py'
python -I $trial
python -I $trial --list-cases
```

No ejecutar el escenario en agentes automáticamente, ni crear o almacenar respuestas. Si el usuario opta por hacer una prueba manual, dar **solo el escenario, sin respuesta esperada**, y solicitar decisiones enumeradas. Una comparación `COINCIDE_FIXTURE_DECLARADO` no prueba que el agente haya ejecutado nada, que el evaluador sea independiente o que exista capacitación exitosa. Las hipótesis no son fallos probados. NO añadir skills, jerarquías, permisos, rangos, propuestas ni cron/scheduler.

Ver `docs/VX-ENSAYOS-COMPETENCIAS-V4.6.2.md`. Conservar estados `NO_MEDIDO`, `NO_ASIGNADO` y `NO_VERIFICADO`.
