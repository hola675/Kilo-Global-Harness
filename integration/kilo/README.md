# Integración Kilo Desktop
Versión del archivo: 0.2.0 | Última modificación: 2026-11-24

## Base auditada, no certificada
Desktop 1.0.0, commit 0e86bc8c350b5ee2009bbb8d4722c955355bbe10; CLI 7.8.27, tag v7.8.27, commit 03a6f07d053cd7e6aa88fa1e258e93510335259f. Ver [auditoría](../../docs/AUDITORIA-CODIGO-KILO-DESKTOP.md). No usar kilo del PATH como prueba del binario Desktop.

## Resolución de configuración
- Global de usuario: Global.Path.config, candidato ~/.config/kilo/ según XDG; kilo.jsonc/kilo.json/opencode.jsonc/opencode.json/config.json en orden de candidato global de Desktop. Agentes en agent/agents y skills en skill/skills de directorios descubiertos.
- Perfil administrado Desktop: <storage kilo.core>/agent/runtime/config/kilo, impuesto vía KILO_CONFIG_DIR; sidecar de propiedad y estado XDG_STATE_HOME separado salvo override. No editar perfil/sidecar ni tokens.
- Instrucciones globales: primer existente entre perfil/AGENTS.md, global.config/AGENTS.md y Claude global condicional. Proyecto: primer tipo coincidente AGENTS.md, CLAUDE.md, CONTEXT.md; instructions agrega fuentes. Probar marcador benigno y detectar shadowing; no afirmar que todas se acumulan.
- Config proyecto: kilo/opencode JSON/JSONC, .kilo/.kilocode y fallbacks del checkout principal; merge por campo, no regla simplista de precedencia. Skills también en .agents/.claude según flags y migración, rutas extras y builtins. Inventariar duplicados, no copiar automáticamente.
- F02 observa rutas reales; F03 prueba en fixture; F04 instala política candidata solo tras aprobación y ruta certificada. No escribir aún ni cambiar selección de modelo.

## Matriz
Registrar por capacidad: fuente/commit, versión instalada, estado de exposición, invocación, resultado, evidencia y fallback. Estados separados: SOURCE_CONFIRMED, DOCUMENTED, EXPOSED, INVOKED, VERIFIED, FAIL, BLOCKED, NOT_RUN, UNSUPPORTED (solo con evidencia de ausencia).
Code/general/explore, Task foreground/background (flag por defecto true), task_id (hijo propio), subagent_depth (default 1), board (default true, opt-out), skill, shell/edit/read, LSP, MCP nativo/desktop_*/externo, plugins motor/Desktop, compactación, goals, worktrees, permisos y sandbox. Defaults son de CLI auditado, verificar en runtime.
Integración por configuración mínima y merge selectivo de archivos del usuario autorizados; evitar reemplazo completo de JSONC y proteger ownership Desktop. No copiar auth.json. Settings/Marketplace nativos antes de integraciones propias; reinicio solo autorizado cuando necesario.
