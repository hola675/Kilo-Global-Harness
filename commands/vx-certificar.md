---
description: Verificar carga de skills, descubrimiento de agentes y delegación Kilo VX sin elevar permisos
---

# /vx-certificar — prueba nativa controlada

Objetivo: $ARGUMENTS

La evidencia previa reporta dos llamadas exitosas a la herramienta nativa skill (vx-engineering-harness y vx-ida-mcp-reverse-engineering) y un bloqueo de glob al HOME por external_directory: deny. No constituye un certificado del equipo ni prueba conexión de IDA MCP. La identidad mostrada por el agente Kilo tampoco demuestra que vx-integrador esté seleccionado.

1. Solicita al operador comprobar visualmente en el selector si vx-integrador aparece como primary y los cinco builders están disponibles. Declara únicamente OBSERVADO_POR_OPERADOR si el operador lo confirma; no inventes una herramienta de lista de agentes.
2. Comprueba el uso nativo de skill en la sesión actual; no infieras carga por mera existencia de SKILL.md. Puedes usar skill para vx-engineering-harness o vx-ida-mcp-reverse-engineering si el objetivo lo requiere.
3. Si Kilo tiene herramienta task autorizada y el operador seleccionó vx-integrador, delega exclusivamente al subagente vx-inspector una revisión de solo lectura de un README.md del proyecto autorizado. Pídele primera cabecera y observaciones, sin edición, Bash o búsquedas del HOME. Si task no existe o deniega, conserva NO_VERIFICADO/BLOQUEADO.
4. No pruebes permisos negativos modificando archivos reales. Para comprobar edit/bash: ask de builders se requiere luego fixture temporal y autorización adicional. Una política en Markdown no acredita por sí sola permiso efectivo.
5. No uses glob ni read para buscar agentes globales fuera del proyecto. external_directory: deny es correcto; no ajustes permisos ni AutoApprove para eludirlo.
6. La carga de la skill de IDA no prueba ida-mcp. No ejecutes herramientas IDA, scripts, patch, debugger, conexiones ni procesos sin aprobación explícita.
7. Entrega un informe de cada gate: VERIFICADO, NO_VERIFICADO o BLOQUEADO; fuente, herramienta nativa realmente invocada y referencia mínima. Distingue archivos verificados, evidencia reportada, pruebas reales y estado no observado.

El validador local en el repositorio scripts/vx_runtime_smoke_v1.py imprime un JSON vacío con --template y verifica un JSON aportado por el operador con --check archivo.json. No obtiene pruebas del host, no escribe HOME y nunca concede certificación independiente por una declaración.
