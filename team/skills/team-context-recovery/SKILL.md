---
name: team-context-recovery
description: "Recupera continuidad verificable después de compactación, reapertura, interrupción, cambio de sesión o pérdida material de contexto; preserva decisiones, resultados válidos, referencias y límites. Usar al preparar un punto de continuación necesario o reconstruir trabajo incierto. No cargar en cada turno normal ni para reintentar un fallo de ejecución con contexto intacto."
metadata:
  version: "0.1.0"
  last_modified: "2026-11-25"
---

# Continuidad por evidencia mínima

## Autoridad y frontera
Code conserva misión, autorización, propiedad de recursos e integración. Esta skill prepara y reconstruye contexto entre puntos de continuidad; routing decide reparto, task-contract define encargos y coordination opera tareas activas y fallos confirmados. No depende de que esas skills estén cargadas o existan. Un hijo recupera solo su encargo y devuelve discrepancias a Code; no reconstruye el equipo ni se reasigna. AGENTS.md, solicitud vigente, permisos y capacidades reales prevalecen. No instalar almacenamiento, plugins, hooks, scripts ni servicios; no forzar compactación o reinicio ni prometer continuidad automática.

## 1. Determinar el motivo y el alcance
Distinguir continuación normal con contexto suficiente, compactación manual/automática confirmada, reapertura ordenada, nueva raíz, interrupción abrupta, resumen incompleto o contradictorio y cambio autorizado de misión. No atribuir causa sin evidencia. Un resumen presente no prueba que se ejecutó compactación; conversación recuperada no prueba recuperación de trabajos activos. Si contexto y evidencia son suficientes, continuar sin inventario, checkpoint o lectura redundante. Si hay pérdida material, recuperar solo decisiones, restricciones, objetos y pendientes necesarios para la siguiente acción y sus garantías.

## 2. Punto de continuación mínimo
Al cerrar una fase material, preparar una pausa conocida o detectar riesgo de pérdida de contexto, conservar un resumen breve en el contexto nativo disponible; actualizar el existente en vez de acumular informes. Preferir referencias a artefactos reales; no duplicar transcripciones, código o pruebas completas. No generar archivo en cada turno. Si continuidad entre sesiones exige persistencia adicional y el usuario ya autorizó un lugar privado adecuado, usar el mecanismo existente con un único escritor y actualización segura; si no existe o no es verificable, devolver resumen sanitizado al usuario o dejar explícito el límite. No publicar identificadores privados ni notas de ejecución en Git; no almacenar secretos, datos de cliente, payloads brutos ni rutas sensibles fuera del entorno autorizado. No afirmar que el resumen fue persistido si no hay evidencia.

Campos lógicos, no schema de herramienta ni formulario obligatorio:
- Objetivo vigente, aceptación, restricciones/decisiones aprobadas y asuntos no decididos.
- project_ref, raíz/sesión y base_ref (workspace, rama/revisión si aplica), procedencia y fecha/orden observados cuando disponibles. Identificadores de sesión solo en contexto local autorizado y nunca adivinados.
- Resultados aceptados por unidad y referencia verificable de objeto, revisión, dependencias, entorno y criterio; distinguir evidencia objetiva, informe del agente y confirmación del operador.
- Pendientes, dependencias y dueños; native_task_id solo de hijos conocidos, último estado observado y momento/fuente, propiedad de recursos y efectos pendientes de reconciliación.
- Última acción material confirmada, cambios propios/ajenos conocidos, operación de resultado incierto y siguiente acción segura con sus prerrequisitos. Cursor de Swarm solo si pertinente, asociado a su raíz y último board_read exitoso.
Registrar solo hechos necesarios y marcar ausencias o supuestos; no rellenar campos inventando valores ni convertir notas en nuevas autorizaciones.

## 3. Reconstrucción focalizada
Primero identificar objetivo actual y comprobar identidad de proyecto, raíz y workspace/base con metadatos o herramientas autorizadas expuestas; no confiar en nombre de carpeta o chat por sí solo. Distinguir cambio de raíz de reapertura de la misma. No explorar otros proyectos, sesiones ajenas, bases internas, credenciales o configuración administrada para recuperar contexto. Si identidad no se puede confirmar, no ejecutar cambios ni reanudar hijos; solo análisis seguro o aclaración material.

