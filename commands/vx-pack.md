---
description: Diagnosticar el Pack VX y preparar operaciones multiagente sin modificar Kilo ni los MCP
agent: vx-integrador
---

Analiza el estado del Pack VX para: $ARGUMENTS. Ejecuta primero el diagnostico pasivo con `python "$HOME/.config/kilo/harness/scripts/vx_pack_doctor.py" --json` si Python existe; de lo contrario explica el bloqueo. No muestres archivos de credenciales ni valores del JSONC.

Usa `/vx-equipo` para tareas reales, eligiendo el perfil y la menor cantidad de delegados necesaria. Los MCP configurados NO se consideran conectados; no instales, habilites, elimines ni modifiques uno sin autorizacion concreta por servidor. Evita ejecutar scripts remotos y ejecutar cambios sobre produccion.

No muevas agentes y skills legacy, ni reemplaces inline agents dentro de `kilo.jsonc`. Solicita revisión del inventario, backup privado completo y prueba de restauracion antes de cualquier futura sustitucion. Separa hechos de runtime verificado, metadatos declarados y propuestas.

Entrega estado de 12 agentes/10 skills, skills faltantes, solapamientos y MCP candidatos, limitaciones y siguiente paso seguro. La salida de inventario no certifica ejecucion nativa del agente o de Swarm.
