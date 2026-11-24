# Integración Kilo Desktop
Versión del archivo: 0.1.0 | Última modificación: 2026-11-24

En F02 registrar versión real, ejecutable, engine, configuración efectiva, esquemas y precedencia. La documentación indica rutas candidatas:
- Agentes globales: ~/.config/kilo/agents/
- Skills globales: ~/.kilo/skills/<name>/
- Config global: ~/.config/kilo/kilo.jsonc
- Política global AGENTS.md: confirmar descubrimiento exacto; no adivinar ubicación.
- Proyecto: configuración, agents, skills y AGENTS.md según rutas realmente descubiertas.
No escribir aún en estas rutas. XDG/overrides y compatibilidad con otros clientes pueden cambiar resolución.
Matriz a comprobar: Code, general/explore, task foreground/background, task_id, nested, Swarm, skill, shell, edición/lectura, LSP, MCP, plugins, compaction, goals, worktrees, permisos y approvals. Para cada capacidad: documented / exposed / invoked / verified / unsupported; versión, evidencia y fallback.
Integración se realiza con configuración mínima y merge selectivo, no reemplazo completo de JSONC, no copia de auth.json ni claves. No alterar selección de modelo sin permiso. Detectar colisiones de nombres y reglas de proyecto; documentar precedencia y avisar si política local anula global. Usar settings de Desktop para validación cuando sea necesario.
