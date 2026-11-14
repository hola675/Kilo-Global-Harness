---
description: Evaluar agentes y jerarquías Kilo para proponer capacitación, fusión o creación de equipos
agent: plan
---

Auditoría del equipo global Kilo: $ARGUMENTS.

Combina `/vx-reconciliar` (fuentes JSONC/Markdown), el registro VX de siete agentes/roles y `status` de VX Evolution. Examina permisos efectivos cuando el runtime lo permita, capacidades repetidas, fallos repetidos, criterios de supervisión, calidad verificable, coste conocido y dependencias. Distingue datos de hipótesis.

La promoción o nombramiento de jefe no es automática: requiere evaluador independiente, evidencia de coordinación y revisión de permisos. Un senior puede seguir implementando cuando el problema lo requiere. No crear jerarquías cíclicas, niveles vacíos ni agentes nuevos si puede resolverse con una skill.

Presenta una propuesta de reorganización, ascenso, contratación, fusión o retiro para `vx-reunion`. Regístrala con `propose --kind team --target <equipo> --title ... --reason ...` solo cuando se solicite. La BD tiene una tabla de relaciones reservada, pero NO activa ni publica esos cambios en V4.3.

Mantén un único escritor de archivos; conserva las configuraciones privadas, AutoApprove y todas las capacidades existentes hasta pruebas.


**V4.6.0 — diagnóstico primero:** usar `/vx-capacidades` como línea base **solo lectura**, y `/vx-reconciliar` como comprobador complementario de campos y límites. No afirmar precedencia de JSONC/Markdown, jerarquía, desempeño o rangos a partir de nombres, fingerprints o permisos declarados. Analizar el inventario global de Kilo **en una sola PC Windows**; no requerir nuevos MCP ni sincronización. La decisión de ascenso, jefatura, fusión o retiro quedará como propuesta pendiente de pruebas y aprobación humana independiente. `NO_VERIFICADO` y `NO_MEDIDO` son resultados válidos. Consultar `docs/VX-CAPACIDADES-V4.6.0.md`.

**V4.6.1 — revisión rigurosa:** usar `/vx-matriz` como referencia de competencias declaradas y de test IDs. No calificar roles ni proponer ascenso por contar PASS de un JSON; la rúbrica de aprendiz/especialista/senior/líder/principal es futura y requiere resultados independientes. Referencia: `docs/VX-MATRIZ-COMPETENCIAS-V4.6.1.md`.

**V4.6.2 — no confundir escenarios con calidad:** `/vx-ensayos` sólo compara archivos locales de decisiones enumeradas frente a fixtures públicos. Los posibles errores y regresiones son hipótesis de capacitación, no justificación de ascenso, retiro, contratación, permisos o jerarquías. CI de harness tampoco mide agentes.
