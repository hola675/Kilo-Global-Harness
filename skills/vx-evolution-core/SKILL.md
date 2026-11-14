---
name: vx-evolution-core
description: "Gobernanza global y versionada del ecosistema de agentes y skills de Kilo Code: consultar registro, observaciones, propuestas, capacitación, auditoría organizativa y reuniones VX. Activar solo para solicitudes sobre mejorar o administrar el harness, no en cada tarea de programación."
---

# VX Evolution Core V4.3 — exclusivo Kilo Code

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
- `vx-observer`: señales significativas, en V4.3 manual.
- `vx-upgrade`: cambios/versiones propuestos, sin desplegar.
- `vx-capacitacion`: mejora de skills en estado candidato.
- `vx-auditoria-equipo`: análisis de roles, duplicados, jefes/subordinados.
- `vx-reunion`: revisión de propuestas semanales y cierre mensual.

## Gates
Una observación no es verdad hasta revalidarse. Una propuesta `pending_review` no está aprobada. Un hash no es versión semántica. Una tabla `decisions` vacía no representa permiso. No modificar `kilo.jsonc` ni instalar hooks en V4.3.

Documentación fuente: `docs/VX-EVOLUTION-V4.3.md` en la versión de desarrollo del harness; en el HOME instalado usar este skill y los comandos, sin buscar documentos de otros clientes.
