# Plan maestro
Versión del archivo: 0.4.0 | Última modificación: 2026-11-24

## Misión
Convertir Kilo Desktop en un equipo de ingeniería que interpreta objetivos, planifica, ejecuta, delega, integra, certifica y aprende, con intervención mínima del usuario dentro de la autorización. Diseñar desde cero, con experiencia y patrones de las investigaciones y la auditoría de código fuente; legacy es referencia histórica inmutable.

## Alcance 1.0
Windows, versión real de Kilo Desktop instalada (referencia auditada: Desktop 1.0.0 + CLI 7.8.27; no se afirma que sea el binario instalado ni la última versión), Code nativo, agentes especialistas, políticas globales, skills propias, integración dinámica de herramientas/MCP existentes, aprendizaje controlado, instalador y desinstalador selectivos, pruebas y documentación. No construir otro motor, chat, proveedor de modelos, servicio permanente, base vectorial, orquestador externo o interfaz Desktop salvo necesidad posterior demostrada.

## Entregables
1. Inventario reproducible de runtime y matriz de capacidades confirmadas/ausentes.
2. Política global breve y contratos de tareas/evidencia; adaptación al esquema real.
3. Equipo de especialistas definido por competencias, no jerarquía redundante.
4. Catálogo de skills originales con fuentes, activación, límites, procedimientos, verificaciones y evaluaciones.
5. Coordinación nativa, registro de estado mínimo solo cuando haga falta, recuperación y trabajo simultáneo.
6. Integración MCP de terceros y MCP propios condicionados a brechas comprobadas.
7. Team Learning con propuestas, pruebas, revisión, aprobación y control de versiones.
8. Paquete global reproducible, instalador idempotente, actualización, rollback, diagnóstico, desinstalación y guía de uso.
9. Certificación en Windows Desktop y pilotos de proyectos representativos; release 1.0.0.

## Reglas de decisión
Nativo primero > configuración > skill > herramienta existente > MCP/plugin propio. Un cambio debe reducir fricción o habilitar una capacidad comprobablemente ausente. Usar contrato/validación mecánica donde una instrucción no basta. No confundir instrucciones con límites efectivos de seguridad; no asignar permisos universales por comodidad.
Trabajo sencillo directo; tareas independientes delegadas; tareas dependientes ordenadas; riesgo alto revisión independiente. Concurrencia ajustada por evidencia, no por cantidad de agentes.
Toda ampliación debe tener dueño, necesidad, alternativas, coste, dependencias, alcance, prueba, fallback y criterio de retirada. Evitar solapamientos entre agentes, skills y MCP.

## Gestión
Roadmap por puertas, no por fechas inventadas. Cada fase tiene entregable, criterios de entrada/salida y estado. Revisar y actualizar estado solo con pruebas. Cambios de alcance/arquitectura se registran como decisiones breves; no multiplicar documentación repetitiva. La release no es una suma de archivos: requiere ejecución real y aceptación. La política de limpieza sin respaldo de componentes antiguos no se aplica automáticamente a futuras actualizaciones del nuevo Harness; para ellas se propone rollback selectivo y reversible, sujeto a aprobación.

## Decisiones tras auditoría de código
Fuente normativa para estas decisiones: [auditoría fijada](AUDITORIA-CODIGO-KILO-DESKTOP.md). Distinguir implementación estática, exposición en runtime y certificación funcional.
- Integración en el CLI empaquetado (kilo serve), no en otro motor ni mediante fork de Electron. Desktop, CLI y SDK son versiones independientes; registrar binario real, hash y versión.
- Code (id code, compatibilidad build) único líder del Harness; conservar modos nativos. Task, sesiones hijas, notificación background, Swarm, catálogo de skills, compactación, cola y gateway MCP son capacidades existentes, no componentes a reconstruir.
- Separar global XDG del perfil administrado Desktop. La primera instrucción global existente puede ocultar otras. F02 debe resolver rutas y F03/F04 demostrar carga efectiva y merge sin invadir archivos administrados.
- Profundidad inicial nativa 1: Code delega a hijos directos. No equivale a límite de concurrencia. Ampliar solo tras caso, autorización y evidencia; no fijar un máximo de motor sin medición.
- Permisos independientes por rol y sesión, techos heredados, guardas de mutación y MCP. La auditoría detectó sandbox de ejecución deshabilitado en nuevos chats de ese snapshot; no asumir confinamiento. Worktree, política y permisos no sustituyen aislamiento técnico.
- Priorizar herramientas desktop_* y nativas realmente expuestas; diferenciar plugin de motor, plugin de interfaz y MCP estándar. No acceder a tokens internos ni ASAR; no exigir plugin propio ni MCP de estado para v1 si no existe brecha.
- Modelos: respetar resolución nativa y configuración autorizada; no imponer overrides de modelo/proveedor/variant dinámicos por coste o complejidad.
- Team Learning: metaskill semántica y observaciones mínimas; usar resultados/eventos nativos, no monitor paralelo por defecto. Introducir activación de la skill solo cuando exista y se pruebe (F11).
- Evidencia de cierre: retorno task, estado UI done, conexión MCP y recepción de board no equivalen a verificación de resultado. Distinguir cada uno.

