# Arquitectura de Kilo Global Harness V3

## Capas

1. **Kilo runtime**: configuración global preexistente `~/.config/kilo/kilo.jsonc`, credenciales y modelos seleccionados por el usuario; el harness no los copia ni reescribe.
2. **Política mínima universal**: sección delimitada `VX-HARNESS-V3` dentro de `~/.config/kilo/AGENTS.md`. Diseño para pocos tokens en cada conversación.
3. **Orquestación bajo demanda**: `~/.kilo/skills/vx-engineering-harness` y `~/.config/kilo/rules/vx-global-harness-v3.md`.
4. **Workflows**: Markdown global `~/.config/kilo/commands/vx-*.md` con objetivos acotados: plan, implementación, depuración, validación, diff, Git, retrospectiva, MCP, modelos y estado.
5. **Agentes especializados**: `vx-integrador` (primary) y `vx-inspector` (subagent readonly). No sobrescriben los 21 agentes existentes. `vx-inspector` restringe edición y Bash, pero su eficacia debe verificarse en runtime.
6. **MCP**: conservar conexiones existentes. `codebase-memory-mcp` para grafos verificables; memoria explícita para decisiones; documentación oficial según stack. MCP configurado no implica conectado.
7. **Git**: cambios normales autónomos permitidos por el encargo del usuario; `main` única rama duradera, ramas `work/*` temporales, protección de CI/revisión y eliminación de la rama propia SOLO después de verificar merge.

## Global-only y multi-repositorio

- `D:\Proyectos\Kilo-Global-Harness` es solamente fuente del instalador y documentación versionada, no directorio de ejecución de configuración.
- Cualquier repositorio abierto en VS Code utiliza los mismos agentes, skills y comandos globales.
- No crear ni sincronizar carpetas de configuración Kilo por repositorio.
- Leer archivos de proyecto `README.md`, `package.json`, etc. es correcto; prohibición solo afecta a archivos de configuración local del agente.
- Kilo puede cargar `AGENTS.md` y configuración local que un repositorio ya contenga, de acuerdo con precedencia del producto. El harness no puede impedirlo sin un mecanismo de restricción en el cliente; revisar si aparece una contradicción.

## Política de recursos

- Reducir duplicación de instrucciones; 1 skill principal por tarea, subagentes con resúmenes.
- No usar `steps=10000000` como supuesto presupuesto de tokens. Un ajuste numérico es decisión independiente que requiere revisar agentes y versiones reales.
- Memoria: verificar índice y cobertura antes de confiar en grafo; no persistir datos confidenciales.
- Congelar versiones MCP operativas; actualizaciones de skills auditadas en lote, sin tareas de actualización automáticas.
- Control de producción: deploys reales, migraciones destructivas, IAM/firewall y borrados ajenos NO se autorizan por AutoApprove.

## Fuentes de referencia

- https://kilo.ai/docs/getting-started/settings
- https://kilo.ai/docs/customize/agents-md
- https://kilo.ai/docs/customize/agent-permissions
- https://kilo.ai/docs/customize/custom-subagents
- https://kilo.ai/docs/customize/skills
- https://kilo.ai/docs/customize/workflows
