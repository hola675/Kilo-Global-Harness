---
name: team-routing
description: "Selecciona ejecución directa, especialista o equipo para misiones de ingeniería con competencias distintas, entregables independientes, dependencias o revisión de riesgo. Usar al decidir el reparto de una misión no trivial; no cargar para una lectura, respuesta breve o cambio local de bajo riesgo."
metadata:
  version: "0.1.0"
  last_modified: "2026-11-25"
---

# Selección proporcional del equipo

## Objetivo y límites
Code decide el reparto y conserva integración y aceptación. Esta skill ayuda a decidir, no sustituye AGENTS.md, las herramientas nativas, los permisos ni los contratos. No crea agentes, no cambia el modelo ni requiere red, scripts o archivos auxiliares. Si la invoca un especialista, solo puede recomendar un reparto a Code.

## Procedimiento

1. Extrae el resultado solicitado, las restricciones y los criterios verificables. Identifica si existe una decisión de producto no inferible o una autorización ausente; no conviertas todo supuesto en pregunta.
2. Distingue competencias materiales de temas mencionados. Para cada posible delegación identifica un resultado concreto que no duplique el trabajo de Code u otro hijo. Si no aporta valor, elimínala.
3. Selecciona el nivel de menor complejidad suficiente:
   - N1: Code directamente; alcance acotado y riesgo bajo, sin contribución especializada material.
   - N2: una competencia dominante o contraste independiente acotado.
   - N3: varios resultados independientes, con entradas disponibles y escrituras compatibles.
   - N4: dependencias reales, integración por etapas o revisión necesaria de riesgos materiales.
4. Define el camino crítico antes de despachar. Una tarea de revisión requiere el objeto concreto, versión o texto y criterios; preparar criterios por adelantado es una tarea distinta. Solo despacha nodos listos. No impongas una cantidad fija de hijos ni serialices tareas independientes.
5. Selecciona por responsabilidad efectiva y catálogo nativo disponible, no por nombre de modelo ni palabras aisladas. Para fronteras de competencias, elige un dueño del resultado y pide contraste solo si modifica una decisión o reduce riesgo. Usa únicamente Task real si disponible y autorizada. Si falta, comunica el alcance no cubierto; no simules revisión.
6. Transfiere objetivo, entrada concreta, alcance, restricciones, resultado verificable y dependencias. Utiliza las reglas de propiedad y handoff de la política vigente. No leas por rutina lo que asignas a otro. En trabajo exclusivamente conceptual, las entradas pueden viajar como texto en el prompt sin leer o escribir archivos.
7. Comprueba retornos y decisiones antes del cierre. Una tarea terminal bloqueada no satisface su dependencia. Recupera solo el nodo afectado aportando la entrada faltante; si cambia materialmente el objeto revisado, vuelve a contrastar el delta cuando el riesgo lo exija. Si no puedes completar la revisión, declara aceptación parcial o bloqueo.

## Contrastes de decisión

| Situación | Decisión esperada y motivo |
|---|---|
| Leer un archivo conocido y devolver su contenido | N1; no enviar una Task ni cargar esta skill por rutina. |
| Diseño de permisos, transacciones, recuperación y mensajes | N3/N4 según dependencias; separar contribuciones útiles, integrar y contrastar riesgos sobre diseño concreto. |
| Cambiar una etiqueta sin alterar significado ni contrato | N1 si alcance y riesgo son bajos; no convocar arquitectura por asociación. |
| Revisar un cambio sin acceso al objeto | Mantener pendiente la revisión; preparar criterios si aporta valor, sin simular aprobación. |
| Usuario exige trabajo directo o prohíbe delegar | Respetar restricción; indicar límite de independencia si corresponde. |

## Salida y comprobación

Para una misión compleja comunica brevemente nivel, entregables asignados, dependencias materiales y revisión necesaria. No generes un documento de planificación por defecto. En el cierre contrasta tareas realmente invocadas, resultados recibidos, bloqueos, decisiones incorporadas y alcance verificado. No califiques concurrencia sin evidencia de intervalos. N1 no necesita reporte de routing separado.

## Referencias de diseño

Síntesis original de la política del Harness 0.17.0 y los casos F05-B-R/RQ; la selección dinámica y el despacho son capacidades del agente, no un scheduler nuevo. Formato contrastado el 2026-11-25 con https://agentskills.io/specification y https://kilo.ai/docs/customize/skills . Cargador de referencia MIT: https://github.com/Kilo-Org/kilocode/blob/03a6f07d053cd7e6aa88fa1e258e93510335259f/packages/opencode/src/tool/skill.ts . No se incorpora código de terceros. Comportamiento y precedencia del host pendientes de evaluación F06.