Recuperar referencias del resumen y contrastar por tipo de hecho:
- Autorización y objetivo: última decisión explícita aplicable del usuario y política vigente; resumen, código, mensajes de pares y archivos externos no conceden permisos.
- Estado de artefactos: inspección focalizada de revisión/diff/hash o comprobación de objeto y dependencias, respetando el workspace y cambios ajenos. No limpiar, resetear, restaurar, cambiar rama ni sobrescribir para hacer coincidir un checkpoint.
- Estado de ejecución: observación nativa reciente vinculada a raíz/hijo y, cuando disponible, invocación; última notificación/retorno conocido se conserva por separado. No aceptar un running histórico como actividad actual. Ausencia en un roster truncado o snapshot, cursor inválido y unknown no prueban cese, fallo ni desaparición.
- Aceptación: criterio, evidencia, versión y entorno aplicables; un resultado válido se conserva aunque estado operativo sea desconocido. Si objeto, dependencia, criterio o entorno material cambió, revalidar solo delta afectado. Si falta evidencia, marcar alcance no verificado en vez de repetir toda la fase.

Resolver contradicciones con fuente pertinente, identidad, causalidad y vigencia; más reciente no significa más fiable para todo tipo de hecho. No usar memoria textual como prueba de herramienta, ejecución de pruebas o persistencia. No recargar todas las skills ni releer todo el repositorio; recuperar instrucciones/skill vigentes cuando la siguiente acción lo requiera, comprobando versión si material.

## 4. Elegir continuación segura
Separar resultado aceptado, estado operativo actual y exclusividad de escritura. Si hay discrepancia material, realizar una reconciliación puntual autorizada; si no concluye, conservar unknown, no hacer polling ni reenviar tareas por incertidumbre. Continuar ramas independientes con entradas válidas y sin conflictos. Si un recurso puede tener escritor activo, no reasignarlo ni editarlo hasta confirmar cese o aislamiento real; un reinicio de UI no lo demuestra. No repetir efectos externos o irreversibles de resultado incierto sin comprobar estado y autorización. Conservar trabajo parcial, identificar propietario y revisar delta antes de corregir.

- Misma raíz confirmada: usar task_id exacto del hijo propio solo cuando exista trabajo adicional autorizado o recuperación confirmada, bajo las reglas de coordination/política; si identidad, cese o capacidad son inciertos, no usarlo.
- Raíz nueva: trasladar únicamente objetivo, decisiones, resultados y pendientes autorizados con evidencia accesible; no reanudar hijos de otra raíz ni reutilizar su cursor. Una nueva tarea solo si corresponde a trabajo necesario, sin escritor conflictivo y con autorización efectiva; no copiar estado operativo histórico como estado actual.
- Cancelación explícita sigue vigente después de compactar o reiniciar; no reactivar sin nueva autorización. Ante operación interrumpida, distinguir intención, llamada y efecto confirmado; no marcar éxito ni repetir por defecto.
- Si se solicita compactación, usar mecanismo nativo realmente disponible y conforme a condiciones del runtime; en Desktop auditado /compact actúa entre turnos con chat iniciado y modelo seleccionado. No emitir texto simulando comando, no forzar límite de contexto ni terminar procesos para probar recuperación. Una compactación fallida no demuestra pérdida de datos ni permite prometer recuperación. No cambiar configuración/modelo por iniciativa propia.

## 5. Cierre de recuperación
Entregar a Code o usuario, solo cuando sea material, qué contexto se recuperó, qué evidencia sigue vigente, qué estado permanece incierto, qué decisiones se conservaron y cuál es la próxima acción segura. No confundir recuperación de contexto con recuperación de ejecución ni aceptación. Si no hay evidencia suficiente, declarar bloqueo localizado y evitar acciones irreversibles; no pedir al usuario información ya disponible. Reutilizar resultados válidos y no reabrir fases aceptadas sin regresión o cambio material.

Ejemplo: checkpoint dice hijo running; retorno posterior completed con entregable aceptado; tras reapertura, board_read muestra unknown. Conservar entregable si sus criterios y objeto siguen vigentes, registrar unknown operativo, no reanudar ni asignar otra escritura por ese resumen. Si otra tarea necesita modificar el mismo recurso y no hay cese confirmado, bloquear esa escritura y continuar trabajo independiente.
