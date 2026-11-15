# VX Evolution V4.6.3 — Hallazgos sobre steps y precedencia (revisión manual)

**Registro:** 2026-11-14 · **Ámbito:** únicamente HOME global del usuario Windows, Kilo Code · **Fuente local:** tablas resumidas aportadas por el operador desde `vx_organizational_audit.py --json`. **No se inspeccionaron prompts, credenciales, contenido de Kilo JSONC ni logs.** Código de agentes y configuración activos sin cambios.

## Hechos observados

- Git local actualizado en `main` al commit documental `5bc46174e68323438e26bb092c5eee600ef3e531`, rama remota `work/v4-6-3-cierre-local-auditoria` eliminada, `origin/main` restante.
- Las once coincidencias de nombre entre JSONC y Markdown son: `architect`, `code-reviewer`, `code-simplifier`, `code-skeptic`, `codebase-memory`, `codebase-memory-auditor`, `codebase-memory-scout`, `data`, `docs-specialist`, `frontend-specialist` y `test-engineer`.
- Para las once coincidencias, `different_declared_fields=[]` y `effective_precedence=NO_VERIFICADO`. El comparador revisa **solo metadatos explícitos compartidos**: `mode`, `steps` y reglas sencillas `permission.edit/bash/task` cuando existen en ambas. Ausencia de diferencias **no** implica mismo prompt, mismos permisos efectivos, ni carga confirmada del runtime.
- En la **consulta completa de las 19 entradas** `AGENT_STEPS_REVIEW`, todas mostraron `configured_steps = 10 000 000` y fuente `kilo-agent-jsonc`. Se ejecutó desde el CLI de solo lectura del usuario; no se modificó `kilo.jsonc`:

| Definición de agente | Fuente | steps declarados |
| --- | --- | ---: |
| architect | kilo-agent-jsonc | 10 000 000 |
| plan | kilo-agent-jsonc | 10 000 000 |
| implementador-vecidya | kilo-agent-jsonc | 10 000 000 |
| general | kilo-agent-jsonc | 10 000 000 |
| frontend-specialist | kilo-agent-jsonc | 10 000 000 |
| explore | kilo-agent-jsonc | 10 000 000 |
| docs-specialist | kilo-agent-jsonc | 10 000 000 |
| debug | kilo-agent-jsonc | 10 000 000 |
| qa-vecidya | kilo-agent-jsonc | 10 000 000 |
| data | kilo-agent-jsonc | 10 000 000 |
| codebase-memory-auditor | kilo-agent-jsonc | 10 000 000 |
| codebase-memory | kilo-agent-jsonc | 10 000 000 |
| code-skeptic | kilo-agent-jsonc | 10 000 000 |
| code-simplifier | kilo-agent-jsonc | 10 000 000 |
| code-reviewer | kilo-agent-jsonc | 10 000 000 |
| code | kilo-agent-jsonc | 10 000 000 |
| ask | kilo-agent-jsonc | 10 000 000 |
| codebase-memory-scout | kilo-agent-jsonc | 10 000 000 |
| test-engineer | kilo-agent-jsonc | 10 000 000 |

**Distribución confirmada:** 19 definiciones de 19 (100 %) con `steps = 10 000 000`; no hay otro valor entre las entradas superiores al umbral 400. La auditoría no afirma el número de agentes únicos que usaron este valor en sesiones reales ni las rondas efectivamente ejecutadas.

## Interpretación basada en documentación de Kilo

La referencia oficial [Kilo Code: Custom Modes](https://kilo.ai/docs/customize/custom-modes) describe `steps` como el **máximo de iteraciones del agente** (rondas de llamadas a herramientas) antes de obligar a una respuesta de texto. Como límite de seguridad operativo, diez millones de iteraciones es extraordinariamente permisivo; ello **no demuestra** que alguna sesión alcanzase el límite ni que exista consumo excesivo.

La misma documentación describe la **fusión de propiedades** de configuraciones, con precedencia documentada entre configuración global JSONC, configuración de proyecto, archivos de directorio Markdown y variables de entorno. Esta es una **regla documentada** y no una comprobación del **Kilo instalado ni del contexto específico de una sesión**. No declarar prioridad efectiva de un agente o subagente sin observar el runtime.

### Puntos de revisión humana (sin cambios)

1. **Listado de 19 entradas completado.** Clasificar funciones reales de los agentes (planificación, lectura, implementación, revisión, memoria y pruebas) solo después de comprobar su modo/ruta; un nombre es una pista, no una garantía de responsabilidad.
2. Confirmar en la interfaz de Kilo qué modo y fuente se usa de verdad para uno o dos agentes representativos; evitar mezclar configuraciones del proyecto abierto con el HOME global.
3. Proponer, **no aplicar**, límites finitos de iteraciones adaptados a cada tipo de trabajo, acompañados de casos de control, medición de tasa de terminación y recuperación cuando se alcanza el límite. Ninguna cifra nueva se aprueba por silencio.
4. Confirmar que los seis agentes que el instalador señaló con `edit` o `bash` en `allow` son **declaraciones** y no permisos operativos ni acciones ejecutadas. Revisarlos separadamente y sin copiar credenciales.
5. Mantener `competence=NO_MEDIDO`, procedencia de delegaciones `NO_VERIFICADO`, y las reuniones automáticas y scheduler **OFF**.

## Próxima fase: diseño de límites medibles (sin aplicación)

Con el inventario **completo**, el siguiente paso no es repetir el CLI ni reducir todos los límites al mismo valor:

1. **Comprobar configuración efectiva:** elegir dos agentes representativos y confirmar en Kilo qué fuente se aplica para `steps`. La precedencia documentada no constituye una prueba de ejecución en este Windows.
2. **Línea base por tipo de tarea:** para tareas reales y casos sintéticos nuevos, documentar manualmente, si la interfaz lo permite y el operador lo autoriza, rondas efectivas de herramientas, finalización, interrupción por límite, necesidad de reintento y calidad externa. Sin guardar prompts ni datos de clientes.
3. **Propuesta reversible:** agrupar agentes según finalidad demostrada y plantear valores candidatos conservadores, distintos según tipo de tarea. Las cifras se fijarán **después** de obtener una línea base, nunca por el nombre del agente ni por observación de un único caso.
4. **Pruebas de regresión:** verificar una tarea corta, una extensa legítima y una que deba detenerse; revisar que el límite no provoque truncamiento inseguro, ni obligue a responder sin terminar una operación importante.
5. **Puerta de aprobación:** el operador revisará el diff exacto, el procedimiento de restauración y la evidencia de beneficios; la autorización para diagnosticar **no** autoriza editar `kilo.jsonc` ni publicar un cambio.

**Estados:** `limite_declarado=VERIFICADO_EN_INVENTARIO_LOCAL`, `limite_efectivo_runtime=NO_VERIFICADO`, `rondas_consumidas=NO_MEDIDO`, `calidad=NO_MEDIDO`, `modificacion_autorizada=false`.

Esta observación es un hito de investigación de V4.6.3 y **no** crea una versión nueva, cambios de permisos, agentes, skill, modelos, MCP, SQLite o programador.
