# Historial resumido por sección
Versión del archivo: 0.32.0 | Última modificación: 2026-11-24

## 2026-11-24
- Investigación: archivo legacy, Kilo nativo, comparación de harness públicos y Task Observer.
- Gobierno: plan maestro, roadmap F00–F14, arquitectura y política candidata, reglas del repositorio.
- Equipo: roles, contratos y catálogo de 35 skills candidatas (13 base + 21 especializadas + 1 aprendizaje).
- Integración: estrategia Kilo/MCP, dependencias y plan de scripts.
- Calidad: matriz de certificación y manifiesto no instalable. Sin código de runtime ni release publicada; F02 pendiente.
Cada sección se actualiza aquí con cambios resumidos; no repetir historial en cada archivo. La versión del archivo y la versión de release son independientes.

## 2026-11-24 — revisión tras auditoría de código
- Investigación/arquitectura: fuente Desktop 1.0.0 y CLI 7.8.27 fijadas; capas, sesiones, cola, gateway, perfiles y precedencia.
- Gobierno/roadmap: F02/F03 desglosadas; gates de permisos, shadowing, reanudación y simultaneidad; F10 posterior a F11, opcional con evidencia.
- Equipo: Code nativo, profundidad 1 inicial, resolución nativa de modelos, permisos reales y mapeo Task/Swarm; activación Team Learning tras certificación.
- Integración/distribución: separar plugins Desktop/CLI y MCP; preservar ownership administrado y par de versiones probado.
- Calidad: nuevos casos específicos, estado estático separado de runtime. 15 archivos de diseño actualizados a versión individual 0.2.0; catálogo 35 y roles 9 sin cambios. No se publica release ni se modifica legacy.

## 2026-11-24 — comprobación F02
- Runtime: versión CLI empaquetada 7.8.27 confirmada por operador; inventario estático, sin pruebas de agentes.
- Calidad: guía de laboratorio F03 y exclusión Git de bytecode Python; F02.4 pendiente de creación local. Artefacto VX anterior no es evidencia actual.

## 2026-11-24 — primera prueba nativa
- Calidad/runtime: F03.1 con marcadores y llamada foreground correctos según informe del operador (PASS_REPORTED parcial). F02 cerrado como inventario limitado, no certificación. Preparada prueba background/Swarm. Facturación, permisos, solapamiento y recuperación aún no certificados.

## 2026-11-24 — delegación asíncrona y Swarm
- Runtime/calidad: dos hijos background, comunicación, continuidad tras delegación y ambas notificaciones reportadas correctamente. Solapamiento y modelo de hijos no verificados. Pruebas focalizadas de intervalos, cursor y permiso negativo preparadas.
- Política: cierre definitivo tras resultados requeridos, estados diferenciados y concurrencia sin conflicto de escrituras. No instalada. F03 sigue abierta.

## 2026-11-24 — solapamiento observable
- Runtime/calidad: intervalos Swarm A/B con 17.256 ms de intersección, marca Code dentro, cursor incremental y notificaciones originales reportados. No certifica inferencia simultánea ni modelo de hijos. F03 abierta.
- Política: evitar reanudación por mera demora de notificación; task_id solo para trabajo adicional autorizado o recuperación de fallo confirmado. Preparada prueba focalizada de permisos; sin instalación global.

## 2026-11-24 — permisos del lector
- Calidad/runtime: lectura y ausencia reportada de herramientas mutantes; hash del fixture antes/después idéntico. No hubo rechazo explícito ni prueba de aislamiento.
- Equipo: distinguir lector de constructor; F03.4B de edición y shell positivos preparada. Sin instalación global ni cambios en legacy.

## 2026-11-24 — constructor y control de modelo
- Runtime/calidad: seis herramientas del constructor operativas según reporte, verificación externa de hash pendiente. Modelo del hijo kilo/kilo-auto/free difiere del objetivo autorizado.
- Gobierno/integración: modelo uniforme obligatorio, precedencia nativa auditada y prueba focalizada F03.4C; no instalación, no cambios de facturación ni configuración global.

## 2026-11-24 — resolución de modelo Gateway
- F03.4C: referencia directa openai/gpt-6-luna falló; selección uniforme sigue bloqueada. Hipótesis de ID calificado kilo/openai/gpt-6-luna, pendiente de catálogo y prueba F03.4D. Sin cambios de configuración local ni facturación.

