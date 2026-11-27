# Historial resumido por sección
Versión del archivo: 0.113.0 | Última modificación: 2026-11-27

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

## 2026-11-24 — recuperación textual del núcleo
- Calidad: versión, marcador temporal, proyecto, identidad declarada y routing reportados; cotejo persistente de marcador/hashes pendiente. Preparado C1 sin inducir selección de nivel ni herramienta. Conducta y retirada NOT_RUN.

## 2026-11-24 — carga del núcleo y primer resultado funcional
- Calidad: cuatro MATCH del script Verificar y marcador cotejado; C1 contenido correcto, routing no acreditado. Preparado C2 de coordinación con rutas exactas y aceptación de resultados. Retirada y certificación completa pendientes.

## 2026-11-24 — desviaciones de coordinación C2
- Calidad: contenidos correctos y dos delegaciones, duplicación de lecturas y ampliación de alcance no justificadas; C2 no supera aceptación completa. Propuesta de ajuste focalizado tras C3–C6, evaluación de decisiones separada de runtime. Política y script activos de prueba sin cambios; retirada pendiente.

## 2026-11-24 — corrección focalizada del núcleo
- Calidad: C3–C6 decisiones correctas, sin certificación de ejecución. C2 conserva fallo de coordinación.
- Política: v0.15.0 refuerza despacho temprano, propiedad de ejecución, alcance y evidencia. Script v0.2.0 prepara 0.15.0, permite retirada de 0.14.0 por registro y hashes. R1 pendiente; sin instalación definitiva.

## 2026-11-24 — nueva política verificada en laboratorio
- Integración: retirada de 0.14.0 y preparación/carga de 0.15.0 correctas según operador; cuatro MATCH. C2-R1 funcional correcto y reporte acotado, disciplina de ejecución no acreditada por falta de traza. No repetir auditoría; retirada final pendiente y comprobación de coordinación trasladable a equipo real. Sin instalación definitiva.

## 2026-11-24 — cierre limitado F04 y equipo candidato F05
- Integración: retirada 0.15.0 reportada y configuración original preservada. Cierre limitado, disciplina real de coordinación pendiente.
- Equipo: nueve definiciones nativas model-neutral v0.1.0 con permisos explícitos, roles y handoff, sin nuevos líderes. Matriz F05 preparada; validación estática limitada, runtime NOT_RUN, sin instalación definitiva.

## 2026-11-24 — refinamiento individual de especialistas
- Investigación: diez repositorios y doce archivos fuente seleccionados, registro fijado, análisis de patrones y nueve identidades propuestas.
- Equipo: Atlas v0.2.0 con criterio técnico, routing, límites y handoff especializado; permisos intactos. A1–A5 preparados, runtime NOT_RUN. Resto de roles sin cambios. Sin instalación definitiva.

## 2026-11-24 — refinamiento Lumen
- Investigación: siete archivos de cuatro repositorios y tres referencias técnicas consultados selectivamente; registro compartido actualizado.
- Equipo: Lumen v0.2.0 integra criterio visual, UX, implementación, accesibilidad, rendimiento y handoff; permisos intactos. L1–L5 preparados, runtime NOT_RUN. Sin instalación, dependencias ni cambios a otros agentes.

## 2026-11-24 — refinamiento Nexo
- Investigación: siete archivos de cuatro repositorios fijados y cuatro fuentes técnicas consultadas selectivamente; registro compartido actualizado.
- Equipo: Nexo v0.2.0 refuerza dominio, contratos, seguridad aplicada, concurrencia, resiliencia y pruebas de efectos; permisos intactos. N1–N5 preparados, runtime NOT_RUN. Sin instalación, dependencias ni cambios a otros agentes.

## 2026-11-24 — refinamiento Prisma
- Investigación: seis archivos de tres repositorios fijados y cuatro páginas técnicas consultadas selectivamente; una ruta adicional 404 excluida.
- Equipo: Prisma v0.2.0 refuerza modelado, integridad, migraciones, rendimiento, recuperación y sincronización; permisos intactos. P1–P5 preparados, runtime NOT_RUN. Sin instalación, dependencias ni cambios a otros agentes.

