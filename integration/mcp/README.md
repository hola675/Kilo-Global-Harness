# Estrategia MCP y plugins
Versión del archivo: 0.1.0 | Última modificación: 2026-11-24

F09: primero inventariar herramientas existentes y nativas. Para cada servidor: nombre, origen oficial, versión fijada, transport, capacidades, ámbito, dependencias, permiso, estado de conexión, llamada inocua y agentes autorizados. No registrar secretos. No instalar catálogo entero ni confiar solo en marketplace o tool annotations.
Candidatos sujetos a revisión: GitHub oficial (repositorios), Playwright (navegador/pruebas), Chrome DevTools (diagnóstico), shadcn (componentes), documentación técnica (fuentes oficiales), diseño/imagen según herramientas ya instaladas y autorizadas, análisis de código/LSP y DB solo si requeridos. Reutilizar MCP ya presentes. Elegir un navegador principal por tarea; no duplicar Playwright/DevTools si no hay beneficio.
F10: MCP propios solo para carencias demostradas. Candidatos:
| Candidato | Brecha a demostrar | Herramientas propuestas |
|---|---|---|
| team-state | no existe persistencia/consulta nativa de contrato | status, checkpoint, list_ready (alcance local) |
| team-learning-store | archivos simples insuficientes para consolidación segura | add_observation, list_relevant, stage_proposal |
| team-capabilities | inventario nativo insuficiente o no consultable | list_verified, explain_unavailable |
No desarrollar tres servidores por obligación. Consolidar si comparten seguridad/estado; preferir cero MCP propios si nativo cubre. No duplicar Task/Swarm/Git, no ejecutar shell arbitrario por MCP ni exponer secretos.
## Desarrollo si se justifica
Especificación de herramientas y esquema JSON, errores estructurados, idempotencia, validación de rutas/inputs, aislamiento por proyecto, cuotas y cancelación. SDK oficial compatible con host, versiones y lockfile fijados, transporte stdio local por defecto para servicios locales; HTTP solo con necesidad, auth y revisión. Herramientas de lectura separadas de mutación; autorización real en servidor además de permisos cliente. Las anotaciones son informativas, no controles. Pruebas unitarias, contrato, handshake/tools/list/call, permisos negativos, inyección, límites, errores, desconexión y prueba con Code/subagente real. No enviar datos a terceros sin autorización.
Fuentes: https://kilo.ai/docs/automate/mcp/using-in-kilo-code ; https://modelcontextprotocol.io ; https://ts.sdk.modelcontextprotocol.io/ ; https://github.com/anthropics/skills/tree/main/skills/mcp-builder ; https://github.com/microsoft/playwright-mcp ; https://github.com/ChromeDevTools/chrome-devtools-mcp ; https://github.com/github/github-mcp-server . Validar versiones concretas en fase.
