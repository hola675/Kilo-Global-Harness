---
description: Consultar e inicializar el registro global VX Evolution Core SOLO para Kilo Code
agent: plan
---

Operación de VX Evolution exclusiva de Kilo Code: $ARGUMENTS.

El motor está instalado en `~/.config/kilo/harness/scripts/vx_evolution_core.py` y utiliza Python 3.13+ con biblioteca estándar. Si está disponible, primero consulta `python -I "$HOME/.config/kilo/harness/scripts/vx_evolution_core.py" status --json`. En Windows también puedes resolver `$HOME\.config\kilo\harness\scripts\vx_evolution_core.py` desde PowerShell.

- `status`, `integrity`, `meeting-preview`: lectura sin crear ni modificar BD.
- `init`: inicialización explícita que **crea** SQLite privado global; nunca dentro del repositorio abierto. No hacerlo por iniciativa propia si el usuario pidió solo inspeccionar.
- `inventory-sync`: actualización explícita de metadatos de agentes/skills globales, sin modificar los archivos fuente.
- `observe`, `propose`: registran datos únicamente cuando el objetivo solicita almacenar una observación/propuesta, nunca enviar código privado o secretos como argumentos.
- `backup`: crea una copia manual; no restaurar ni borrar backups sin revisión.

No ejecutes hooks, modelos ni MCP para operar la base; usa el CLI local. Nunca ejecutes aprobación/publicación porque aún NO está implementada. Si la herramienta no está instalada o la BD no existe, indica qué falta. No inventes ejecuciones.
