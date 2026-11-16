---
description: Preparar análisis autorizado de IDA mediante MCP, sin escritura ni autoinstalación
---

# /vx-ida — Investigación binaria con IDA MCP (solo guía)

Activar la skill global `vx-ida-mcp-reverse-engineering` cuando el usuario pida análisis de binarios autorizados con IDA. Identificar el objetivo, comprobar que el servidor MCP **oficial** está conectado y qué herramientas read-only ofrece realmente. Nunca asumir que un MCP configurado ya está listo.

Proponer una secuencia triage → funciones → xrefs → ASM/pseudocódigo → informe con direcciones y procedencia. Separar datos confirmados de hipótesis. Si `ida-hcli` falla por `HCLI_CURRENT_IDA_PYTHON_EXE`, consultar el procedimiento de diagnóstico de la skill y no inventar rutas.

**Prohibiciones por defecto:** no instalar ni habilitar MCP, modificar `kilo.jsonc`, ejecutar binarios, ejecutar Python arbitrario, parchar bytes, modificar IDB, lanzar depurador, alterar permisos ni AutoApprove. Ante falta de ACL o conexión, reportar bloqueo y solicitar consentimiento por herramienta/objetivo. Ninguna invocación se ha realizado al mostrar este comando.
