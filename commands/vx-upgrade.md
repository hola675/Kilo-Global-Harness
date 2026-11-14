---
description: Gestionar propuestas de versionado de agentes y skills Kilo sin autoaprobar ni desplegar
agent: plan
---

Analiza la propuesta de mejora: $ARGUMENTS.

Consulta el estado global con `python -I "$HOME/.config/kilo/harness/scripts/vx_evolution_core.py" status --json`. Comprueba que el componente sea propio de Kilo Code y su versión real esté verificada; el hash del inventario no es una versión SemVer.

Formula problema, evidencia, alcance, dependencias, versión candidata propuesta, pruebas mínimas, riesgos, regresiones y rollback. Antes de recomendar un nuevo agente comprueba si una skill o capacitación existente resuelve el problema.

Si se solicita registrar la propuesta, usa `propose --kind agent|skill|team|core|governance --target <id> --title <texto-sin-secretos> --reason <texto-neutro> --priority P0|P1|P2|P3 --version 1.2.0-rc.1`. El estado devuelto es `pending_review`, no una aprobación.

No crees/modifiques activos, no cambies permisos, no te promociones y no hagas deploy. La activación versionada y rollback automático se implementarán en V4.7 tras decisiones y pruebas independientes.
