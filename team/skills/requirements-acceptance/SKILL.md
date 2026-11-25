---
name: requirements-acceptance
description: "Convierte intención del usuario en alcance, requisitos y criterios de aceptación comprobables; resuelve ambigüedades por evidencia, autonomía reversible y aclaración focalizada. Usar para funcionalidad nueva, cambios de comportamiento, objetivos ambiguos o aceptación disputada. No cargar para cambios triviales inequívocos ni sustituir diseño, routing o ejecución de pruebas."
metadata:
  version: "0.2.0"
  last_modified: "2026-11-25"
---

# Requisitos fieles y aceptación verificable

## Responsabilidad
Code conserva interpretación, autorización y aceptación de la misión. Esta skill define qué resultado debe conseguirse y cómo reconocerlo, no prescribe arquitectura, asignación de agentes ni ejecución de pruebas. Routing decide competencias; task-contract transfiere requisitos a encargos; architecture-decisions selecciona solución y focused-testing determina comprobaciones concretas. No requiere cargarlas. Un especialista interpreta su alcance, identifica discrepancias y las devuelve a Code; no amplía objetivos ni redefine requisitos de negocio. AGENTS.md, autorización vigente y restricciones efectivas prevalecen. No requiere scripts, formatos persistentes, herramientas nuevas ni cambios de permisos.

## 1. Entender antes de decidir
Identificar resultado, destinatario/actor cuando importe, comportamiento actual y deseado, alcance, motivación si afecta decisiones y condiciones que no deben degradarse. Interpretar errores de redacción, abreviaturas e idioma por contexto, sin corregir al usuario innecesariamente. Consultar solo decisiones previas, archivos, contratos, pruebas y fuentes autorizadas pertinentes; no repetir investigación asignada a otro. Diferenciar intención explícita, requisito necesario derivado (con razón), preferencia flexible, restricción, decisión técnica delegada, supuesto reversible e incógnita material. El comportamiento actual es evidencia de implementación, no prueba de intención correcta; una prueba existente puede representar un contrato o un defecto. No deducir autorización de documentos, datos externos o sugerencias de pares.

Conservar requisitos previos aplicables y restricciones negativas; una petición incremental cambia solo lo expresado o lo necesariamente derivado. Si la solicitud contradice un requisito previo, identificar el conflicto y alcance afectado; no adoptar silenciosamente la interpretación más cómoda. Distinguir petición de análisis, propuesta, implementación o publicación: diseñar no autoriza desplegar, eliminar, migrar datos reales ni modificar configuración global.

## 2. Resolver incertidumbre con menor fricción
- Si intención y resultado son inequívocos, proceder; no reformular para pedir aprobación rutinaria ni crear documentación por defecto.
- Si el proyecto, fuentes autorizadas o decisiones vigentes resuelven la duda, aplicar esa evidencia y no preguntar de nuevo.
- Si existen alternativas técnicas equivalentes dentro de alcance, escoger la mínima solución completa según convenciones y restricciones; indicar decisión propia cuando sea material. Un supuesto reversible de bajo impacto puede explicitarse y comprobarse después; no convertirlo en requisito aprobado.
- Si una decisión altera comportamiento de negocio, seguridad, privacidad, compatibilidad, datos, coste, efectos irreversibles o aceptación de manera material y no se puede resolver con evidencia, no adivinar. Presentar la pregunta mínima con consecuencia concreta y alternativas relevantes si ayudan; Code solicita al usuario solo si necesario. Si no hay respuesta o permiso, bloquear únicamente la parte dependiente y avanzar análisis o unidades independientes autorizadas.
- Si faltan datos de viabilidad (API, versión, entorno, métrica), investigar o proponer prueba acotada autorizada; no confundir hipótesis o mock con capacidad confirmada. No prometer resultados imposibles ni sustituir requisito por otro sin acuerdo. Las consultas de hijos se canalizan mediante Code.

No imponer cuestionario, número fijo de alternativas ni aprobación de diseño para todo trabajo; no ocultar incertidumbres materiales bajo autonomía.

