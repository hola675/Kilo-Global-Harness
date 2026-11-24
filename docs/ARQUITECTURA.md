# Arquitectura y estructura
Versión del archivo: 0.3.0 | Última modificación: 2026-11-24

## Capas
1. Host: Kilo Desktop y su engine, proveedor/modelo seleccionado por el usuario. Code conserva modo y prompt nativos. Selección de modelos independiente de roles, skills y coordinación.
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

## Ajustes derivados de la auditoría
Desktop (kernel Electron/React y plugins) → kilo.core → CLI empaquetado kilo serve → sesión Code → Task hijas. Desktop work session agrupa chats; chat equivale a sesión del motor, no a un trabajador autónomo. Workspace-board visual no es Swarm; cola de prompts no es grafo de dependencias.
La coordinación usa eventos de finalización del Task y árbol de sesiones nativos; no implementar scheduler/polling/servidor adicional. Un contrato es lógico: no extender schema Task ni confundir task_ref del Harness con task_id nativo de reanudación.
Separar configuración global XDG, perfil administrado KILO_CONFIG_DIR y configuración de proyecto/checkout principal. No escribir en perfil administrado ni sidecar de Desktop. Reutilizar gateway desktop_* sin acceder a su autenticación interna. Plugins de motor y Desktop tienen ciclos y contratos distintos.
La auditoría indica sandbox de agente deshabilitado en el snapshot Desktop: aislamiento de checkout no es sandbox de ejecución. Restringir herramientas o usar entorno aislado verificable cuando el riesgo lo requiera. Referencia: [auditoría](AUDITORIA-CODIGO-KILO-DESKTOP.md).

## Resiliencia frente al modelo
Capas de control (diseño, no runtime instalado): selección nativa autorizada → contrato de tarea y contexto suficiente → ejecución acotada según capacidades observadas → verificación objetiva → integración o corrección acotada → aprendizaje reutilizable. El modelo interpreta y ejecuta; el contrato define qué se acepta, las herramientas aportan evidencia y el líder integra. Ninguna capa garantiza compensar ausencia de razonamiento, contexto o tool calling. No rebajar controles ni cambiar proveedor sin autorización. Comparación entre modelos en F12; reutilizar fixtures y pruebas existentes. Política normativa en [plan maestro](PLAN-MAESTRO.md).
