# VX Runtime — estado real y certificación gradual · 16-11-2026

**Propósito:** validar Kilo Code global en el único PC Windows, sin confundir archivos en disco con herramientas efectivamente invocadas. Datos reportados por el operador; ningún token, configuración íntegra o contenido privado se guarda en GitHub.

## Evidencia observada

| Puerta | Estado actual | Fuente | Limitación |
|---|---|---|---|
| Archivos VX | VERIFICADO | PowerShell V023 + doctor: 12/12 agentes, 31/31 skills, 43 hashes cotejados | No acredita descubrimiento ni permisos de Kilo |
| skill vx-engineering-harness | VERIFICADO EN SESIÓN | Respuesta Kilo que identifica llamada nativa skill | No prueba otras skills |
| skill vx-ida-mcp-reverse-engineering | VERIFICADO EN SESIÓN | Respuesta Kilo que identifica llamada nativa skill | No equivale a conexión IDA |
| Protección external_directory | BLOQUEO ESPERADO | glob hacia HOME fue denegado por Kilo | No demuestra que los agentes falten |
| Selector primario vx-integrador | NO VERIFICADO | El agente activo informó Kilo/alias Yoan | Seleccionar visualmente vx-integrador |
| Delegación vx-inspector | NO VERIFICADO | task no se invocó | Piloto read-only en README del proyecto |
| Seguridad efectiva de vx-inspector | NO VERIFICADO | ACL en Markdown, sin prueba de host | No intentar editar archivos reales |
| Builders edit/bash ask | NO VERIFICADO | Builders definidos en código, sin prueba interactiva | Piloto posterior en fixture aislado |
| IDA MCP conectado | NO VERIFICADO | Doctor detecta IDA configurado, no conectado | Test de herramienta read-only separado |

**Observaciones:** coexistencia con 19 inline; el doctor detecta 11 solapamientos de nombre entre inline y agentes Markdown legados (no IDs VX). No deshabilitar ni migrar esas definiciones sin análisis posterior. Context7, Playwright e IDA están configurados, no necesariamente conectados.

## Piloto P1 — sin riesgo

1. Abrir nueva sesión Kilo tras /reload. Operador confirma si vx-integrador aparece en selector y puede seleccionarlo; un alias de presentación no cuenta.
2. Desde vx-integrador, con autorización del operador, invocar task a vx-inspector para revisar solo la primera cabecera de README.md del proyecto actual. El inspector no debe escribir ni usar bash.
3. Contrastar los nombres de herramientas utilizadas en el transcript Kilo; si task no se ejecutó, registrar NO_VERIFICADO.
4. Cargar las dos skills por skill tool cuando corresponda; la carga es distinta de disponibilidad de MCP.
5. Para builders edit/bash ask y conexión IDA MCP, diseñar fixture aparte con autorización por acción. Mantener scheduler OFF, MCP sin cambios, una sola escritura STRICT.

## Herramientas y comprobación declarativa

- Comando global: /vx-certificar
- CLI de evidencia en repo: python -I scripts/vx_runtime_smoke_v1.py --template
- CLI para validar JSON preparado manualmente: python -I scripts/vx_runtime_smoke_v1.py --check <archivo.json>

El validador NO lee HOME ni logs de Kilo, ni certifica criptográficamente la veracidad de los reportes. Incluso ocho estados VERIFICADO recibidos del operador permanecen como EVIDENCIA_DECLARADA_REQUIERE_REVISION_HUMANA. Nunca concede permisos ni activa automatizaciones. El archivo JSON es local/privado; no subirlo al repositorio si contiene datos de sesiones.
