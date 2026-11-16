# VX Runtime — estado real y certificación gradual · 16-11-2026

**Propósito:** validar Kilo Code global en el único PC Windows, sin confundir archivos en disco con herramientas efectivamente invocadas. Datos reportados por el operador; ningún token, configuración íntegra o contenido privado se guarda en GitHub.

## Evidencia observada

| Puerta | Estado actual | Fuente | Limitación |
|---|---|---|---|
| Archivos VX | VERIFICADO | PowerShell V023 + doctor: 12/12 agentes, 31/31 skills, 43 hashes cotejados | No acredita descubrimiento ni permisos de Kilo |
| skill vx-engineering-harness | VERIFICADO EN SESIÓN | Respuesta Kilo que identifica llamada nativa skill | No prueba otras skills |
| skill vx-ida-mcp-reverse-engineering | VERIFICADO EN SESIÓN | Respuesta Kilo que identifica llamada nativa skill | No equivale a conexión IDA |
| Protección external_directory | BLOQUEO ESPERADO | glob hacia HOME fue denegado por Kilo | No demuestra que los agentes falten |
| Selector primario vx-integrador | OBSERVADO POR OPERADOR | Captura de Kilo: Vx Integrador marcado y activo, cinco builders visibles | No atestación nativa del selector ni ACL de builders |
| Delegación vx-inspector | VERIFICADO POR INFORME DE SESIÓN | Dos llamadas nativas `task` reportadas: primera `BLOCKED` por requisito de selector; segunda `completed` con revisión de README | No acredita permisos efectivos ni auditoría independiente del delegado |
| Seguridad efectiva de vx-inspector | NO VERIFICADO | ACL en Markdown, sin prueba de host | No intentar editar archivos reales |
| Builders edit/bash ask | NO VERIFICADO | Builders definidos en código, sin prueba interactiva | Piloto posterior en fixture aislado |
| IDA MCP conectado | NO VERIFICADO | Doctor detecta IDA configurado, no conectado | Test de herramienta read-only separado |

**Observaciones:** coexistencia con 19 inline; el doctor detecta 11 solapamientos de nombre entre inline y agentes Markdown legados (no IDs VX). No deshabilitar ni migrar esas definiciones sin análisis posterior. Context7, Playwright e IDA están configurados, no necesariamente conectados.

## Piloto P1 — ejecutado con una corrección de handoff

1. La captura aportada por el operador muestra Vx Integrador seleccionado y los cinco builders visibles. La identidad de presentación de la sesión no era suficiente por sí sola.
2. El primer `task(vx-inspector)` reportado acabó `BLOCKED`: el delegado exigió comprobar de nuevo el selector que no puede observar. Después de trasladar el prerequisito como **confirmación visual del operador**, el segundo `task` devolvió `completed` con una revisión declarada de solo lectura del README.
3. El título indicado por el inspector coincide con el encabezado del README actual. Sus tres observaciones: brecha entre inventario/CLI y runtime, inventarios históricos de 30 frente a 31 skills actuales, y encabezado V4.6 presentado como fase futura tras su cierre.
4. Ninguna ejecución de Bash, edición, inspección HOME ni conexión IDA MCP se reportó en la P1. La ausencia declarada de estas acciones no certifica que las ACL efectivas sean correctas.
5. P1 cumple el criterio **delegación nativa con respuesta**; la certificación global continúa parcial. No repetir la comprobación visual sin cambio de contexto ni tratarla como herramienta nativa.

## Piloto P2.1 — bloqueo de precondición; edición no certificada

El intento anterior de edición leyó la línea `Estado del piloto: SIN_VALIDAR`, pero informó ausencia de herramienta nativa. La captura posterior del laboratorio muestra **`Code` seleccionado**, no `Vx Docs Builder`, y autonomía **`Auto`**, cuyo estado efectivo de aprobación manual no se comprobó. No es válido atribuir ese `TOOL_UNAVAILABLE` al builder; estado P2 = **PRECONDITION_NOT_MET / NO_VERIFICADO**, no fallo demostrado de seguridad.

**Procedimiento P2.1, separado de producción:** abrir VX-Team-Lab y ejecutar `/vx-p2` sin fase, que declara `agent: vx-docs-builder`, para solicitar al host el agente correcto y comenzar **sin escrituras**. Confirmar visualmente que el selector muestra Vx Docs Builder y establecer **aprobación manual por acción**, sin modificar globalmente `kilo.jsonc` ni AutoApprove. Luego usar `/vx-p2 fase=denegar`: la única edición solicitada a `README.md` deberá mostrar aprobación previa y el operador denegará; comprobar `SIN_VALIDAR`. Únicamente tras superar la denegación, realizar otra llamada aprobada una sola vez, reversible. Si no aparece edición nativa con builder confirmado, registrar TOOL_UNAVAILABLE; si Kilo escribe sin aprobación previa en modo manual, registrar FAIL_UNAPPROVED_WRITE y detener. **Vx Docs Builder tiene `bash: deny`** y no se permite usar terminal/MCP como alternativa.

## Incidencia P2.2 — diagnóstico de aprobación en el host

Después de la captura que mostraba Vx Docs Builder activo y autonomía Manual, el operador reportó que el agente **no invocó herramientas**: razonó que su herramienta de edición aplicaría cambios directamente y finalizó en PRECONDITION_NOT_MET. Ese razonamiento no es evidencia del comportamiento de permisos de Kilo. En Kilo, `ask` es una decisión **del host al proponer** una llamada nativa `edit`, `write` o `apply_patch`; no existe una herramienta separada que el agente deba invocar para mostrar la ventana. Sin embargo, antes de la llamada debemos comprobar por UI que **Settings → Auto Approve → Edit** coincide con `Ask` y que el escudo de autoaprobación en runtime está desactivado; `Manual` por sí solo no demuestra el permiso `edit` efectivo. [Permisos de agentes](https://kilo.ai/docs/customize/agent-permissions) · [Auto-Approve](https://kilo.ai/docs/getting-started/settings/auto-approving-actions).

El comando `/vx-p2` ahora incluye `PERMISSION_NOT_CONFIRMED` y exige esta evidencia previa. Si se confirma, permitir **una sola llamada nativa de edición en fase=denegar**, rechazar en el Permission Dock y verificar fuera del agente que README continúe SIN_VALIDAR. Cualquier escritura sin solicitud previa supone FAIL_UNAPPROVED_WRITE y detiene las pruebas; no hay autorización de reintento, Bash ni ediciones en producción. **Estado global P2: NO VERIFICADO; no se ha observado petición ni denegación real.**

## Herramientas y comprobación declarativa

- Comandos globales: /vx-certificar y /vx-p2 (selector del Docs Builder)
- CLI de evidencia en repo: python -I scripts/vx_runtime_smoke_v1.py --template
- CLI para validar JSON preparado manualmente: python -I scripts/vx_runtime_smoke_v1.py --check <archivo.json>

El validador NO lee HOME ni logs de Kilo, ni certifica criptográficamente la veracidad de los reportes. Incluso ocho estados VERIFICADO recibidos del operador permanecen como EVIDENCIA_DECLARADA_REQUIERE_REVISION_HUMANA. Nunca concede permisos ni activa automatizaciones. El archivo JSON es local/privado; no subirlo al repositorio si contiene datos de sesiones.