## 2026-11-24 — refinamiento Forja
- Investigación: siete archivos de tres repositorios fijados y cinco referencias técnicas contrastadas selectivamente; registro compartido actualizado.
- Equipo: Forja v0.2.0 refuerza diagnóstico, automatización, reproducibilidad, CI/CD, recuperación y límites operativos; permisos intactos. FJ1–FJ5 preparados, runtime NOT_RUN. Sin instalación, dependencias ni cambios a otros agentes.

## 2026-11-24 — refinamiento Faro
- Investigación: seis archivos de tres repositorios fijados y cinco referencias técnicas contrastadas por extractos oficiales; tres rutas 404 excluidas.
- Equipo: Faro v0.2.0 refuerza investigación dirigida, trazabilidad, compatibilidad, contraste de capacidades y protección de información; permisos intactos. FR1–FR5 preparados, runtime NOT_RUN. Sin instalación, dependencias ni cambios a otros agentes.

## 2026-11-24 — refinamiento Veritas y pruebas evolutivas
- Investigación: seis archivos de tres repositorios fijados y documentación de motores consultada selectivamente; sin benchmark local.
- Equipo: Veritas v0.2.0 refuerza revisión independiente, selección por riesgo, mantenimiento y evidencia; permisos intactos. V1–V5 preparados.
- Política/calidad: candidata global 0.16.0 y estrategia 0.6.0 consolidan reutilización, sustitución equivalente, selección progresiva y evaluación de motores. F04 histórico conserva guardia 0.15.0; F05 valida nuevo candidato. Runtime/benchmark NOT_RUN. Sin instalación, dependencias ni cambios a otros agentes.

## 2026-11-24 — refinamiento Bastión
- Investigación: cinco archivos de dos repositorios fijados y referencias oficiales de seguridad y escáneres consultadas selectivamente; dos rutas 404 excluidas.
- Equipo: Bastión v0.2.0 refuerza amenazas, autorización, MCP, secretos, suministro y verificación defensiva focalizada; permisos intactos. B1–B5 preparados, runtime/benchmark NOT_RUN. Política 0.16.0 intacta; sin instalación, dependencias ni cambios a otros agentes.

## 2026-11-24 — refinamiento Ágora y cierre de diseño individual
- Investigación: seis archivos de tres repositorios fijados, extractos de W3C, GOV.UK, Google y Diátaxis; una ruta 404 excluida.
- Equipo: Ágora v0.2.0 refuerza UX writing, documentación, claridad, significado, localización y contenido; permisos intactos. G1–G5 preparados. Nueve candidatos v0.2.0; F05.2-R DONE_DOC, F05 IN_PROGRESS, F05.3 siguiente. Runtime y comprensión con usuarios NOT_RUN. Política 0.16.0 intacta; sin instalación, dependencias ni cambios a otros agentes.

## 2026-11-24 — laboratorio F05.3
- Integración/pruebas: candidato Probar-Equipo-KiloTeam.ps1 0.1.0, workspace exclusivo local, política 0.16.0, nueve agentes 0.2.0, modelo autorizado, registro y retirada selectiva. Procedimiento focalizado sin repetir F03/F04. Sin modificación global ni dependencias. Parser/ejecución Windows y descubrimiento NOT_RUN; F05.3 IN_PROGRESS.

## 2026-11-24 — corrección F05.3-R1
- Pruebas: parser, preparación y doce hashes iniciales reportados PASS con 0.1.0; marcador devuelto pero comparación bloqueada por auxiliar .kilo/.gitignore. Script 0.1.1 reconoce plantilla exacta del CLI fijado y exige autorización adicional para su retirada; registro y guardas intactos. Revalidación focalizada pendiente, sin recrear laboratorio ni almacenar marcador.

## 2026-11-24 — revalidación F05.3-R1
- Pruebas: corrección 0.1.1 PASS reportado de parser, integridad y plantilla; PASS_LOAD_REPORTED. Descubrimiento siguiente mediante descripción nativa de Task; no repetir preparación ni marcador. Sin modificación de código, agentes ni política; F05.3 IN_PROGRESS.

