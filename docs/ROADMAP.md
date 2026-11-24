# Roadmap de ejecución
Versión del archivo: 0.1.0 | Última modificación: 2026-11-24

Leyenda: DONE_DOC = entregable documental completado; PENDING = no iniciado/certificado; BLOCKED = dependencia no disponible. No confundir DONE_DOC con PASS de runtime.

| Fase | Dependencia | Estado | Entregable y puerta de salida |
|---|---|---|---|
| F00 Investigación y archivo | ninguna | DONE_DOC | legacy íntegro; tres estudios enlazados; límites explícitos |
| F01 Plan y estructura | F00 | DONE_DOC | arquitectura, políticas, contratos, catálogo y estrategia de distribución; ninguna instalación |
| F02 Runtime y laboratorio | F01 | PENDING | diagnóstico de solo lectura Windows; versión Desktop/motor, rutas, esquema, precedencia, providers, herramientas, permisos, MCP/plugins y fixture aislado; informe sin secretos |
| F03 PoC nativa y línea base | F02 | PENDING | Code invoca un subagente y skill de prueba; dos tasks solapadas, retorno, board si soportado, aislamiento y fallo controlado; comparación directa/delegada |
| F04 Núcleo Code y políticas | F03 | PENDING | AGENTS global y configuración mínima; sesiones nuevas prueban carga, routing y conflictos de precedencia; no reemplazar Code |
| F05 Equipo mínimo | F04 | PENDING | arquitectura, frontend, backend, datos, plataforma, investigación, calidad, seguridad, editorial; reutilizar general/explore; cada rol prueba herramientas positivas/negativas y resultado |
| F06 Skills base propias | F04 | PENDING | coordinación, requisitos, arquitectura, implementación, depuración, pruebas, Git, contexto, herramientas, seguridad y creación de skills; evals positivas/negativas y comparación sin skill |
| F07 Coordinación avanzada | F05,F06 | PENDING | dependencias, concurrencia, handoff, Swarm, recuperación y consolidación; probar conflicto, cancelación y continuidad; ningún doble escritor |
| F08 Skills especializadas | F05,F06 | PENDING | familias por stack, UX, frontend, backend, datos, plataforma, QA y editorial; fuentes actualizadas por skill, evals, perfiles de proyectos |
| F09 MCP y plugins existentes | F02,F05 | PENDING | inventario, validación de procedencia, conexión y llamada real por rol, permisos y latencia; perfiles opt-in sin duplicados |
| F10 MCP propios / extensiones | F07,F09 | PENDING | demostrar brecha o documentar NO_NECESARIO; PoC mínimo, SDK compatible, pruebas de contrato y seguridad; no servicio permanente |
| F11 Team Learning | F06,F07 | PENDING | detección, deduplicación, propuesta, staging, eval, aprobación y activación; pruebas multi-root, privacidad y fallo no bloqueante |
| F12 Integración y rendimiento | F08,F09,F10,F11 | PENDING | escenarios end-to-end, costes observables, latencia, conflictos, recuperación y comparación baseline; sin regresiones críticas |
| F13 Distribución Windows | F12 | PENDING | manifiesto, dependencias fijadas, paquete sin legacy, scripts Diagnostico/Simular/Instalar/Verificar/Actualizar/Desinstalar/Restaurar, CI y prueba limpia |
| F14 Pilotos y release | F13 | PENDING | web, ERP/local-first y desktop cuando aplique; aceptación del usuario, matriz real, documentación, release y hash verificable |

## Prioridades y paralelismo
Ruta crítica: F02→F03→F04→F05/F06→F07→F11→F12→F13→F14. F08 y F09 pueden avanzar en paralelo tras sus dependencias; F10 se cierra como no necesario si no hay brecha. Cada fase arranca con criterios y alcance explícitos; revisión de evidencia antes de desbloquear dependientes. F02 es el siguiente trabajo, no instalación.
## Hitos de versión del Harness
0.1.x: diseño y prueba nativa; 0.2.x: núcleo y equipo; 0.3.x: skills y coordinación; 0.4.x: integraciones y aprendizaje; 0.5.x: integración y empaquetado; 1.0.0-rc: piloto; 1.0.0: release certificada. Versiones objetivo, no releases publicadas ni promesas de fechas.
