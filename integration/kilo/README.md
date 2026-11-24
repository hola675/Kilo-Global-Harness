# Integración Kilo Desktop
Versión del archivo: 0.3.0 | Última modificación: 2026-11-24

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

## Control de modelo uniforme
Requisito del operador: un único modelo autorizado para Code y especialistas; objetivo de laboratorio openai/gpt-6-luna, pendiente de confirmación BYOK y coste. No sustituir por free/auto, otro proveedor ni modelo de pago por iniciativa del agente. Si catálogo, cuota o configuración impiden usarlo, informar y detener delegación afectada. Política no equivale a enforcement del motor. Fuente fijada: https://github.com/Kilo-Org/kilocode/blob/03a6f07d053cd7e6aa88fa1e258e93510335259f/packages/opencode/src/kilocode/tool/task.ts#L282-L412 . Para tarea nueva sin override explícito: workflow > selección guardada (solo KILO_CLIENT=cli) > modelo del agente > subagent_model disponible > padre. Reanudación puede usar modelo de sesión previa; overrides explícitos se resuelven por separado. No inferir origen de kilo-auto/free por este orden. Probar primero model: openai/gpt-6-luna en definición de un lector de laboratorio, nuevo chat Code con mismo modelo y nueva task sin override; no reusar task_id. Verificar identidad efectiva del hijo y del líder, y proveedor/coste en panel, sin copiar credenciales. Si falla, revisar configuración efectiva y workflow; probar subagent_model y overrides autorizados por separado. Centralización en F04/F05 tras evidencia; no editar perfil administrado de Desktop.
