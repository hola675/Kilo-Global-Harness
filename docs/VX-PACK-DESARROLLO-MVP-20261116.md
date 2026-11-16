# Pack VX de desarrollo — primera implementación funcional (V0.1.0)

**Fecha:** 2026-11-16 · **Estado:** rama independiente de implementación, no instalada en el Kilo real. **Ámbito:** Kilo Code global en PC Windows, agente nativo Kilo preservado, MCP existentes conservados. Se mantiene `main` como única rama permanente, scheduler OFF y autorizaciones explícitas.

## Qué incluye en código (no solo concepto)

El equipo base pasa de **7 agentes VX originales** a **12**, preservando los siete IDs/alias ya confirmados. Los cinco nuevos implementadores, aún sin alias humanos, cubren: `vx-frontend-builder`, `vx-backend-builder`, `vx-qa-builder`, `vx-data-builder` y `vx-docs-builder`. Los originales se refuerzan con protocolos de coordinación y revisión. Los implementadores se pueden seleccionar directamente en el picker de Kilo (`mode: all`); `edit: ask`, `bash: ask` o `deny` según función, `mcp/task/agent_manager: deny`. **Si `task` no permite aprobar interactivamente, devuelve plan, no elude el permiso**. La rama requiere validación efectiva con la versión de Kilo del operador.

**Skills VX propias:** 10, con frontmatter del formato Agent Skills y descripciones de carga bajo demanda: `vx-engineering-harness` y `vx-evolution-core` originales; nuevas `vx-implementation-handoff`, `vx-test-regression`, `vx-debugging-root-cause`, `vx-frontend-quality`, `vx-security-review`, `vx-data-contracts`, `vx-docs-traceability` y `vx-self-improvement`. Son guías de ejecución completas y de mínimo contexto, **no ejecución de scripts**, no permisos ni evidencia de experiencia. La última crea propuestas de mejora, nunca las aplica por sí sola.

**Router operativo:** `scripts/Seleccionar-Equipo-V4.ps1` continúa eligiendo `code` nativo por defecto y proponiendo builders por perfil. Solo con `-UsarBuildersVX` devuelve uno de los implementadores; incluso así **solo planifica**, no arranca sesiones ni modifica archivos. Perfiles `frontend`, `backend`, `qa`, `database`, `docs` y otros. El validador comprueba permisos mínimos, IDs y skills. La operación STRICT sigue siendo un escritor por worktree; el modo multiworktree se desarrollará después con aprobación específica.

## Instalador y sustitución del perfil

El instalador V4 `scripts/Instalar-Kilo-Global-Harness.ps1` se amplió para reconocer **las diez skills VX propias** a partir de un catálogo cerrado. Es un modo de instalación incremental tradicional con sus propios respaldos por archivo; **NO es** el nuevo sistema de sustitución completa.

Se añadió `scripts/vx_pack_bootstrap.py`, un **bootstrap independiente Windows**, con estas operaciones:

- `diagnose` / `simulate`: inventario de candidatos, 12 agentes y 10 skills, MCP configurados solo por nombre, faltantes por catálogo, sin usar modelos ni modificar HOME.
- `apply` explícito (`--home` absoluto y `--confirm-migration`): exige preflight limpio, prepara snapshot en memoria ZIP cifrada mediante **Windows DPAPI CurrentUser** (no genera ZIP de credenciales en claro), verifica hashes, reemplaza solamente agentes Markdown y skills del perfil global, instala agentes/skills/rules/commands/scripts VX, verifica hashes y no modifica `kilo.jsonc`.
- `verify`: compara hashes de assets, inventario de agentes/skills y regla global; **no** demuestra que Kilo los invocó realmente.
- `restore` explícito: copia previa cifrada, cotejo de hashes contra estado instalado, protección contra sobrescribir cambios posteriores salvo autorización diferenciada. La restauración solo funciona bajo el **mismo usuario DPAPI/entorno compatible**; no sirve para transportar automáticamente sesiones/cuentas a otra PC.

