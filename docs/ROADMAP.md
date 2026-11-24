# Roadmap de ejecución
Versión del archivo: 0.6.0 | Última modificación: 2026-11-24

Leyenda: DONE_INVENTORY = inventario estático y preparación de laboratorio completados dentro del alcance; no certificación funcional ni cobertura absoluta; IN_PROGRESS = trabajo iniciado, puerta aún no superada; DONE_DOC = entregable documental completado; PENDING = no iniciado/certificado; BLOCKED = dependencia no disponible; NO_NECESARIO = brecha descartada con evidencia (solo fases condicionales). No confundir DONE_DOC con PASS de runtime.

| Fase | Dependencia | Estado | Entregable y puerta de salida |
|---|---|---|---|
| F00 Investigación y archivo | ninguna | DONE_DOC | legacy íntegro; tres estudios y auditoría estática Desktop/CLI fijada; límites explícitos |
| F01 Plan y estructura | F00 | DONE_DOC | arquitectura, políticas, contratos, catálogo y estrategia de distribución actualizados según auditoría; ninguna instalación |
| F02 Runtime y laboratorio | F01 | DONE_INVENTORY | F02.1–F02.4: binario empaquetado y hash, perfil global/administrado, procedencia y colisiones, matriz de capacidades y fixture aislado; informe sanitizado |
| F03 PoC nativa y línea base | F02 | IN_PROGRESS | F03.1–F03.5: Code, marker de instrucciones, subagente y skill reales, task foreground/background, board incremental, permisos y aislamiento, recuperación y baseline |
| F04 Núcleo Code y políticas | F03 | PENDING | AGENTS global y configuración mínima por ruta verificada; prueba de shadowing y sesión nueva; no sustituir Code ni tocar propiedad Desktop; política base sin depender de team-learning aún inexistente |
| F05 Equipo mínimo | F04 | PENDING | arquitectura, frontend, backend, datos, plataforma, investigación, calidad, seguridad, editorial; reutilizar general/explore; cada rol prueba herramientas positivas/negativas, techos de sesión y resultado; profundidad inicial 1; modelos nativos |
| F06 Skills base propias | F04 | PENDING | coordinación, requisitos, arquitectura, implementación, depuración, pruebas, Git, contexto, herramientas, seguridad y creación de skills; evals positivas/negativas y comparación sin skill; probar colisiones y disponibilidad por agente |
| F07 Coordinación avanzada | F05,F06 | PENDING | dependencias, concurrencia, handoff, Swarm, recuperación y consolidación; probar conflicto, cancelación, reanudación de hijo propio, reinicio/compactación por separado y límites; sin polling ni doble escritor; nesting opcional justificado |
| F08 Skills especializadas | F05,F06 | PENDING | familias por stack, UX, frontend, backend, datos, plataforma, QA y editorial; fuentes actualizadas por skill, evals, perfiles de proyectos |
| F09 MCP y plugins existentes | F02,F05 | PENDING | inventario nativo/desktop_*/MCP externo/plugins de motor; procedencia, conexión, exposición e invocación real por rol; perfiles opt-in sin duplicados |
| F10 MCP propios / extensiones | F07,F09,F11 | PENDING | gate de necesidad con resultados F07/F09/F11; cerrar NO_NECESARIO si nativo/archivos cubren; si no, PoC mínimo, SDK compatible, pruebas y fallback; sin fork ni tokens internos |
| F11 Team Learning | F06,F07 | PENDING | metaskill primero, activar tras prueba; usar eventos/resultados existentes, observación semántica, deduplicación, staging, eval, aprobación; pruebas multi-root, privacidad y fallo no bloqueante |
| F12 Integración y rendimiento | F08,F09,F10,F11 | PENDING | escenarios end-to-end, costes observables, latencia, conflictos, recuperación y comparación baseline; sin regresiones críticas |
| F13 Distribución Windows | F12 | PENDING | manifiesto con par Desktop/CLI certificado, destinos y propiedad verificados, dependencias fijadas, paquete sin legacy, scripts Diagnostico/Simular/Instalar/Verificar/Actualizar/Desinstalar/Restaurar, CI y prueba limpia |
| F14 Pilotos y release | F13 | PENDING | web, ERP/local-first y desktop cuando aplique; aceptación del usuario, matriz real, documentación, release y hash verificable |

