# Equipo nativo — diseño de roles
Versión del archivo: 0.12.0 | Última modificación: 2026-11-24

Nueve definiciones candidatas implementadas; no instalables globalmente ni certificadas en runtime. Identificadores team-* derivados de nombre de archivo, mode: subagent, description y permission en frontmatter, cuerpo como prompt. Definiciones neutrales respecto al modelo; selección central por el operador, común por defecto. No depender solo del fallback al padre. Admitir modelos gratuitos/de pago/suscripción autorizados; no fijar el modelo provisional en roles distribuidos. Code, general y explore nativos no se duplican.

| Rol | Responsabilidad | Capacidades candidatas |
|---|---|---|
| team-architect | requisitos técnicos, contratos, arquitectura, decisiones | lectura, escritura de diseños asignados, investigación, pruebas de concepto |
| team-frontend | UI/UX, accesibilidad, web y diseño de interacción | lectura, edición, shell, navegador y MCP de diseño autorizados |
| team-backend | APIs, dominio, integraciones | lectura, edición, shell, pruebas, MCP pertinentes |
| team-data | esquemas, consultas, migraciones, sincronización | lectura, edición, pruebas con datos ficticios; no producción automática |
| team-platform | Windows, Linux, CI/CD, DevOps, desktop si aplica | edición, shell y diagnósticos; despliegue/infra sensible con permiso |
| team-research | investigación técnica, fuentes y comparación | lectura, web/docs; sin escritura de código ajeno |
| team-quality | pruebas, regresiones, revisión funcional | lectura y ejecución de pruebas; fixture separado; no editar el objeto certificado |
| team-security | amenazas, dependencias, permisos y seguridad | lectura y pruebas controladas; no cambios destructivos |
| team-editorial | documentación, UX writing, textos claros y precisos | edición de documentación y contenido asignado, revisión de lenguaje |

## Permisos
Matriz de intención, no configuración efectiva: constructores pueden leer/escribir/ejecutar dentro de asignación; investigadores leen y reportan; revisores ejecutan comprobaciones seguras y no mutan entregable revisado. MCP por necesidad y capacidad; skills accesibles según permisos nativos. Profundidad nativa inicial 1; delegación anidada opt-in solo con caso probado, lista autorizada y profundidad/concurrencia medida. No heredar globalmente los permisos de Code; comprobar guardas de sesión padre, agente propio y Desktop. Code coordina. No asumir que prompt impide escrituras; verificar enforcement nativo y límites de shell/MCP. El snapshot Desktop deshabilita sandbox de agente: checkout separado reduce colisiones, no confina filesystem. Restringir herramientas o usar aislamiento técnico verificable si requerido. Probar permisos positivos y negativos con cada rol.
## Alta de rol
Crear solo cuando no cubre un rol existente, demostrar beneficio, definir descripción discriminante, responsabilidades, entradas/salidas, herramientas, permisos, ejemplos de routing, eval y versionado.

## Evidencia de laboratorio y consecuencia de diseño
F03.4A reportó read operativo y herramientas edit/write/apply_patch/bash/task ausentes en lector; hash del fixture inalterado confirmado por operador. Ausencia de herramienta no es rechazo de llamada, ni demuestra confinamiento. No extrapolar esta matriz a constructores: F03.4B prueba edit y bash positivos con agente separado. En roles de desarrollo buscar capacidad efectiva de editar y ejecutar pruebas; en roles de revisión/investigación evitar mutación no necesaria. No usar permisos de un rol lector como plantilla indiscriminada del equipo. El glob de rutas ocultas tuvo resultados vacíos en esta muestra; usar read de directorio conocido como alternativa de lectura autorizada, sin concluir defecto general.

F03.4B reportó seis herramientas del constructor operativas; F03.4D reportó selección explícita correcta del lector. Evidencia y limitaciones en [laboratorio](../../tests/F03-LABORATORIO.md). Mantener contratos de trabajo y verificación independientes del modelo; adaptar alcance a capacidades observadas, sin reducir aceptación. Política vigente en [plan maestro](../../docs/PLAN-MAESTRO.md).

