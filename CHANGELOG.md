# Historial resumido por sección
Versión del archivo: 0.8.0 | Última modificación: 2026-11-24

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
