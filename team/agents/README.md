# Equipo nativo — diseño de roles
Versión del archivo: 0.6.0 | Última modificación: 2026-11-24

No hay agentes nuevos instalables aún. Identificadores candidatos team-*, mode: subagent, nombre/description/prompt y permisos según esquema certificado en F02. Definiciones neutrales respecto al modelo; selección central por el operador, común por defecto. No depender solo del fallback al padre. Admitir modelos gratuitos/de pago/suscripción autorizados; no fijar el modelo provisional en roles distribuidos. Code, general y explore nativos no se duplican.

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