## 2026-11-24 — descubrimiento F05-A
- Pruebas: nueve IDs y responsabilidades reportados desde Task; PASS_REPORTED_DISCOVERY, F05.3 DONE_POC_LIMITED. F05.4 IN_PROGRESS: primera Task focalizada de Faro, lectura y exposición de capacidades; no certificar por recitación ni confundir modo y modelo. Sin cambios de código o instalación.

## 2026-11-24 — primera invocación F05-C-R1
- Pruebas: Faro PASS_REPORTADO de invocación, lectura, evidencia y exposición consultada; 12s reportados, enforcement/benchmark NOT_RUN. Siguiente F05-C-A1 Atlas con evidencia reutilizada, sin mutación. F05.4 IN_PROGRESS; sin cambios de código ni instalación.

## 2026-11-24 — invocación F05-C-A1
- Pruebas: Atlas PASS_REPORTADO de invocación, diseño y reutilización de evidencia; 26s reportados, contrato no aprobado para producción, pruebas/ask NOT_RUN. Siguiente F05-C-G1 Ágora (redacción sin mutación), cierre de ronda por hashes y fixtures registrados para edición posterior. Sin cambios de código ni instalación.

## 2026-11-24 — invocación F05-C-G1
- Pruebas: Ágora PASS_REPORTADO de invocación, composición y fidelidad semántica; tiempos 54s/68s reportados, edición/enforcement NOT_RUN. Cierre de ronda por hashes pendiente; siguiente conjunto de fixtures mutantes requiere registro separado y procedimiento compatible. F05.4 IN_PROGRESS, sin cambios de código ni instalación.

## 2026-11-24 — integridad y fixture editorial F05-C-G2
- Pruebas: doce hashes y auxiliar reportados MATCH al cerrar ronda no mutante. Script 0.2.0 incorpora modos de preparación/verificación/retirada de fixture editorial con propiedad separada, resultado fijo, sin alterar registro original. Parser/ejecución de ampliación NOT_RUN. F05.4 IN_PROGRESS; sin cambios de agentes, política ni instalación global.

## 2026-11-24 — preparación F05-C-G2
- Pruebas: parser y preparación editorial 0.2.0 PASS_REPORTADO, doce MATCH y BASELINE. Siguiente edición real de Ágora y verificación independiente; sin cambios de código o instalación. F05.4 IN_PROGRESS.

## 2026-11-24 — edición efectiva F05-C-G2
- Pruebas: traza de lectura/edición/lectura reportada de Ágora y PASS_F05_EDICION_VERIFICADA, doce MATCH y resultado exacto; 17s/31s reportados. Siguiente retirada selectiva y verificación de baseline. Sin cambios de código, política ni instalación. F05.4 IN_PROGRESS.

## 2026-11-24 — retirada editorial y desarrollo F05-C-DEV
- Pruebas: retirada editorial y doce MATCH posteriores reportados PASS. Script 0.3.0 incorpora extensión de desarrollo, contrato/pruebas protegidos y cuatro propietarios; verificación sin ejecución, retirada con huella revisada. Parser Windows y ejecución pendientes. Sin cambios de agentes, política o instalación global.

## 2026-11-24 — preparación F05-C-DEV
- Pruebas: parser 0.3.0, preflight Node/SQLite y preparación PASS_REPORTADO; doce MATCH, seis BASELINE. Siguiente construcción por cuatro propietarios con paralelismo nativo si disponible, verificación de integridad y revisión previa a ejecución. F05.4 IN_PROGRESS, sin cambios de código o instalación.

## 2026-11-24 — construcción F05-C-DEV
- Pruebas: cuatro implementaciones y despacho concurrente PASS_REPORTADO; integridad de catorce protegidos y cuatro cambios reportada PASS. Revisión Veritas/Bastión sin ejecución siguiente; observación de notificaciones redundantes para fase posterior. F05.4 IN_PROGRESS; sin cambios de código, agentes, política ni instalación.

## 2026-11-24 — revisiones F05-C-DEV-R
- Pruebas: Veritas y Bastión completados, revisión estática reportada sin bloqueantes de código; huella posterior estable. Nueve especialistas con primera tarea devuelta. Puerta de ejecución pendiente de procedencia Node, contraste de fuentes y autorización explícita. Sin cambios de código, agentes, política o instalación.