## 2026-11-24 — catálogo Gateway confirmado
- Integración/calidad: CLI lista la referencia calificada y operador actualizó el lector de laboratorio. Verificación externa posterior del contenido del constructor y hash intacto del lector. Pendientes ejecución uniforme en Desktop y facturación, sin instalación global.

## 2026-11-24 — resiliencia e independencia de modelos
- Runtime: selección explícita por agente y coincidencia comercial de Luna reportadas; proveedor independiente y facturación no verificados.
- Gobierno/arquitectura: Luna provisional; selección central configurable, modelos gratuitos y de pago autorizados, contratos y verificación objetiva independientes del modelo, adaptación acotada y comparación F12. F03.4E preparada. Se consolidó detalle de resolución en integración y evidencia en laboratorio; sin instalación global.

## 2026-11-24 — configuración central y continuidad
- Runtime: lector sin modelo individual ejecutado con modelo coincidente con configuración central; precedencia exacta y facturación pendientes.
- Calidad: casos focalizados de reanudación de hijo propio, aislamiento Swarm y rechazo de reanudación desde otra raíz preparados; sin instalación global.

## 2026-11-24 — reanudación y separación de tableros
- Runtime: mismo hijo reanudado con contexto y modelo reportados, nueva lectura y mensaje Swarm. Raíz B no muestra el mensaje de A en la muestra.
- Calidad: aislamiento universal no certificado; preparado caso negativo de parentesco con hijo propio de laboratorio. Sin instalación global ni repetición de positivos.

## 2026-11-24 — control de parentesco
- Runtime/calidad: rechazo explícito de reanudación desde raíz distinta, sin reintento reportado. Preparada prueba de error de lectura y recuperación lógica; fallo terminal, cancelación, compactación y reinicio permanecen separados. Sin instalación global.

## 2026-11-24 — recuperación lógica de tareas
- Runtime/calidad: error de read, BLOCKED, corrección de alcance y reanudación del mismo hijo con resultado válido reportados. No error terminal de Task.
- Política: distinguir bloqueo/fallo/cancelación, preservar evidencia, corregir antes de reintentar y respetar cancelación explícita; preparada F03.5D según control Stop subagent de Desktop. Sin instalación global.

## 2026-11-24 — cancelación y continuidad
- Runtime/calidad: estados running/cancelled/completed, mismo hijo y lectura recuperada reportados; continuidad de contexto parcial. Preparada compactación nativa /compact de raíz entre turnos. Fallo terminal y reinicio no certificados; sin instalación global.

## 2026-11-24 — recuperación de checkpoint y estado histórico
- Calidad: siete campos recuperados; ejecución de compactación no acreditada. Resumen intermedio conserva running frente a completed reportado previamente para mismo hijo.
- Política: reconciliar estado operativo con evidencia nativa reciente antes de actuar; preparar F03.5F de reapertura ordenada. Sin instalación global ni publicación de IDs.

## 2026-11-24 — continuidad y estado unknown
- Calidad: raíz, checkpoint y referencia hija recuperados; ejecución actual unknown, reinicio no acreditado. Auditoría confirma fallback unknown cuando falta estado de participante en snapshot, no causa concreta.
- Política: conservar por separado resultado verificado y estado actual; no reanudar automáticamente ni repetir evidencia válida. Sin instalación global.

## 2026-11-24 — compactación y reapertura confirmadas
- Calidad: operador confirma ejecución/finalización de /compact y cierre/reapertura; recuperación de contexto e identidad reportada, persistencia del estado operativo no verificada.
- Rendimiento: F03.6 preparada con auditoría declarativa comparable directa/delegada y métricas observables. Sin ejecución remota de laboratorio ni instalación global.

## 2026-11-24 — baseline de delegación
- Rendimiento: UI reporta 18s directo, 59s delegado y 19s hijo, resultados principales coincidentes; una muestra, métricas de coste no disponibles y discrepancias de líneas no resueltas.
- Política: directo para tareas breves, delegación justificada y validación proporcional. Preparada F03.7A de techo de sesión condicionada a control real. Sin instalación global.