## Prioridades y paralelismo
Ruta crítica: F02→F03→F04→F05/F06→F07→F11→F12→F13→F14. F08, F09 y F11 pueden avanzar en paralelo tras sus dependencias; F10 se decide después de los resultados F07, F09 y F11, evitando construir almacenamiento o MCP antes de probar la metaskill. F12 espera F10 (implementación certificada o NO_NECESARIO), F08, F09 y F11. La secuencia de IDs no obliga a ejecutar serialmente. Cada fase arranca con criterios y alcance explícitos; revisión de evidencia antes de desbloquear dependientes. F03 está en ejecución en laboratorio, no instalación global.
## Hitos de versión del Harness
0.1.x: diseño y prueba nativa; 0.2.x: núcleo y equipo; 0.3.x: skills y coordinación; 0.4.x: integraciones y aprendizaje; 0.5.x: integración y empaquetado; 1.0.0-rc: piloto; 1.0.0: release certificada. Versiones objetivo, no releases publicadas ni promesas de fechas.

## Desglose ejecutable de las próximas fases
| Paso | Trabajo | Evidencia de salida |
|---|---|---|
| F02.1 | Identificar Desktop, binario CLI empaquetado frente a PATH, versión/hash y referencia de código | Informe sin secretos; divergencias registradas |
| F02.2 | Resolver XDG/global, perfil Desktop, rutas de proyecto y checkout principal, instrucciones y candidatos duplicados | Mapa de rutas, presencia/hash, candidatos de shadowing; no modificación |
| F02.3 | Inventariar modelos sin credenciales, flags, herramientas, permisos, MCP y plugins distinguiendo sus tipos | Matriz fuente estática/exposición/invocación/prueba; lo no observable queda NOT_RUN |
| F02.4 | Definir laboratorio descartable y alcance de prueba, procedimiento de autorización/retirada | Fixture y comandos revisados; sin cambios en proyectos reales |
| F03.1 | Sesión nueva Code, marcador benigno de instrucciones, subagente Markdown y skill de prueba | Identidad, descubrimiento y carga real, sin modo primario nuevo |
| F03.2 | Task foreground y dos hijos background no conflictivos | IDs, retorno, notificación y timestamps solapados; Code continúa, no polling |
| F03.3 | Swarm entre hijos y padre, cursor, sesión raíz independiente | Mensajes observados, alcance, no asumir lectura ni despertar |
| F03.4 | Permisos positivos/negativos por agente y sesión, worktree y estado de sandbox | Pruebas inocuas en fixture; bloqueo de release si se requiere aislamiento no disponible |
| F03.5 | Fallo, cancelación, task_id propio y ajeno, compactación/reanudación y reinicio por separado; baseline directo/delegado | Resultados y límites, métricas disponibles, fallback para funciones ausentes |
F02 no inicia ni modifica servicios por sí solo; las comprobaciones activas son F03. No exponer tokens, leer auth.json, instalar paquetes ni probar sobre proyectos reales.
## Puerta de compatibilidad
El código auditado corresponde a Desktop 1.0.0 / CLI 7.8.27, no necesariamente al instalado. Si difiere, revalidar contratos críticos contra la versión real. Si falta una capacidad central, registrar BLOCKED, alternativa y decisión explícita antes de avanzar; no marcar PASS por documentación.

