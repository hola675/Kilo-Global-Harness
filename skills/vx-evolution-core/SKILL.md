---
name: vx-evolution-core
description: "Gobernanza global y versionada del ecosistema de agentes y skills de Kilo Code: consultar registro, observaciones, propuestas, capacitación, auditoría organizativa y reuniones VX. Activar solo para solicitudes sobre mejorar o administrar el harness, no en cada tarea de programación."
---

# VX Evolution Core V4.5 — exclusivo Kilo Code

## Principios
- Los datos residen en HOME/.config/kilo/vx-evolution/, separados del repositorio activo. Los archivos de runtime Kilo permanecen en sus rutas globales.
- Evitar cargar skills, agentes o proveedores de otros clientes. Solo Kilo y sus rutas compatibles reconocidas.
- Solo un escritor de estado SQLite; múltiples lectores. No publicar modificaciones en agentes o skills directamente desde observaciones.
- Diferenciar **existencia de inventario**, **evidencia de desempeño**, **propuesta**, **aprobación**, **versión validada** y **versión activa**.
- Un autor no puede certificar por sí solo la calidad de su mejora. Las promociones y cambios de permisos requieren evaluación externa y aprobación humana explícita.
- No registrar datos sensibles, prompts completos, código ni rutas de clientes. Los resúmenes son genéricos y el identificador de proyecto es HMAC local.

## Uso bajo demanda
Motor: `python -I "$HOME/.config/kilo/harness/scripts/vx_evolution_core.py"`.
Consultar `status`; crear BD con `init` solo cuando esté autorizado; usar `inventory-sync` para global Kilo; `observe` para observación importante; `propose` para candidato de mejora. `meeting-preview` muestra semanal o mensual sin programar nada.

## Responsables lógicos
- `vx-equipo`: coordinación de tareas actuales.
- `vx-observer`: observaciones de calidad manuales; en V4.4 puede contar tres señales del runtime mediante plugin global opcional y explícitamente activado.
- `vx-upgrade`: cambios/versiones propuestos, sin desplegar.
- `vx-capacitacion`: mejora de skills en estado candidato.
- `vx-auditoria-equipo`: análisis de roles, duplicados, jefes/subordinados.
- `vx-reunion`: semanal lunes 09:00 hora local Windows; mensual primer lunes del mes siguiente (hora pendiente), actas y decisiones manuales.

## Gates
Una observación no es verdad hasta revalidarse. Una propuesta `pending_review` no está aprobada. Un hash no es versión semántica. Una tabla `decisions` vacía no representa permiso. No modificar `kilo.jsonc`. La V4.4 permite instalar el plugin exclusivamente global mediante switch del instalador y habilitar contadores con `observer-mode light` tras una petición explícita. Nunca tomar una señal como resultado evaluado.

Documentación fuente: `docs/VX-EVOLUTION-V4.3.md` en la versión de desarrollo del harness; en el HOME instalado usar este skill y los comandos, sin buscar documentos de otros clientes.

## Observabilidad segura V4.4

Consultar `observer-status`, `observer-report --days 7` antes de afirmar que hay datos. Solo esquema SQLite v2; para historial v1, migración `observer-migrate` explícita con backup. El hook no captura tareas terminadas ni métricas de tokens: solo recuenta `session_idle`, `session_error`, `session_compacted`. No crear propuestas, aprobaciones o evaluaciones automáticamente a partir de esos números. La instalación del plugin y la activación son opt-ins separados y reversibles. Ver `docs/VX-OBSERVER-V4.4.md`.


## V4.5 — Reuniones sin programación

`meeting-calendar --cadence weekly|monthly` consulta fecha local sin crear BD; `meeting-preview` muestra propuestas y ventanas de revisión. El esquema v3 requiere `meeting-migrate` **explícito**, con backup previo de v2. `meeting-prepare` solo crea agenda cuando lo solicita el operador; `meeting-view` lee acta; `meeting-note` añade notas neutras; `meeting-decide` y `meeting-close` exigen confirmación en una **terminal interactiva local** que no debe responder un agente por su cuenta. La identidad no está verificada criptográficamente: ninguna decisión autoriza publicar agentes o skills. El scheduler semanal y mensual permanece apagado, incluso tras aprobar una propuesta. Referencia: `docs/VX-REUNION-V4.5.md`.
