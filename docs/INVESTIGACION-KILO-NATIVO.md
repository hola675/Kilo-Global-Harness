# Investigación inicial — Kilo Desktop Native Team
Versión del archivo: 0.1.0 | Última modificación: 2026-11-24
Estado: investigación documental; certificación de runtime pendiente.

## Decisión de arquitectura
Code (identificador nativo a confirmar en runtime: code) es el único líder del equipo. No se crea un modo primario personalizado ni se sustituye el prompt nativo. El resto de especialistas son agentes mode: subagent; se aprovechan general y explore existentes. La implementación archivada en legacy/ es referencia, no dependencia ni fuente de instalación.

## Evidencia y alcance
- Desktop comparte motor con Kilo y permite seleccionar Code, gestionar agentes, skills y MCP, aprobar acciones y utilizar worktrees. Desktop 0.1.16 (2026-11-13) añadió sesiones multiagente; 1.0.0 (2026-11-17) alcanzó disponibilidad general. Las pestañas multiagente no equivalen a delegación ni a un Swarm compartido.
- El motor documenta task en primer plano y background:true, entrega de resultados al padre, reanudación con task_id y delegación anidada según permisos/profundidad. Los hijos comparten directorio/worktree; el contexto separado no aísla archivos.
- Swarm aporta board_post y board_read entre descendientes de una sesión, no entre sesiones independientes; mensajes no cambian permisos ni interrumpen procesos. No usar polling continuo. Confirmar exposición en Desktop instalado.
- Los subagentes admiten Markdown, mode: subagent, permisos por rol, modelo opcional y carga de skills. La configuración global y de proyecto se combina; confirmar rutas y precedencia en el binario Desktop real.
- AGENTS.md contiene políticas compartidas; skills se cargan según tarea. No modificar el agente Code mediante prompt sustitutivo. Probar instrucciones globales y específicas de proyecto.
- MCP: Desktop muestra catálogo, alcance y estado de conexión. Conexión no demuestra herramientas invocables ni autorización; inventariar por agente y comprobar una llamada inocua por capacidad. No copiar credenciales ni duplicar MCP existentes.
- Plugins JS/TS: hooks, herramientas, eventos, compaction y permisos documentados para CLI/VS Code. Desktop no se da por certificado por compartir motor. No incorporar plugin propio hasta probar una carencia real y la compatibilidad. No autoaprobar operaciones protegidas mediante hooks.
- Session Goals (/goal) documentado para CLI/VS Code; verificar en Desktop. No confundir objetivos persistentes con ejecución indefinida ni con recuperación después de cerrar la app.

## Modelo operativo propuesto
Code analiza objetivo, criterios de aceptación, dependencias y riesgos; asigna tareas por capacidad y propiedad de archivos; usa background cuando las tareas son independientes y foreground cuando hay dependencias. Los hijos comparten hallazgos relevantes mediante Swarm si está disponible. Code integra, ejecuta comprobaciones transversales y entrega evidencia. No duplicar escrituras; usar worktrees separados para alternativas o cambios incompatibles. Los revisores no modifican el trabajo que certifican. Reutilizar agentes nativos en vez de duplicarlos.

Roles candidatos, no instalados: arquitectura, frontend/UX, backend, datos, plataforma, investigación, seguridad, calidad y editorial/documentación. Especialistas con herramientas de lectura, edición, shell y MCP según responsabilidad y alcance; revisión independiente de solo lectura salvo acciones de prueba controladas. Delegación anidada solo si aporta valor, con profundidad y concurrencia acotadas tras medición. Permisos altos para acciones reversibles del proyecto; aprobación explícita para operaciones sensibles, cambios globales, publicación externa o destrucción de datos. No usar allow global indiscriminado: permisos de herramientas, shell y MCP tienen alcances distintos.

## Pruebas de aceptación antes de empaquetar
1. Registrar versión Desktop, versión del motor, rutas efectivas y agente Code; inventariar configuración, plugins y MCP sin secretos.
2. Confirmar descubrimiento de un subagente Markdown de prueba sin crear un modo principal adicional; comprobar que Code lo invoca con task.
3. Dos tareas independientes simultáneas: comprobar timestamps solapados, retorno automático y que Code sigue trabajando.
4. Enviar y leer mensajes reales de Swarm entre hijos y padre; comprobar alcance y comportamiento si no existe el tablero.
5. Comprobar escritura en archivos asignados, permisos efectivos, denegación de fuera de alcance, prompts sensibles y prueba MCP inocua por rol.
6. Verificar skills bajo demanda, modelo heredado/seleccionado, continuidad tras interrupción, worktree aislado y resultado integrado.
7. Verificar plugin/goal solo si existen en runtime; registrar ausencias sin inventar sustitutos. Certificar versión concreta, no extrapolar de VS Code.
8. Diseñar instalación idempotente, respaldo, rollback y desactivación selectiva de componentes VX previos; no desinstalar MCP/skills ajenos. Probar en perfil aislado antes de tocar configuración real.

## Fuentes oficiales consultadas 2026-11-24
- https://kilo.ai/docs/desktop/overview
- https://kilo.ai/docs/desktop/release-notes
- https://kilo.ai/docs/desktop/quickstart
- https://kilo.ai/docs/desktop/settings/ai
- https://kilo.ai/docs/desktop/features/git
- https://kilo.ai/docs/customize/custom-subagents
- https://kilo.ai/docs/customize/agent-permissions
- https://kilo.ai/docs/customize/agents-md
- https://kilo.ai/docs/customize/skills
- https://kilo.ai/docs/automate/agent-manager
- https://kilo.ai/docs/getting-started/settings
- https://kilo.ai/docs/automate/extending/plugins
- https://kilo.ai/docs/code-with-ai/agents/goals
- https://github.com/Kilo-Org/kilo-desktop
- https://github.com/Kilo-Org/kilocode

No se ha accedido al runtime local del usuario ni se han instalado agentes, plugins o MCP. Esta investigación no constituye una certificación funcional.