## 2026-11-24 — contraste F05-C-DEV-E
- Pruebas: diagnóstico Node favorable reportado y cuatro fuentes reconstruidas con hashes coincidentes; inspección directa sin nuevos bloqueantes del PoC. Autorización y ejecución pendientes; comprobar identidad de binario/huella antes y después según alcance. Sin cambios de código o instalación.

## 2026-11-24 — aceptación F05-C-DEV-E
- Pruebas: ejecución autorizada reportada 6/6 PASS, salida 0 y huella previa/posterior intacta. PoC funcional aceptado en su alcance; siguiente comprobación focalizada de ask/deny sin mutación. Sin cambios de código, agentes, política ni instalación.

## 2026-11-24 — F05-C-PERM-01
- Pruebas: solicitud ask y rechazo reportados PASS; Veritas BLOCKED sin ejecución, como se esperaba. Siguiente aprobación única en nueva Task. Sin cambios de código, permisos, agentes ni instalación.

## 2026-11-24 — F05-C-PERM-02
- Pruebas: FAIL_REPORTADO de aprobación puntual (comando ejecutado sin solicitud); causa desconocida. Contraste de fuentes de permisos y procedencia del snapshot auditado; siguiente diagnóstico no mutante de llamadas existentes. Subpuerta permisos BLOCKED, sin cambios de código, configuración o instalación.

## 2026-11-24 — F05-C-PERM-D1
- Pruebas: mismo rol y nuevas hijas reportados, fallo de aprobación reproducido; procedencia no disponible, causa desconocida. Fuentes de composición/configuración contrastadas; siguiente inventario local sanitizado D2, sin mutación. Permisos BLOCKED, sin cambios de código o instalación.

## 2026-11-24 — F05-C-PERM-D2
- Pruebas: modo Manual actual, regla global echo * allow e integridad reportados. Causa probable no demostrada; siguiente sonda fuera de patrón en chat nuevo, sin cambios de permisos ni instalación.

## 2026-11-24 — F05-C-PERM-D3
- Pruebas: rechazo nativo reportado PASS para node --version; operación BLOCKED. Siguiente D4 aprobación única tras confirmar identidad Node; FAIL histórico de echo conservado. Sin cambios de código, configuración o instalación.

## 2026-11-24 — F05-C-PERM-D4
- Pruebas: aprobación única confirmada por operador y salida de versión reportada; ask focalizado PASS_REPORTADO. Siguiente restricción shell de Faro sin habilitar permisos. Sin cambios de código, agentes, configuración o instalación.

## 2026-11-24 — F05-C-PERM-03
- Pruebas: Faro sin shell expuesto, PASS_EXPOSICION_REPORTADO; denegación dinámica NOT_RUN. Reutilizar inventarios de revisores; siguiente retirada selectiva de extensión tras huella y autorización. Sin cambios de código, permisos o instalación.

## 2026-11-24 — F05-C-DEV-X
- Pruebas: identidad Node, retirada autorizada de extensión y baseline original intacto reportados PASS. Siguiente routing discriminante F05-B sin selección impuesta. Sin cambios de código, permisos o instalación.

## 2026-11-24 — F05-B-R
- Gobierno: política 0.17.0 refuerza liderazgo Code, selección proporcional por competencias, delegación de diseño, revisión independiente y evidencia; no reemplaza modo nativo.
- Pruebas: B1 directo reportado PASS, B2 routing NOT_VERIFIED; script 0.4.0 prepara candidato nuevo y reconoce baseline anterior. Recertificación focalizada pendiente, sin cambios de especialistas o permisos.

## 2026-11-24 — carga F05-B-R
- Pruebas: parser, retirada autorizada, preparación 0.17.0 y carga por marcador reportados PASS. Siguiente contraste B1/B2 sin selección impuesta; sin cambios de código, política o instalación global.

## 2026-11-24 — selección autónoma F05-B-R
- Pruebas: B1 directo PASS semántico reportado; B2 tres delegaciones pertinentes elegidas por Code, selección PASS_REPORTADO. Retornos, integración y revisión completada no acreditados; recuperar evidencia existente y verificar integridad. Sin cambios de política, agentes, scripts o instalación.

