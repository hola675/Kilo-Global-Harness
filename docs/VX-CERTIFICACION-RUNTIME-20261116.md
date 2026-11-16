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

## Piloto P2 — propuesto, no ejecutado

Crear un proyecto de prueba aislado y **fuera del repositorio del Harness** (abierto como workspace autorizado), con un archivo inofensivo y conocido, por ejemplo `ACL_TEST.txt`. Seleccionar visualmente `Vx Backend Builder` o `Vx Docs Builder`; verificar `edit: ask` primero denegando un cambio solicitado y comprobando que no se escribió nada. Para la prueba de aprobación, volver a solicitar una **edición mínima y reversible** y aprobarla explícitamente si la UI presenta la autorización; registrar mensaje de permiso, herramienta invocada y hash antes/después. No ejecutar Bash ni MCP y no conectar el sandbox a producción. Si se edita sin requerir aprobación, registrar FAIL de la política esperada y detener las pruebas. No ejecutar P2 automáticamente por esta documentación: requiere nueva autorización del operador en Kilo.

## Herramientas y comprobación declarativa

- Comando global: /vx-certificar
- CLI de evidencia en repo: python -I scripts/vx_runtime_smoke_v1.py --template
- CLI para validar JSON preparado manualmente: python -I scripts/vx_runtime_smoke_v1.py --check <archivo.json>

El validador NO lee HOME ni logs de Kilo, ni certifica criptográficamente la veracidad de los reportes. Incluso ocho estados VERIFICADO recibidos del operador permanecen como EVIDENCIA_DECLARADA_REQUIERE_REVISION_HUMANA. Nunca concede permisos ni activa automatizaciones. El archivo JSON es local/privado; no subirlo al repositorio si contiene datos de sesiones.
