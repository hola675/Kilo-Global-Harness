# Contrato de interacción: estados, recuperación y efectos
Versión del archivo: 0.1.0 | Última modificación: 2026-11-28

Aplicación: flujos con latencia, envío de información, persistencia, desconexión, permisos o resultado incierto. Referencia original para ux-product-design; no es máquina de estados obligatoria ni contrato de backend. Solo consulta cuando esos problemas sean materiales. Los nombres de estado son ilustrativos y se adaptan al dominio real.

## Contrato mínimo
Registra para cada transición material: estado previo, evento/acción, precondición y permiso, autoridad de resultado (contrato/servicio/núcleo o estado local confirmado), estado siguiente y evidencia, información y acciones visibles, recuperación y conservación de datos. No inventar endpoints, estados de dominio ni persistencia. Separa estado de formulario, solicitud y operación de negocio cuando sus ciclos difieran. Una acción visual no acredita ejecución. Si falta estado verificable, declara incertidumbre y solicita el contrato concreto a Code.

| Situación | Información útil | Acción segura / límite |
|---|---|---|
| Sin datos confirmados | Explicar ausencia, filtros o primera acción relevante según contexto | No representar ausencia como error ni ocultar fallo de carga. |
| Enviando | Mostrar que se recibió la acción y que aún no se confirmó el resultado | Evitar duplicación por interacción; no prometer cancelación si no existe. |
| Entrada rechazada | Campo o dato que necesita corrección y cómo corregirlo | Conservar lo válido cuando seguro; no repetir datos sensibles en el mensaje. |
| No permitido | Explicar restricción sin exponer información protegida | No inducir reenvío ni confundir permiso con formato inválido. |
| Indisponibilidad confirmada | Problema del servicio, no atribuirlo a la persona | Alternativa o reintento solo si permitido y seguro. |
| Resultado incierto | La operación podría haberse aplicado; no se dispone de confirmación | Consultar estado por mecanismo autorizado si existe; no iniciar otra operación con efecto ni declarar fallo/éxito. |
| Resultado confirmado | Mostrar consecuencia e identidad útil cuando contrato lo permite | Permitir siguiente tarea; reversión solo si es capacidad real. |
| Sin red / datos antiguos | Distinguir última información confirmada, cambios locales y estado no sincronizado | Cola offline y reconciliación solo cuando soportadas; no afirmar persistencia de borradores. |

## Decidir la forma
Usa formulario de una sola vista para decisiones relacionadas y abordables; divide por objetivos significativos cuando reduzca complejidad real, permite retroceder y revisa conservación de entrada. Diálogo solo si la interrupción o subtarea lo justifica y puede mantener foco, contexto y salida accesibles. Para cambios irreversibles o consecuencias relevantes muestra el alcance efectivo y alternativa de corrección, confirmación o reversión según contrato; una confirmación visual no demuestra prevención de duplicado. En escritorio denso, conserva ritmo de trabajo, teclado y acceso a información; en TPV evita depender de gestos finos o red permanente; en móvil prueba condiciones de espacio y entrada. No obligar a cada perfil a compartir el mismo layout.

## Ejemplo propio, hipotético
Una solicitud ficticia de venta se envía y vence el plazo de respuesta. El identificador de operación solo se muestra si está confirmado y permitido. Estado de solicitud: sin confirmación; estado de negocio: desconocido. La pantalla informa «No se pudo confirmar el resultado. Comprueba el estado antes de registrar otra venta». Se ofrece comprobar estado únicamente si el contrato contiene tal capacidad; si no, se conserva la referencia disponible, se evita duplicar el efecto y se deriva al procedimiento de recuperación autorizado. No ofrecer cancelación o devolución ficticia. Si la autoridad confirma rechazo sin efecto, se habilita corregir o reintentar conforme al contrato; si confirma éxito, mostrar el resultado. El ejemplo no prescribe una API ni acredita idempotencia.

## Verificación proporcional
Definir tareas sin indicar la solución, estados alcanzables y resultado observable. Para el ejemplo, distinguir validación corregible, respuesta incierta y confirmación; usar datos sintéticos, oráculo definido con anterioridad, y no efectuar pagos. Inspección heurística y prototipo son evidencia limitada; investigación real requiere autorización, personas pertinentes y protección de datos. Comprobar navegación, lectura, foco y recuperación según alcance; si no hay UI ejecutable, revisión documental únicamente. No exigir pruebas de todos los estados no afectados.

## Fuentes de criterio
Consulta documental 2026-11-28: [GOV.UK Service Manual: investigación moderada](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing), [GOV.UK Design System: validación](https://design-system.service.gov.uk/patterns/validation/) y [revisión de respuestas](https://design-system.service.gov.uk/patterns/check-answers/); [Carbon: formularios](https://carbondesignsystem.com/patterns/forms-pattern/); [Jakob Nielsen: heurísticas de usabilidad](https://www.nngroup.com/articles/ten-usability-heuristics/); [W3C WCAG 2.2, explicación informativa de 3.3.4](https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html). Aplicar criterios de accesibilidad correspondientes al medio y contrato; no generalizar una guía de diseño gubernamental o de IBM. Las tablas y el ejemplo son propios; no se incluyen código, recursos ni textos de terceros. La adaptación de estados inciertos deriva también de las garantías B02/B07 del Harness, no de una garantía de ejecución de esas fuentes.