## 2026-11-24 — integración y recuperación F05-B-R
- Pruebas: recepción 3/3, integración y cierre de ejecución reportados; revisión Veritas BLOCKED por falta de objeto concreto, integridad PASS. Siguiente revisión focalizada de propuesta existente, sin repetir tareas ni modificar política, permisos o instalación.

## 2026-11-24 — recuperación F05-B-RQ
- Pruebas: recuperación asistida de revisión concreta reportada PASS; aceptación conceptual condicionada, revisión del delta no acreditada. Siguiente verificación y retirada autorizada F05.5; conservar regresión de dependencias y límites. Sin cambios de política, agentes, scripts o instalación.

## 2026-11-25 — cierre F05 y apertura F06
- Pruebas: integridad y retirada autorizada F05 reportadas PASS; DONE_POC_LIMITED con límites conservados.
- Skills: team-routing 0.1.0 candidato original, matriz de evaluación F06.1 y catálogo actualizados. Sin instalación ni certificación de runtime.

## 2026-11-25 — F06.1-R
- Investigación: patrones de selección y coordinación de seis fuentes primarias; decisiones y referencias fijadas en INVESTIGACION-SKILLS.md.
- Skills: team-routing 0.2.0, selección por cohesión, competencias, coste y readiness; matriz R1–R9, sin cambios de política ni permisos. Runtime NOT_RUN.

## 2026-11-25 — F06.2-R contrato de tarea
- Equipo/skills: candidato team-task-contract 0.1.0, entrada proporcional, autonomía acotada y handoff con evidencia; sin nuevo protocolo ni cambios de política, agentes o motor.
- Investigación/calidad: fuentes contrastadas y diez casos focalizados; revisión independiente y runtime NOT_RUN; F06 continúa abierta, sin instalación ni release.

## 2026-11-25 — F06.3-R coordinación de tareas
- Skills: candidato team-coordination 0.1.0, dependencias dinámicas, conflictos de recursos, comunicación material, recuperación de ejecución y aceptación.
- Investigación/calidad: código Task/Swarm fijado y doce escenarios focalizados; sin cambios de política, agentes o motor. Revisión independiente y runtime NOT_RUN; sin instalación/release.

## 2026-11-25 — F06.4-R recuperación de contexto
- Skills: candidato team-context-recovery 0.1.0, checkpoint mínimo, reconstrucción focalizada, conciliación de evidencia y continuación segura; no persistencia nueva ni cambios de agentes/política.
- Investigación/calidad: compactación/Swarm y F03.5 contrastados, doce casos focalizados; revisión independiente y runtime NOT_RUN, sin instalación/release.

## 2026-11-25 — F06.5-R requisitos y aceptación
- Skills: candidato requirements-acceptance 0.1.0, clasificación de intención, resolución proporcional de ambigüedad, cobertura y aceptación por evidencia.
- Investigación/calidad: seis referencias comparadas y doce casos focalizados; sin nuevo motor, cambios de política/agentes, instalación ni release. Revisión independiente y runtime NOT_RUN.

## 2026-11-25 — F06.6-R decisiones arquitectónicas
- Skills: candidato architecture-decisions 0.1.0, selección contextual, límites, alternativas, evidencia, reversibilidad y registro de decisiones proporcional.
- Investigación/calidad: seis fuentes comparadas, doce casos focalizados; sin imponer patrón/stack, dependencias nuevas, cambios de política/agentes, instalación ni release. Revisión independiente y runtime NOT_RUN.

## 2026-11-25 — F06.7-R disciplina de implementación
- Skills: candidato implementation-discipline 0.1.0, incremento mínimo completo, reutilización, protección de cambios, flujos reales, compatibilidad y limpieza comprobada.
- Investigación/calidad: cinco fuentes comparadas, doce casos focalizados; sin TDD destructivo, nueva dependencia, cambios de política/agentes, instalación ni release. Revisión independiente y runtime NOT_RUN.

