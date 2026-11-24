# Fuentes y metodología de investigación
Versión del archivo: 0.2.0 | Última modificación: 2026-11-24

Base: los tres documentos INVESTIGACION-* de docs/. Revisión adicional documental 2026-11-24:
- Kilo: https://kilo.ai/docs/customize/custom-subagents ; https://kilo.ai/docs/customize/agent-permissions ; https://kilo.ai/docs/customize/skills ; https://kilo.ai/docs/customize/marketplace ; https://kilo.ai/docs/desktop/settings/ai ; https://kilo.ai/docs/automate/tools ; https://kilo.ai/docs/getting-started/settings ; https://kilo.ai/docs/automate/mcp/using-in-kilo-code . Usar esquema/rutas como candidatos, verificar Desktop.
- Agent Skills: https://github.com/agentskills/agentskills ; https://agentskills.io/specification ; https://github.com/anthropics/skills/tree/main/skills/skill-creator ; https://github.com/anthropics/skills/tree/main/skills/mcp-builder . Formato, activación progresiva, evaluaciones y herramientas.
- MCP: https://modelcontextprotocol.io ; https://ts.sdk.modelcontextprotocol.io/ ; https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/ . Verificar protocolo negociado, SDK, seguridad y límites.
- Dominio: https://asvs.owasp.org/ ; https://wstg.owasp.org/ ; https://github.com/microsoft/playwright-mcp ; https://github.com/ChromeDevTools/chrome-devtools-mcp ; https://github.com/microsoft/skills . WCAG/W3C, NIST SSDF y documentación de stacks son candidatos de investigación futura, no auditorías ya realizadas.
- Patrones: Oh My OpenAgent, Superpowers, GSD Core, OpenCode Swarm, Oh My ClaudeCode, Beads, Gas Town, OpenHands, Task Observer, OpenAI y Anthropic: ver investigaciones existentes.

Por cada skill/MCP nuevo registrar fuente primaria, commit/release cuando exista, fecha, licencia, patrón, divergencias, límites y evidencia de evaluación. Preferir estándares y documentación del mantenedor a listados comerciales. No confundir resultado indexado con auditoría de código. Crear síntesis propia; revisar licencia y atribuir si se incorpora material derivado. No enviar datos de cliente a fuentes externas. Fuentes actuales deben volver a verificarse al implementar; no instalar desde URL sin fijar versión. No se ejecutaron harness externos ni se certificó Desktop en esta fase.

## Especialistas F05
[Investigación comparada de especialistas](INVESTIGACION-ESPECIALISTAS.md): registro por commit, archivo, licencia API, popularidad y síntesis de patrones. No confundir estudio selectivo con auditoría integral. Sin material externo copiado ni ejecución de harness.
