# Auditoría de referencia · VECIDYA Kilo Global Harness V3.0

**Fuente principal:** `Kilo-Code-Auditoria-20261113-124536.zip` proporcionado por el usuario el 2026-11-13. Es una copia sanitizada, NO un backup recuperable. El análisis ocurrió fuera del PC Windows. No se publican secretos ni originales privados.

## Hallazgos observados

- Configuración global encontrada: `01-Kilo-Config/kilo.jsonc`. JSON parseable; contiene **21 definiciones de agentes**.
- **19 definiciones** conservan `steps=10000000`. `steps` limita iteraciones, no tokens.
- **11 archivos Markdown** en directorio global de agentes con nombres que también están en el objeto `agent` del JSON; la precedencia real debe probarse en Kilo.
- MCP configurados en esta copia: `cloudflare`, `memory`, `codebase-memory-mcp`, `microsoft-learn`, `imagegen` (**cinco**). No se puede concluir si están conectados.
- La configuración proporcionada no declara explícitamente un modelo principal. Esto no prueba que Kilo carezca de modelo operativo.
- Skills incluidas en la copia: **22** en `~/.kilo/skills`, **9** en `~/.agents/skills` y **7** en `~/.kilocode/skills`. Hay instrucciones específicas de herramientas y algunas requieren dependencias adicionales.
- `task-observer` 3.10.0 usa un disparador muy amplio (antes de casi cualquier herramienta) y documentación extensa; recomienda pausarla conservando un backup si se prioriza reducir contexto.
- `AGENTS.md` global ya existía con reglas útiles, pero una regla antigua prohibía push/merge sin aprobación explícita; las preferencias actuales solicitan autonomía Git ordinaria en tareas autorizadas. V3 añade una sección posterior marcada para definir la excepción con límites claros.
- Los JSON de auditoría pueden contener sustituciones `[REDACTADO]` que no son válidas como permisos. Por eso NO se usan como fuente para modificar el runtime.

## Diferencias importantes respecto al repositorio anterior

- `main` contenía V2.0 (regla que forzaba cambiar permisos y apagar AutoApprove). Esta versión V3 no cambia los permisos ni AutoApprove.
- El usuario exige **cero skills, agentes o MCP por proyecto**. Todos los assets del harness se instalan en HOME; el repositorio mantiene únicamente la versión fuente.
- El instalador V3 no modifica `kilo.jsonc`, por tanto no destruye comentarios JSONC ni tokens y puede convivir con cambios de UI posteriores.
- Validación real de conexiones MCP, selección de modelos, indexación de repositorios y carga de subagentes sigue pendiente de ejecutar en Windows.

## Riesgos abiertos y tratamiento

| Hallazgo | Gravedad | Tratamiento V3 |
| --- | --- | --- |
| Límites steps de 10 millones | Alta (consumo/bucles) | Solo diagnóstico. Planificar reducción tras prueba de versiones y límites. |
| AutoApprove y permisos muy amplios | Alta | Mantener elección del usuario; reglas globales prohíben acciones destructivas o no autorizadas. Permisos reales siguen gobernados por Kilo. |
| Duplicados JSON/Markdown | Media | No sobrescribir, identificar y reconciliar en fase posterior con pruebas. |
| Skill task-observer demasiado activa | Media | `-PausarTaskObserver` la mueve a backup privado, reversible. |
| Configuración MCP sin garantía de conexión | Media | `/vx-mcp`, pruebas concretas en runtime. |
| Secretos potencialmente expuestos | Alta | No publicar el ZIP, credenciales ni archivos de backup; rotar claves reveladas previamente. |
| Contenido local de `D:\Proyectos` no accesible aquí | Informativa | Modificaciones se publican al remoto GitHub; sincronizar local mediante fast-forward. |

## Criterios de aceptación

1. `-Modo Diagnostico` y `-Modo Simular`: cero mutaciones.
2. `-Modo Aplicar`: solamente rutas globales bajo HOME; intactos `kilo.jsonc`, configuración VS Code y archivos de proyectos.
3. Aplicación repetida sin archivos duplicados ni cambio de contenido no gestionado.
4. `-Modo Verificar`: hashes de assets coinciden y sección AGENTS está presente.
5. `-Modo Restaurar`: restaura solo archivos respaldados y no sobrescribe cambios posteriores salvo autorización explícita.
6. CI valida sintaxis PowerShell y realiza un smoke test aislado. No equiparar CI con prueba real de MCP.
7. Flujo Git usa rama temporal, CI/PR/merge y única rama permanente main cuando se pueda verificar y eliminar con seguridad.


## Adenda V3.1 — Pruebas funcionales del operador (13-11-2026)

- V3 aplicada y verificada: 14 comandos, 2 agentes, skill de orquestacion y reglas globales detectados. La prueba de ejecución efectiva de subagentes sigue pendiente.
- Hay 12 nombres de agente presentes en JSON y Markdown. La documentación oficial indica fusión por precedencia de propiedades; por ello hay **doble mantenimiento**, pero no se demuestra fallo de ejecución. Se prohíbe eliminar de forma automática los duplicados hasta comparar permisos y comportamiento efectivo.
- Se reportaron 19 valores `steps: 10000000`; son límites de iteraciones, no de tokens. Auditoría en solo lectura y normalización posterior bajo control de cambios.
- La presencia de `opencode-models-discovery` en `opencode.json` y `tui.json` puede estar prevista por la instalación de un plugin en dos superficies distintas; no retirar sin confirmar doble carga.
- ImageGen: tres generaciones mediante CLI `codex-imagegen-mcp@0.2.3` verificadas por el operador. No se ha verificado que la sesión de Kilo exponga el mismo conjunto de herramientas. El comando `/vx-imagegen` solo inspecciona y no genera imagenes.
- Se conserva AutoApprove, permisos, proveedores, modelos, MCP y `kilo.jsonc` sin modificación por defecto.

Documentación oficial: https://kilo.ai/docs/customize/custom-modes ; https://kilo.ai/docs/customize/marketplace ; https://kilo.ai/docs/automate/mcp/using-in-kilo-code .