## 2026-11-25 — F06.8-R diagnóstico sistemático
- Skills: candidato systematic-debugging 0.1.0, síntoma/causa, hipótesis discriminantes, reproducción segura, contención y corrección verificable.
- Investigación/calidad: cinco grupos de fuentes contrastados y doce escenarios focalizados; sin umbral arbitrario de intentos, instrumentación obligatoria, nuevas dependencias, instalación ni release. Revisión independiente y runtime NOT_RUN.

## 2026-11-25 — F06.9-R pruebas focalizadas y adopción de calidad
- Skills: focused-testing 0.1.0 y protocolo quality-baseline 0.1.0/schema 1; auditoría inicial, consolidación por equivalencia, evidencia y certificación incremental. Dieciocho escenarios Q1–Q18.
- Política: candidato 0.18.0, disparador de inspección por proyecto y revisión focalizada; sin modificar agentes, permisos o motor. Marcador propio no acredita release; no se creó registro real ni se ejecutó auditoría de proyecto. Revisión independiente y runtime NOT_RUN.

## 2026-11-25 — F06.10-R disciplina Git
- Skills: git-workflow 0.1.0, ramas mínimas, preservación de índice/worktree, integración verificable, consolidación y continuidad quality-baseline; catorce casos G1–G14.
- Política: 0.19.0 candidata, máximo tres ramas propias incluyendo principal, tercera excepcional y consolidación previa; sin modificar agentes, permisos o protección. No se retiraron ramas históricas ni se integró PR. Revisión independiente y runtime NOT_RUN.

## 2026-11-25 — F06.11-R descubrimiento de herramientas y MCP
- Skills: tool-mcp-discovery 0.1.0, capacidades efectivas por agente/sesión, selección autorizada y no redundante, invocación, fallbacks y brecha demostrada; dieciséis casos M1–M16.
- Investigación/calidad: fuentes CLI/Desktop fijadas y documentación MCP; sin nuevas dependencias, inventario persistente, cambios de agentes/política/permisos ni instalación. F09/F10 pendientes; revisión independiente y runtime NOT_RUN.

## 2026-11-25 — F06.12-R ingeniería segura
- Skills: secure-development 0.1.0, controles por frontera/identidad/recurso, secretos, privacidad, dependencias, agentes y evidencia focalizada; dieciocho casos S1–S18.
- Investigación/calidad: NIST, OWASP, SLSA y Kilo; sin nuevas herramientas, permisos, cambios de agentes/política ni instalación. Referencia histórica de política en Bastión pendiente de reconciliación transversal. Revisión independiente y runtime NOT_RUN.

## 2026-11-25 — F06.13-R ingeniería de skills
- Skills: skill-authoring 0.1.0, método propio de investigación objetiva, alternativas, compatibilidad, diseño original, evaluación diferencial, simplificación y evolución controlada; dieciocho casos H1–H18.
- Política: candidato 0.20.0 incorpora método de creación/evolución; núcleo candidato 13/13 y 175 escenarios diseñados. Sin agentes/permisos nuevos ni instalación; revisión transversal, revisión independiente y runtime NOT_RUN. Team Learning pendiente.

## 2026-11-25 — F06-AUD-R auditoría transversal
- Política 0.21.0: routing compacto, carga selectiva y adopción de calidad sin ambigüedad; mantiene autorización, independencia y gates.
- Skills: team-routing 0.3.0; team-coordination, requirements-acceptance, architecture-decisions, implementation-discipline, systematic-debugging, tool-mcp-discovery y focused-testing 0.2.0; restantes intactas. Catálogo 0.16.0 unifica responsabilidades y remite a fuente normativa; 175 escenarios preservados.
- Equipo/registro: Bastión 0.3.0 sin cambio de permisos; manifiesto 0.40.0 separa inventario F06 de evidencias históricas, corrige fase. F06 sigue IN_PROGRESS; laboratorio compatible pendiente, revisión independiente y runtime NOT_RUN.

## 2026-11-25 — F06-LAB-R1 laboratorio comparativo
- Scripts: Probar-Skills-KiloTeam.ps1 0.1.0, 24 fuentes fijadas, dos workspaces, 38 archivos protegidos, creación/retirada selectiva y verificación por propiedad. No modifica F04/F05 ni perfil global.
- Evaluación: preparación y primera ronda comparativa de solo lectura/diseño; reutiliza 175 escenarios sin atribuir cobertura automática. Manifiesto 0.41.0; parser Windows, runtime y revisión independiente NOT_RUN.

