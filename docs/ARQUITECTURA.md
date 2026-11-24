# Arquitectura y estructura
Versión del archivo: 0.1.0 | Última modificación: 2026-11-24

## Capas
1. Host: Kilo Desktop y su engine, proveedor/modelo ya configurado. Code conserva modo y prompt nativos.
2. Comportamiento: política global breve, instrucciones del proyecto y skills bajo demanda; sin duplicar instrucciones nativas.
3. Equipo: agentes Markdown subagent; Code elige roles por descripción; general/explore existentes se reutilizan.
4. Coordinación: task foreground/background y board donde estén expuestos; contratos y propiedad de archivos; estado nativo primero, checkpoints propios solo si falta continuidad.
5. Conocimiento: catálogo modular de skills originales, referencias y evals; Team Learning prepara mejoras.
6. Integración: adaptadores de configuración nativa, MCP existentes y opcionales propios, plugins solo por carencia.
7. Distribución: manifiesto de propiedad, instalador Windows, pruebas, actualización y rollback. Estado de usuario separado del repositorio y de fuentes instalables.

## Estructura real de diseño
- AGENTS.md: reglas del repositorio; README.md: mapa.
- docs/: plan, roadmap, arquitectura, fuentes, investigaciones, instalación.
- team/policies/: fuente candidata de política global, no instalar aún.
- team/agents/: diseño de roles; luego un archivo por agente.
- team/skills/: catálogo; luego nombre/SKILL.md y referencias necesarias.
- team/contracts/: contratos de tareas/observaciones.
- team/learning/: diseño de mejora continua.
- integration/kilo/: mapeo y capacidades; futuras plantillas validadas.
- integration/mcp/: inventario y diseño de MCP propios; servidores solo tras F10.
- scripts/: plan de scripts; implementación en F02/F13.
- tests/: estrategia, posteriormente fixtures/evals y pruebas ejecutables.
- registry/: manifiesto y versiones verificadas; estado inicial no instalable.
- legacy/: archivo inmutable, excluido del paquete.

## Flujo
Usuario → Code → clasificación/objetivo/criterios → ejecución directa o DAG de tareas → especialistas y herramientas → integración → pruebas/revisión → entrega y Team Learning. El líder sigue trabajando en tareas no conflictivas; ningún agente se arroga identidad o permisos de otro. Swarm es mensajería, no lock ni sistema de autorización. Un worktree separado aísla checkout, no credenciales ni recursos externos.

## Estado
Separar definición versionada en Git, configuración instalada, credenciales del proveedor y datos efímeros. Checkpoints contienen identificadores, alcance, commit base, resultados y siguiente acción, nunca secretos. Identidad estable por proyecto y sesión; no basarse en basename. No afirmar persistencia tras cerrar Desktop sin prueba. Si una capacidad falta, degradar a ejecución secuencial o manual con evidencia.