## Control de modelo uniforme
Requisito del operador: un único modelo autorizado para Code y especialistas; objetivo de laboratorio openai/gpt-6-luna, pendiente de confirmación BYOK y coste. No sustituir por free/auto, otro proveedor ni modelo de pago por iniciativa del agente. Si catálogo, cuota o configuración impiden usarlo, informar y detener delegación afectada. Política no equivale a enforcement del motor. Fuente fijada: https://github.com/Kilo-Org/kilocode/blob/03a6f07d053cd7e6aa88fa1e258e93510335259f/packages/opencode/src/kilocode/tool/task.ts#L282-L412 . Para tarea nueva sin override explícito: workflow > selección guardada (solo KILO_CLIENT=cli) > modelo del agente > subagent_model disponible > padre. Reanudación puede usar modelo de sesión previa; overrides explícitos se resuelven por separado. No inferir origen de kilo-auto/free por este orden. Probar primero model: openai/gpt-6-luna en definición de un lector de laboratorio, nuevo chat Code con mismo modelo y nueva task sin override; no reusar task_id. Verificar identidad efectiva del hijo y del líder, y proveedor/coste en panel, sin copiar credenciales. Si falla, revisar configuración efectiva y workflow; probar subagent_model y overrides autorizados por separado. Centralización en F04/F05 tras evidencia; no editar perfil administrado de Desktop.

## Corrección de referencia de modelo — 2026-11-24
F03.4C — informe del operador: Code main/code reportó openai/gpt-6-luna; la definición del lector declaró esa cadena; Task foreground nueva sin overrides devolvió Model not found: openai/gpt-6-luna. No se obtuvo ejecución del hijo ni lectura delegada. FAIL_REPORTED de la referencia configurada; identidad efectiva común y facturación NOT_VERIFIED. No hubo sustitución deliberada. No atribuir la causa definitiva sin catálogo efectivo.
Fuente CLI fijada: https://github.com/Kilo-Org/kilocode/blob/03a6f07d053cd7e6aa88fa1e258e93510335259f/packages/opencode/src/provider/provider.ts#L2212-L2217 ; parseModel divide por primera barra. Fuente Desktop: https://github.com/Kilo-Org/kilo-desktop/blob/0e86bc8c350b5ee2009bbb8d4722c955355bbe10/plugins/chat/src/web/selection/model-catalog.ts ; providerID y modelID son campos distintos, Kilo Gateway id kilo, distintivo BYOK específico del Gateway. Hipótesis: openai/gpt-6-luna es el modelID del Gateway, y la referencia completa sería kilo/openai/gpt-6-luna. No confundir nombre/identidad informada en prompt con par de metadatos de selección ni con proveedor facturado. No declarar el candidato disponible hasta comprobar catálogo.
F03.4D: consultar con binario empaquetado models kilo (sin --verbose/--refresh) desde laboratorio, filtrar Luna; no inicia inferencia, puede inicializar caché/config de CLI independiente, ausencia no demuestra ausencia en Desktop. Confirmar selector de Desktop en Kilo Gateway con BYOK y, cuando sean visibles, los dos campos de modelo de sesión. Solo si el catálogo acredita exactamente kilo/openai/gpt-6-luna y usuario autoriza ese modelo, sustituir exclusivamente model del lector en laboratorio, conservar permisos; abrir nuevo chat con misma selección Gateway y lanzar nueva task sin overrides ni task_id, una sola lectura. Si catálogo no lo confirma, detener y reportar; no adivinar otro ID. Registrar par providerID/modelID cuando se exponga, identidad hijo, resultado y coste/proveedor de las dos solicitudes en panel. Si solo se expone identidad textual, marcar alcance de evidencia. No cambiar auth, perfil Desktop ni modelos globales.