## 2026-11-25 — F06-LAB-R1 diagnóstico local
- Evidencia reportada: parser PASS, 24 fuentes MATCH, F06_AUSENTE, checkout b4f9303 detached. Registro documental únicamente; preparación, runtime y revisión independiente pendientes. Manifiesto 0.42.0.

## 2026-11-25 — F06-LAB-R1.2 preflight
- Script 0.1.1: corrige falso positivo potencial por directorio F04 vacío tras retirada histórica, sin borrado ni excepción para entradas activas/enlaces. Preparación anterior BLOCKED reportada; parser/runtime de corrección pendientes. Manifiesto 0.43.0.

## 2026-11-25 — F06-LAB-R1a preparación y carga reportadas
- Evidencia del operador: parser 0.1.1 PASS, F04_EMPTY_CONTAINER, F06_PREPARADO, 38/38 MATCH, auxiliares MATCH_TEMPLATE tras uso y ambos PASS_LOAD_REPORTED. Manifiesto 0.44.0; catálogo, modelo efectivo, invocación, comportamiento y revisión independiente pendientes. Sin cambios de script ni núcleo.

## 2026-11-26 — F06-R1a.2 descubrimiento
- Evidencia del operador: 9/9 agentes propios en ambas variantes, 0/13 skills propias baseline y 13/13 candidate, builtin común kilo-config. Manifiesto 0.45.0; catálogo reportado, no invocación ni permisos probados; sin cambios del núcleo o script.

## 2026-11-26 — F06-R1a.3 invocación explícita
- Evidencia del operador: invocación team-routing declarada satisfactoria y decisiones N1/N3 correctas. Traza y operaciones no verificadas, no prueba autónoma. Manifiesto 0.46.0; sin cambios de componentes ni script.

## 2026-11-26 — F06-R1b.1 lectura comparativa
- Evidencia del operador: contenido esperado de fixture idéntico en ambas variantes; PASS_REPORTED_CONTENT_ONLY. Operaciones, tiempo e integridad posterior pendientes; sin atribuir mejora de rendimiento. Manifiesto 0.47.0; sin cambios de componentes.

## 2026-11-26 — F06-R1b.1 ampliación de evidencia
- Resúmenes visibles aportados: 1 search y Read en cada variante, 6s baseline y 8s candidate, sin Task/skill visibles; exactitud de formato no verificada y rendimiento no establecido. Manifiesto 0.48.0; solo documentación.

## 2026-11-26 — F06-R1b.2 evaluación diferencial
- Evidencia: 38 MATCH antes del diseño; baseline 110s con dos especialistas; candidate 34s y tres activaciones pertinentes visibles, sin contraste independiente acreditado. Hallazgos G1/G2, aceptación no concedida y rendimiento no comparable. Manifiesto 0.49.0; solo documentación, recuperación focalizada pendiente.

## 2026-11-26 — F06-R1b.2-R recuperación y política candidata
- Evidencia: recuperación asistida de 88s, dos revisores inicialmente BLOCKED sin objeto; revisión concreta recuperada e integración focalizada. No certifica autonomía ni equivalencia de rendimiento; G1/G2/G3 pendientes según alcance.
- Política 0.22.0: preflight de objeto accesible y contraste independiente de riesgos materiales solicitado, límite explícito ante capacidad o autorización ausente. Sin cambios de agentes, skills, permisos ni script. Manifiesto 0.50.0 distingue versión activa 0.21.0 e hipótesis candidata; evaluación y revisión independiente pendientes.

## 2026-11-26 — F06-R1b.2-R transición
- Evidencia: integridad posterior a recuperación 38/38 MATCH y auxiliares MATCH_TEMPLATE reportados. Script 0.1.2 fija política 0.22.0, 23 pins y lógica intactos; manifiesto 0.51.0. Retirada antigua autorizada y evaluación nueva pendientes.