**Limitaciones actuales deliberadas de migración limpia:**
1. Si `kilo.jsonc` declara agentes custom inline, se **bloquea** antes de tocar el perfil: no se reescribe un JSONC con secretos/comentarios mediante serialización destructiva. La siguiente iteración necesita parser/lógica de migración que preserve texto, pruebas y rollback.
2. Si existen skills en `~/.agents/skills` o `~/.kilocode/skills`, se **bloquea la limpieza**: son directorios compatibles potencialmente usados por otros programas. No se borran ni desactivan por sorpresa. Debe estudiarse perfil aislado o configuración de descubrimiento verificada.
3. MCP existentes se preservan, sus claves no se imprimen y no se determina conexión real solo por figurar en el JSONC. El catálogo `registry/vx-pack-mcp-catalog-v1.json` tiene **cuatro integraciones opcionales** (GitHub, Context7, Playwright, Cloudflare), sin comandos de instalación ni configuración/credenciales. Cada nueva conexión requerirá aprobación individual.
4. No hay validación de la instalación real del operador ni de la carga de skills y permisos en su Kilo Desktop; la CI utiliza HOME temporal.
5. El snapshot cubre configuración, agentes, skills y datos VX bajo las rutas especificadas; si hubiera una BD SQLite en uso con WAL activo, la coherencia transaccional debe verificarse antes de confiar en una restauración operativa. El bootstrap no migra ni modifica bases SQLite.
6. Para recuperar exactamente estados anteriores del perfil y no perder cambios posteriores, toda operación de rollback requiere revisión. El snapshot DPAPI no sustituye un procedimiento de recuperación de credenciales/identidad para otra máquina.

**No ejecutar `apply` contra HOME real todavía**: primero CI, revisión independiente de las rutas y opciones de backup, luego autorización específica del operador con lista exacta de cambios. La decisión de diseño previo sobre backup y migración no es permiso ilimitado para modificar la PC.

## Verificación prevista

- Registro de **12 agentes y 10 skills VX**; `Validar-Registro-V4.ps1` debe comprobar IDs, fuentes, permisos `ask/deny`.
- Selector: por defecto `code`; opt-in por perfil solo en función de tarea, sin acciones.
- Unit tests Python en HOME temporal; lectura de JSONC con comentarios/trailing commas; rechazo de agentes inline y skills de compatibilidad.
- **CI Windows real** (entorno de GitHub): respaldos DPAPI, cifrado, integridad, instalación, verificación, rollback y bloqueo de restauración cuando hubo ediciones posteriores.
- Diferenciar PASS de CI del descubrimiento real de agentes en Kilo.

## Referencias contrastadas, sin copiar código de terceros

- [Kilo: Custom Modes](https://kilo.ai/docs/customize/custom-modes), [Permissions](https://kilo.ai/docs/customize/agent-permissions), [Skills](https://kilo.ai/docs/customize/skills), [Agent Manager](https://kilo.ai/docs/automate/agent-manager) y [MCP](https://kilo.ai/docs/automate/mcp/using-in-kilo-code).
- [Agent Skills — especificación](https://github.com/agentskills/agentskills) y [Anthropic Skills — estructura/ejemplos](https://github.com/anthropics/skills); se usa el formato abierto, no se copia contenido.
- [obra/superpowers](https://github.com/obra/superpowers) como inspiración de pruebas, depuración y verificación antes de declarar éxito; las instrucciones VX son originales.
- [GitHub MCP](https://github.com/github/github-mcp-server), [Context7](https://github.com/upstash/context7), [Playwright MCP](https://github.com/microsoft/playwright-mcp) y [Cloudflare MCP](https://github.com/cloudflare/mcp), solo como referencias de catálogo. **No instalados.**

## Roadmap siguiente

**Pack 0.1:** cerrar CI Windows, reparar bugs, revisar seguridad/rollback, PR independiente. **Pack 0.2:** migración segura de agentes inline JSONC y tratamiento de rutas compatibles sin borrar recursos de otras aplicaciones. **Pack 0.3:** pruebas de permisos y delegación en Kilo real, descubrimiento de skills, comunicación y contratos de tarea. **Pack 0.4:** Agent Manager con worktrees paralelos, handoffs y DAG de dependencias, solo si autoriza el operador. **VX Academy V4.8+:** evaluar capacidades de cada agente y rendimiento de nuevas skills; propuesta de actualización versionada y aprobación humana, nunca autopublicación.
