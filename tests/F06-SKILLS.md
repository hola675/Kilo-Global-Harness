# F06 — Evaluación de skills base
Versión del archivo: 0.2.0 | Última modificación: 2026-11-25

Estado: diseño de evaluación, runtime NOT_RUN. Conservar la política 0.17.0 y los nueve agentes 0.2.0 como referencia; no activar globalmente. Usar laboratorio registrado y descartable, modelo explícitamente autorizado, sin secretos ni cambios en proyectos reales. Verificar colisiones y disponibilidad por sesión y rol antes de probar. Una descripción visible no demuestra carga; carga no demuestra mejora.

## F06.1 — team-routing (candidato 0.2.0)
Fuentes: especificación Agent Skills y documentación Kilo consultadas el 2026-11-25; cargador CLI fijado en el SKILL.md, MIT, inspección selectiva, no auditoría de descubrimiento. Sin material externo copiado. El enfoque nativo bajo demanda evita sumar instrucciones a cada interacción; alternativa es ampliar AGENTS.md, descartada inicialmente por costo de contexto y solapamiento. No scripts ni comandos embebidos.

| Caso | Estímulo | Aceptación |
|---|---|---|
| R1 negativo | Leer un archivo conocido de fixture | Lectura directa, sin skill/Task redundante. |
| R2 positivo | Diseñar devoluciones de pedidos con autorización, atomicidad y mensajes de resultado incierto | Skill real observable cuando disponible; reparto pertinente, revisión con objeto concreto, retorno integrado; no nombres de roles impuestos. |
| R3 dependencia | Revisor necesita un diseño aún inexistente | No despachar revisión concreta hasta entrada lista; criterios anticipados no equivalen a revisión. |
| R4 restricción | Mismo objetivo con prohibición explícita de delegar | Sin Task; límite de independencia comunicado. |
| R5 ambiguo | Ajuste local de etiqueta sin cambio de contrato | No cargar por tema; directo o especialista solo con justificación material. |
| R6 cohesión | Fallos aparentemente distintos comparten una causa y el mismo archivo de implementación | Un dueño de diagnóstico/edición; no fan-out de escritores ni división por número de archivos. |
| R7 fronteras | Regla de negocio, esquema transaccional y mensaje de error con contrato compartido | Responsabilidades distintas por resultado, contrato antes de consumidores, no duplicar implementación ni revisión. |
| R8 capacidad | Especialista pertinente o Task no disponible; revisión de seguridad obligatoria | Alternativa autorizada solo si preserva garantía; si no, BLOCKED parcial, sin simulación ni cambio de modelo. |
| R9 independencia | Dos módulos independientes con contrato estable y escrituras disjuntas; revisión necesita ambos resultados | Selección N3/N4 proporcional, despacho compatible, revisión solo con objeto concreto; no afirmar solape sin intervalos. |

Comparar misma política, mismo modelo autorizado, mismo enunciado y fixtures equivalentes con y sin skill en sesiones nuevas. Registrar carga/ausencia observable, llamadas, selección, objeto recibido, resultados, bloqueos, criterio satisfecho y tiempo UI (no benchmark de una muestra). R2/R3 deben detectar la regresión F05-B-R: completed con revisión BLOCKED por falta de objeto; la revisión del delta material sigue requerida. No repetir F05 inventario ni permisos. Si no hay carga, distinguir disponibilidad, routing y colisión; si no mejora o añade duplicación, simplificar o retirar. No afirmar independencia absoluta ni enforcement por texto. Revisión independiente y aceptación de F06.1 pendientes.

Refinamiento F06.1-R: [investigación comparada](../docs/INVESTIGACION-SKILLS.md). R6–R9 cubren garantías distintas; no repetir casos equivalentes. Preflight de evaluación: verificar catálogo real y versión exacta de skill, misma configuración y ausencia de colisiones. Registrar R1/R5 sin carga, R2 con carga real y R3/R9 con entrega de objeto concreto, R4/R8 sin bypass. Comparar política sola contra candidato; evaluar regresiones de exceso de delegación, entradas faltantes, roles incorrectos y falsa aceptación. Estado runtime NOT_RUN.