## 2026-11-26 — F06-R1b.2-R retirada histórica
- Evidencia reportada: retirada autorizada, 38/38 MATCH, ambos auxiliares reconocidos, F06_RETIRADO y diagnóstico 24 MATCH/F06_AUSENTE. Manifiesto 0.52.0; preparación nueva pendiente, sin cambios de componentes.

## 2026-11-26 — F06-R1b.2-R preparación nueva
- Evidencia reportada: script 0.1.2 parser PASS, 24 fuentes MATCH, F06_PREPARADO y 38/38 MATCH en ambas comprobaciones. Manifiesto 0.53.0; carga, catálogo y evaluación de comportamiento pendientes. Sin cambios de componentes.

## 2026-11-26 — F06-R1b.2-R carga y catálogo
- Evidencia reportada: ambos marcadores PASS_LOAD_REPORTED, 38/38 MATCH, auxiliares reconocidos, nueve especialistas por variante y separación 0/13 vs 13/13 skills propias. Manifiesto 0.54.0; traza independiente, permisos y comportamiento pendientes. Sin cambios de componentes.

## 2026-11-26 — F06-R1b.2-R control y transferencia
- Control directo reportado 14/10s, sin activación redundante visible; nueva misión candidate con cinco skills y una revisión frente a dos encargos baseline. Manifiesto 0.55.0; prompts/retornos, integración, integridad posterior y revisión de política pendientes. Sin cambios de componentes.

## 2026-11-26 — F06-R1b.2-R contraste y cierre focalizado
- Evidencia: prompts/retornos de ambos baseline y único candidate; G1/G3 PASS_REPORTED en muestra, G2 parcial y delta NOT_RUN. Integridad posterior 38 MATCH y auxiliares reconocidos. Manifiesto 0.56.0; continuar escenarios pendientes sin modificar núcleo ni laboratorio.

## 2026-11-26 — F06-R1b.3/R1b.4
- Evidencia: cuatro respuestas conceptuales, prevención de reintentos inseguros y proliferación de skills, activación autónoma visible de skill-authoring. Manifiesto 0.57.0; integridad posterior, revisión independiente y pruebas reales pendientes. Sin cambios de componentes.

## 2026-11-26 — F06-R2.1 reserva
- R1 integridad final reportada 38 MATCH. Fixture de reserva con seis tests nativos, base roja 4/2 y referencia 6/0 en Node Linux; script 0.1.3 extiende propiedad sin modificar núcleo ni pins R1. Manifiesto 0.58.0; revisión independiente, parser Windows y ejecución local pendientes.

## 2026-11-26 — F06-R2.1 preparación
- Evidencia: parser 0.1.3 y preparación reportados, 38+4 protegidos y registro MATCH, dos fuentes BASELINE; fixture ejecutable cotejado con pruebas Linux. Manifiesto 0.59.0; preflight Node, revisión independiente y runtime Windows pendientes. Sin cambios de componentes.

## 2026-11-26 — F06-R2.1 preflight
- Evidencia: identidad de Node 26.12.1, firma válida OpenJS Foundation, huella y ausencia de variables reportadas. Manifiesto 0.60.0; revisión independiente pendiente, posible desvío de modo señalado. Solo documentación, sin ejecución ni instalación.

## 2026-11-26 — F06-R2.2 endurecimiento
- Laboratorio: candidato 0.1.4, modos canónicos, guardas de parámetros/despacho, revalidación de registro R1 y señal de operación parcial. Manifiesto 0.61.0; fixture y pins intactos. Parser, guardas Windows, revisión del delta e integridad local 0.1.4 pendientes.

## 2026-11-27 — F06-R2.3 a R2.8, certificación funcional
- Laboratorio 0.1.4: parser, 12/12 guardas negativas e integridad R1/R2 PASS_REPORTED; revisión independiente APTO CON CONDICIONES.
- Comparación Windows: ambas variantes reproducen 4 PASS y 2 fallos esperados; tras corrección autónoma, ambas obtienen 6/6 PASS, salida 0 e integridad posterior conservada.
- Candidate activa implementation-discipline y systematic-debugging; no se demuestra superioridad causal ni de rendimiento.
- Manifiesto 0.62.0. Evidencias respaldadas fuera del repositorio. Fixture, agentes, skills y política intactos. Recuperación parcial y retirada pendientes.