## 2026-11-24 — límites de permisos de sesión
- Calidad: precheck NOT_VERIFIED, herencia de sesión bloqueada por falta de control accesible acreditado. Preparado caso diferencial de edición por archivo en perfil descartable.
- Política: distinguir permisos por agente/proyecto/sesión y no equiparar contrato con confinamiento. Sin instalación global.

## 2026-11-24 — bloqueo previo a edición granular
- Calidad: perfil y fixtures preparados, hashes intactos; no ejecución de especialista granular ni edit acreditada. Preparado diagnóstico de identidad/Task/descubrimiento y despacho explícito sin nesting ni cambios globales.

## 2026-11-24 — edición granular comprobada
- Calidad: despacho corregido, edición autorizada y rechazo explícito de edición protegida reportados; hashes externos verifican diferencia e integridad. apply_patch comparte permiso edit según fuente; herramienta exacta por llamada no acreditada.
- Política/contrato: capacidades semánticas y herramientas expuestas, sin eludir denegaciones. Preparada F03.8 de coordinación sin reanudación redundante. Sin instalación global.

## 2026-11-24 — coordinación y transición limitada a F04
- Calidad: dos notificaciones, trabajo independiente y no reanudación reportados; integración parcial por error de ruta, ausencia de polling no acreditada.
- Política/contrato: referencias concretas y base de workspace; retorno terminal no equivale a aceptación. F03 cerrada como PoC limitada para desarrollo candidato; F04.1 preparación de prueba de instrucciones globales, sin instalación ni certificación integral.

## 2026-11-24 — diagnóstico de rutas globales
- Integración: directorios de usuario y perfil Desktop existentes; tres archivos globales ausentes según operador. Preparada prueba temporal de marcador aleatorio, creación exclusiva y retirada por hash; carga efectiva pendiente. Sin instalación global definitiva.

## 2026-11-24 — resolución de instrucciones globales
- Runtime: marcador global no disponible, marcador proyecto correcto. Auditoría distingue Global.Path.config XDG y servicio global.config con override de Desktop; preparada alternativa instructions absoluta desde JSONC global de usuario, condicionada a ausencia de conflictos y propiedad comprobable. Sin instalación global ni modificación de perfil.

## 2026-11-24 — protección de configuración existente
- Integración: preflight abortó por kilo.jsonc de usuario existente. Preparada prueba de overlay kilo.json mediante merge nativo, condicionada a ausencia de instructions y otros candidatos, con verificación de hashes y retirada selectiva. No se sobrescribe configuración existente.

## 2026-11-24 — recuperación de instrucciones explícitas
- Integración: overlay creado sin sobrescribir JSONC, último informe devuelve marcador global y de proyecto; cotejo local exacto y retirada pendientes. Estrategia complementaria candidata condicionada a compatibilidad y propiedad. Sin instalación definitiva.

## 2026-11-24 — recuperación de referencias de la prueba global
- Integración: cierre abortado antes de retirar por variables de sesión ausentes. Preparada recuperación con hashes históricos de configs y comparación exacta con plantilla conocida del marcador; no se afirma hash histórico de AGENTS.md. Incorporar registro local persistente de propiedad en futuras pruebas. Limpieza aún pendiente.

## 2026-11-24 — normalización nativa de configuración
- Integración: hash original coincide según flujo, overlay difiere; retirada abortada. Fuente confirma inserción automática de $schema, causa local no verificada. Preparada comprobación semántica estricta y retirada autorizada solo de temporales identificados. F13 deberá contemplar normalización nativa y propiedad persistente.

## 2026-11-24 — núcleo global candidato
- Integración: F04.1 PASS_RECOVERED reportado, schema oficial presente, temporales retirados y original intacto. Limitación de hash histórico del marcador conservada.
- Política: núcleo operativo v0.14.0 consolidado en siete secciones, routing N1–N4, contrato, capacidad, seguridad, calidad, recuperación y evolución condicionada. Matriz F04 preparada; validación funcional NOT_RUN, sin activación ni release.

## 2026-11-24 — preparación de evaluación del núcleo
- Calidad: revisión estática del candidato sin cambios de política; script temporal F04 con registro de propiedad persistente, schema y protección de originales. Prueba funcional Windows NOT_RUN; no instalador definitivo ni activación automática.
