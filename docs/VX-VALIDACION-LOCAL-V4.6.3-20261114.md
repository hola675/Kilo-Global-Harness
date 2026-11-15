# VX Evolution V4.6.3 — Validación del CLI Windows y puerta de auditoría manual

**Fuente:** salida de PowerShell 7.6.8 proporcionada por el operador, ejecución local del 2026-11-14 según el registro de instalación · **Ámbito:** Kilo Code global, un solo equipo Windows · **Clasificación:** evidencia de instalación, integridad de archivos y diagnóstico estático. **No es una evaluación del runtime ni de competencias.**

## Cierre técnico verificado por el operador

La terminal del usuario actualizó `main` mediante fast-forward desde `c85b711` hasta `8e9b993`, ejecutó el instalador en modos `Simular`, `Aplicar` y `Verificar`, y obtuvo `VX V4.6.3: CLI LOCAL OK` ejecutando `vx_organizational_audit.py` con Python aislado. El instalador comprobó los archivos administrados globales; se observaron `vx-organizacion.md` y `vx_organizational_audit.py` instalados y verificados con `[OK]`.

El operador eliminó correctamente la rama remota temporal `work/v4-6-3-auditoria-organizacion` y terminó con `origin/HEAD -> origin/main` y `origin/main`. No hace falta reinstalar V4.6.3 para registrar este cierre.

| Métrica observada en el equipo real | Resultado |
| --- | ---: |
| Agentes declarados en JSONC | 21 |
| Agentes con el mismo nombre en JSONC y Markdown | **11** |
| Solapamientos con diferencias detectadas en campos explícitos comparados | **0** |
| Definiciones `steps > 400` | **19** |
| Skills repetidas por nombre entre rutas globales | **0** |
| Skills de perfil no observadas | **0** |
| Agentes del router no observados | **0** |
| Hallazgos para revisión manual | **30** |
| Estado del informe CLI | **PASS** |
| Procedencia de delegación de Kilo | `NO_VERIFICADO` |
| Rendimiento/competencia de especialistas | `NO_MEDIDO` |

Los **30 hallazgos** son las 11 coincidencias de nombre de agentes y las 19 declaraciones de `steps` sobre el umbral. No representan 30 errores ni 30 personas/agentes únicos afectados. La ausencia de diferencias explícitas solo cubre `mode`, `steps` y permisos simples comparables presentes en ambas fuentes: **no compara prompts completos, herramientas complejas, comportamiento o prioridad de carga**. No fusionar ni retirar agentes por esta salida.

La simulación también contabilizó **6 declaraciones de agentes JSONC** con `edit` o `bash` en `allow`, lo cual es una **pista de revisión de configuración**, no prueba de permisos usados por el runtime ni vulnerabilidad demostrada. No autoriza endurecer ni modificar permisos automáticamente.

## Conservación de configuración y límites de la prueba

La instalación indicó `task-observer activa: False`, `VX Observer instalado: True` y `AutoApprove` presente, **sin modificación del ajuste**. Que el plugin VX Observer esté instalado no verifica su modo de captura operativo; mantener separado de `task-observer`. Se informó que los MCP son configuraciones declaradas, no conexiones verificadas. Esta acta deliberadamente no publica nombres de MCP del usuario, rutas privadas, identificadores de sesión, nombre de respaldo, prompts, tokens ni logs de Kilo.

El instalador anunció conservación de la configuración JSONC, permisos, modelos, MCP y AutoApprove; su fase Verificar informó `VERIFICACION DE ARCHIVOS: OK`. El auditor V4.6.3 fue diseñado para no abrir SQLite, emitir propuestas ni ejecutar agentes; **la salida no constituye una auditoría forense de todas las escrituras del sistema**. El scheduler y las notificaciones permanecen sin autorización para activarse.

La restricción anterior de PowerShell **desde Kilo** sigue siendo una política legítima; la ejecución directa y autorizada desde PowerShell del operador no demuestra que la herramienta pueda invocarse dentro de la extensión. Aún falta comprobar la ejecución interactiva de `/vx-organizacion` si la política lo permite, sin ampliar AutoApprove ni accesos.

## Puerta de revisión manual V4.6.3

1. **Procedencia y delegación:** inspeccionar desde la interfaz de Kilo (sin exportar logs completos) el perfil/modo de ejecución de `vx-inspector` y `vx-test-analyst` para las tareas V4.6.2, si la UI expone trazas verificables. Una respuesta del coordinador o un ID de sesión no autentica al subagente.
2. **Solapamientos (11):** revisar solo metadatos seguros y determinar si hay efecto observable en Kilo. Con `0` diferencias explícitas detectadas, priorizar comprobación de procedencia antes que propuestas de fusión. No contrastar/volcar prompts completos por defecto.
3. **Steps elevados (19 entradas):** justificar, por agente, por qué se usa el valor; sin medir latencia, costes y resultados no se puede recomendar reducirlo.
4. **Permisos simples (6 declaraciones):** verificar uso efectivo/ámbito, sin conceder ni revocar permisos como parte de esta auditoría.
5. **Calidad y capacitación:** los cinco casos conversacionales V4.6.2 coincidieron con fixtures públicos, no ciegos; todavía faltan casos independientes, revisiones separadas y métricas reales antes de cualquier evaluación de competencia.

**Decisión de cierre:** V4.6.3 código integrado y CI Windows PASS, instalación y CLI del equipo real PASS. La auditoría **estática** está cerrada; la verificación de procedencia y el estudio manual de hallazgos continúan pendientes. V4.7 es diseño posterior, **sin autorización de publicación**, cambios de jerarquía, permisos, nuevos agentes, skill, MCP, SQLite, tareas ni scheduler.

Referencia: [Guía V4.6.3](VX-AUDITORIA-ORGANIZATIVA-V4.6.3.md), [Roadmap maestro](VX-EVOLUTION-ROADMAP.md).