## Implementación F05.1–F05.2
F05.1–F05.2: nueve archivos Markdown candidatos team/agents/team-*.md, versión individual 0.1.0, frontmatter description/mode/permission y cuerpo de prompt, sin modelo fijado. Fuente CLI 7.8.27 fijada: packages/opencode/src/config/agent.ts carga agent/agents/**/*.md y extrae nombre de ruta y prompt del cuerpo; config/markdown.ts parsea frontmatter; agent/agent.ts combina permisos de rol, sesión y configuración; subagent-permissions.ts hereda denies/external_directory de sesión y task/todowrite según reglas. No confundir fuente estática con exposición o enforcement real. Baseline candidata default deny de herramientas no listadas; read/glob/grep/skill, board y todo allow; task y external_directory deny; edición allow para frontend/backend/data/platform/editorial, ask para architect, deny para research/quality/security; bash ask para architect/frontend/backend/data/platform/quality/security, deny para research/editorial; webfetch/websearch ask para architect/research/security y deny demás. Shell ask no garantiza inmutabilidad, edición allow no confina a rutas contractuales y permiso externo puede depender del techo de sesión; usar laboratorio descartable y autorización. MCP no listado queda denegado por default; acceso por tool exacta/perfil se evalúa F09. Code/general/explore nativos intactos. Pruebas estáticas de estructura y matriz, runtime NOT_RUN. F05 continúa IN_PROGRESS; F06 no depende de instalar equipo, pero activación definitiva bloqueada.

| Definición | Edit | Bash | Webfetch/websearch |
|---|---|---|---|
| [team-architect](team-architect.md) | ask | ask | ask |
| [team-frontend](team-frontend.md) | allow | ask | deny |
| [team-backend](team-backend.md) | allow | ask | deny |
| [team-data](team-data.md) | allow | ask | deny |
| [team-platform](team-platform.md) | allow | ask | deny |
| [team-research](team-research.md) | deny | deny | ask |
| [team-quality](team-quality.md) | deny | ask | deny |
| [team-security](team-security.md) | deny | ask | ask |
| [team-editorial](team-editorial.md) | allow | deny | deny |

La matriz común permite board_read/board_post y todowrite como candidatos, no demuestra exposición. Las reglas del rol se combinan con permisos de configuración y sesión: comprobar resultado, no asumir aislamiento. Revisores no editan el objeto revisado; shell ask exige revisar efectos incluso si un test escribe caches o fixtures. Los límites de edición por tarea son contractuales hasta disponer de control granular verificable. Agentes no pueden autoconcederse permisos; MCP se habilitará por perfil autorizado y evidencia, no indiscriminadamente.

## Refinamiento individual de identidades (F05)
[Investigación comparada de especialistas](../../docs/INVESTIGACION-ESPECIALISTAS.md): fuentes fijadas, metodología y propuesta de nueve alias. Atlas (team-architect) v0.2.0 implementado con criterio propio, routing discriminante, fronteras, metodología y entrega. Lumen (team-frontend) v0.2.0 integra diseño de producto, implementación frontend, accesibilidad, estados y validación visual proporcional. Nexo (team-backend) v0.2.0 incorpora invariantes de dominio, contratos, autorización, concurrencia, fallos y validación de efectos. Prisma (team-data) v0.2.0 refuerza modelado, integridad, migración, consultas, recuperación y sincronización local-first. Forja (team-platform) v0.2.0 refuerza diagnóstico, automatización, cadena de suministro, distribución, recuperación y operación autorizada. Los otros cuatro roles conservan v0.1.0 hasta su ronda específica. No usar alias como ID de Task ni afirmar exposición de displayName sin prueba. Permisos de Atlas sin cambios; rol asesor con edición/shell/web ask. El resto de matriz se conserva. F05.3 se prepara tras revisar las identidades individuales, con pruebas comparativas focalizadas y modelo autorizado.