## Evidencia F02 — 2026-11-24
- F02.1: PASS de identificación de versión; Desktop 1.0.0 y CLI empaquetado 7.8.27 confirmado mediante --version. Metadato PE 1.4.4 no equivale a versión CLI. Hash inventariado localmente, no comparación con distribución oficial.
- F02.2/F02.3: inventario estático realizado; perfil administrado identificado, rutas candidatas y residuos de otros proyectos detectados. Exposición, permisos efectivos, facturación y precedencia real pendientes de F03. No publicar inventario privado.
- F02.4: [procedimiento de laboratorio](../tests/F03-LABORATORIO.md) preparado y utilizado en la primera prueba reportada por el operador. No utilizar proyectos reales ni la prevalidación VX histórica en artifacts/ como evidencia del nuevo equipo.
- F03: inicialmente NOT_RUN; ver evidencia posterior. No confundir identificación del binario con certificación del par host/engine.

## Evidencia F03.1 — 2026-11-24
Fuente: informe textual de Kilo Desktop aportado por el operador, no ejecución ni inspección independiente de trazas desde este repositorio. Reporta coincidencia de los marcadores de instrucciones, skill y fixture; llamada skill y task foreground al subagente team-lab-reader con identificador de sesión hija. Estado PASS_REPORTED para estas comprobaciones; identidad root code, ruta global y precedencia, restricciones de escritura, aislamiento y facturación no certificados. openai/gpt-6-luna es identificador del modelo reportado, no del agente. F03.2/F03.3: probar dos hijos background y comunicación board; F03.4/F03.5 pendientes. No publicar identificadores de sesión ni datos de cuenta.

## Evidencia F03.2/F03.3 — 2026-11-24
Fuente: informe de operador y salida textual de Kilo; no inspección independiente de trazas. PASS_REPORTED: Code identificado como main/code con modelo openai/gpt-6-luna; dos llamadas background running con hijos distintos; lectura independiente posterior a lanzamiento y anterior a notificación A; ambos mensajes board_post/board_read y ambas notificaciones finales recibidas (B llegó después del primer informe). Los dos marcadores esperados coinciden. Diferencia de publicaciones: 456 ms; no mide duración ni demuestra solapamiento. NOT_VERIFIED: intervalos de hijos, actividad del líder dentro de intervalo simultáneo, modelo efectivo de hijos, cobertura BYOK/facturación, cursor incremental y aislamiento entre raíces. F03 permanece IN_PROGRESS. Siguiente: comprobar intervalos observables con marcas Swarm y permiso negativo edit sobre fixture descartable, sin repetir positivos ya registrados. Después F03.5 y pruebas pendientes de F03.3/F03.4. No publicar IDs de sesión, mensajes ni datos privados.

## Evidencia F03.2A/F03.3A
F03.2A/F03.3A — evidencia reportada por operador, 2026-11-24: A START 1795549652198, END 1795549669795; B START 1795549652539, END 1795549673539; Code ACTIVE 1795549669294 (ms, timestamps Swarm). A 17597 ms, B 21000 ms, intersección 17256 ms; marca Code dentro, 501 ms antes del fin común. PASS_REPORTED de solapamiento de intervalos delimitados por publicaciones, actividad observable de Code y lectura incremental con cursor (cinco marcas nuevas y lectura posterior vacía). No prueba concurrencia de inferencia, CPU ni duración continua del líder. Ambas notificaciones originales llegaron, B después del informe inicial. Code hizo una llamada Task adicional sobre la sesión B para obtener salida antes de recibir su notificación original: el informe afirma que no relanzó el trabajo, pero no hay traza independiente para confirmarlo. No se certifica coordinación sin redundancia ni recuperación intencional por este incidente. No se publican IDs de sesión o mensaje. Sin evidencia nueva sobre modelo efectivo de hijos, BYOK/coste, permisos efectivos, aislamiento de raíces ni recuperación.
Siguiente puerta: F03.4a (permisos negativos y positivos en fixture), F03.3b (aislamiento de raíces), F03.4 restantes y F03.5. No repetir pruebas positivas salvo regresión. F03 continúa IN_PROGRESS.