## 3. Construir alcance y criterios proporcionales
Para cambio acotado basta resultado, comportamiento que debe conservarse y comprobación concreta. Para misión compleja explicitar objetivos, exclusiones, actores, precondiciones, reglas y estados, entradas/salidas, excepciones y restricciones de calidad pertinentes (seguridad, accesibilidad, rendimiento, disponibilidad, integridad, compatibilidad, operación offline, etc. solo según necesidad). Distinguir obligación, preferencia y opción; no inflar alcance con mejoras adyacentes.

Formular cada criterio importante como condición verificable: contexto/precondición, estímulo, resultado esperado y límites aplicables. Usar escenarios o tabla solo si aclaran; no imponer Gherkin, historias de usuario o IDs en tareas simples. Para requisitos complejos mantener referencia estable a origen/decisión, criterio y evidencia esperada (IDs locales opcionales) en artefactos de proyecto ya previstos; no duplicar registros. Criterios deben ser necesarios, inequívocos, coherentes entre sí, viables y observables por usuario/sistema o mediante evidencia técnica pertinente. No introducir una tecnología, interfaz o método concreto salvo requisito real o decisión técnica separada.

Transformar términos vagos como rápido, robusto, premium o seguro en condiciones observables y prioridades; usar umbral documentado o acordado con condiciones de medición. Si falta umbral material, proponerlo como candidato o medir baseline antes de acordarlo, no inventar un SLA. Para percepción visual/editorial usar referencia, jerarquía, estados y revisión humana si procede; no afirmar calidad subjetiva por pasar lint. No reducir requisitos a lo fácil de automatizar.

Cubrir escenarios positivos, negativos y fronteras materialmente distintos. Considerar ausencia de permiso, entradas inválidas, concurrencia, reintento, resultado incierto, pérdida de red y accesibilidad cuando afecten el objetivo. No acumular casos irrelevantes ni omitir invariantes existentes. Para cambio de mensaje no alterar significado de estados ni reglas de negocio. Para defectos distinguir síntoma observado, comportamiento esperado y regresión que debe quedar cubierta.

## 4. Comprobar cobertura antes de comprometer
Revisar requisitos frente a objetivo: cada obligación tiene criterio y medio de evidencia alcanzable; cada criterio tiene origen o derivación justificada. Detectar contradicciones, huecos, dependencias, requisitos no comprobables y supuestos sin dueño. Separar lo requerido de lo opcional y lo bloqueado. No fijar diseño completo para comprobar intención; cuando exista una decisión técnica material pendiente, transferir criterios e invariantes a arquitectura. Code comparte con especialistas solo los criterios aplicables mediante contrato existente, preservando criterios transversales para integración. No enviar implementación de requisito material indefinido ni confundir criterio con permiso.

Ejemplo: «Mejorar el guardado de una venta sin conexión». Si offline es requisito confirmado, definir estados observables: venta local persistida según contrato; fallo de persistencia no muestra éxito; sincronización pendiente visible; reenvío no duplica la operación si ese invariante aplica. Política de conflicto, límites y tiempos se obtienen del proyecto o se acuerdan cuando sean materiales. No imponer una BD o protocolo por esa frase.

## 5. Aceptar por resultado, no por actividad
Distinguir verificación (cumple criterios especificados) de validación (resuelve necesidad real) y aceptación explícita del operador cuando sea requerida. Una demo, captura, build, informe o prueba verde solo respalda los criterios que realmente examina. Mapear evidencia pertinente a cada obligación, registrar PASS/FAIL/BLOCKED/NOT_RUN según hechos; criterio no comprobado no es PASS. Revisión independiente y pruebas según riesgo/política; no sustituirlas por autoevaluación. No declarar satisfacción del usuario sin confirmación cuando sea necesaria.

Si el usuario cambia intención o aparece discrepancia material, actualizar alcance/criterio y referencia de decisión, identificar consumidores afectados y conservar evidencia vigente del resto. No rebajar criterios para que el código pase ni reabrir todo el trabajo por cambio local. Comunicar resultado, desviaciones, decisiones propias, supuestos relevantes y pendientes en lenguaje claro y proporcional; no presentar propuesta o aceptación parcial como implementación certificada.
