---
description: Diagnosticar el Pack VX y preparar operaciones multiagente sin modificar Kilo ni los MCP
agent: vx-integrador
---

Analiza el estado del Pack VX para: $ARGUMENTS. NO ejecutes Bash desde Kilo para inspeccionar HOME si external_directory esta denegado. El operador puede ejecutar el doctor desde su PowerShell externo cuando sea necesario. No muestres archivos de credenciales ni valores del JSONC.

Usa `/vx-equipo` para tareas reales, eligiendo el perfil y la menor cantidad de delegados necesaria. Los MCP configurados NO se consideran conectados; no instales, habilites, elimines ni modifiques uno sin autorizacion concreta por servidor. Evita ejecutar scripts remotos y ejecutar cambios sobre produccion.

No muevas agentes y skills legacy, ni reemplaces inline agents dentro de `kilo.jsonc`. Solicita revisión del inventario, backup privado completo y prueba de restauracion antes de cualquier futura sustitucion. Separa hechos de runtime verificado, metadatos declarados y propuestas.

Entrega estado de 12 agentes/31 skills, skills faltantes, solapamientos y MCP candidatos, limitaciones y siguiente paso seguro. La salida de inventario no certifica ejecucion nativa del agente o de Swarm.


**Evidencia funcional:** si el usuario pide verificar el runtime, utiliza /vx-certificar. Dos llamadas nativas exitosas a skill no demuestran descubrimiento de agentes, permisos de builders, delegacion ni conexion IDA MCP. Las 11 coincidencias inline/Markdown del doctor corresponden a agentes heredados, no a IDs VX; no cambiar configuraciones ni permisos por ese inventario. El instalador vigente para el HOME con inline y skills externas es Instalar-Pack-VX-Convivencia-V023.ps1, condicionado a simulacion limpia, respaldo DPAPI y Kilo cerrado.

**Auditoría de sustitución:** existen dos vías distintas: `Instalar-Kilo-Global-Harness.ps1 -Modo Diagnostico|Simular` (incremental, sin desactivar legacy) y `vx_pack_bootstrap.py --mode diagnose|simulate` (sustitución completa bajo preflight Windows/DPAPI). Nunca confundir los respaldos de ambos instaladores. Para `apply` o `restore` del bootstrap se exige acción humana explícita, inventario y cierre de sesiones de Kilo, no solo un informe del doctor. La verificación de archivos puede mostrar 31 skills VX; su carga efectiva necesita /reload y traza del tool skill. No equiparar ambas evidencias.
