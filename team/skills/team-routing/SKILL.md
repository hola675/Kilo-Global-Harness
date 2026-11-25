---
name: team-routing
description: "Decide si Code debe ejecutar, delegar o coordinar una misión de ingeniería según competencias, acoplamiento, riesgo, dependencias y coste. Usar al repartir trabajos no triviales o replantear un reparto fallido. No cargar para lecturas conocidas, respuestas directas o cambios locales sin necesidad especializada ni riesgo material."
metadata:
  version: "0.3.0"
  last_modified: "2026-11-25"
---

# Routing de ingeniería proporcional

## Contrato
Code es dueño de la misión, la decisión de reparto y la integración. Esta skill decide quién debe intervenir y cuándo una unidad es delegable; team-task-contract define entradas y handoff; team-coordination gobierna ejecución. No requiere cargarlas. Aplicar AGENTS.md y los contratos vigentes. Si la carga un hijo, solo recomienda a Code, sin subdelegar. No modifica permisos, modelo, configuración ni archivos por sí sola; no requiere red ni comandos.

## 1. Clasificar antes de explorar
Extraer objetivo, aceptación, alcance permitido, incertidumbre material y garantías que no pueden degradarse. No leer por anticipado el objeto que analizará otro salvo prerrequisito. Si el usuario restringe delegación, coste, fuentes o herramientas, respetarlo. Resolver supuestos reversibles; consultar solo decisiones materiales no inferibles o autorizaciones ausentes.

Proponer unidades por **resultado coherente**, no por número de archivos, longitud del prompt ni cantidad de agentes disponibles. Para cada unidad identificar resultado verificable, competencia, entradas, escrituras y dependencia de otros resultados. Eliminar unidades sin aportación distinta.

## 2. Elegir el menor nivel suficiente
- N1 directo: tarea acotada de bajo riesgo, sin necesidad material de especialista o revisión; ejecutar sin informe de routing ni llamadas extra.
- N2 especialista: competencia dominante, contexto separado útil o contraste independiente acotado; Code conserva integración.
- N3 equipo paralelo: varios resultados útiles que pueden avanzar sin esperar decisiones ajenas ni modificar el mismo recurso.
- N4 multifase: dependencias reales, integración por etapas o puertas de revisión material; ordenar el camino crítico y desbloquear unidades listas.

Dos decisiones prevalecen sobre la cantidad de trabajo:
- Mantener una unidad cohesionada si dividirla multiplica cambios de contrato, escrituras compartidas o transferencias de contexto. Una investigación difícil de una sola causa puede merecer N2, no una multitud de hijos.
- Dividir cuando los resultados tengan criterios propios y entradas estables, y la separación permita avanzar independientemente o contrastar un riesgo real. Una revisión independiente sí puede examinar el mismo objeto congelado sin convertirse en segundo escritor.

Comparar coste cualitativo de llamadas, contexto, espera, integración y retrabajo frente al valor de especialización y concurrencia. No estimar tokens, precios, velocidad ni límites del motor sin evidencia. No serializar por costumbre ni paralelizar por apariencia. No degradar garantías por ahorrar llamadas.

## 3. Elegir competencia por resultado
Consultar catálogo nativo disponible y descripciones de los agentes, no asumir su disponibilidad por nombre. Usar estos contrastes semánticos cuando correspondan al equipo instalado:
| Competencia primaria | Resultado que la justifica | Límite frente a otra competencia |
|---|---|---|
| Atlas / arquitectura | Fronteras, contratos transversales, decisión estructural | Nexo para regla de negocio acotada; Prisma para persistencia. |
| Lumen / frontend | Interacción, accesibilidad, interfaz y estados visibles | Ágora para texto aislado; Nexo para autoridad del servidor. |
| Nexo / backend | Servicio, autorización funcional, transiciones, integración API | Bastión contrasta amenazas; Prisma define invariantes de datos. |
| Prisma / datos | Modelo, restricciones, consultas, migración y transacciones | Nexo consume el contrato; no duplicar dueño de persistencia. |
| Forja / plataforma | Entorno, build, entrega, CI y automatización operativa | Veritas evalúa evidencia; no duplicar implementación. |
| Faro / investigación | Evidencia primaria, alternativas o incógnita técnica decisiva | No delegar búsqueda por rutina si evidencia vigente basta. |
| Veritas / calidad | Criterios, regresión o revisión independiente de un objeto | El constructor corrige; Bastión revisa riesgos de seguridad. |
| Bastión / seguridad | Frontera de confianza, acceso, exposición y amenazas | No sustituye implementación ni toda la revisión funcional. |
| Ágora / editorial | Claridad, fidelidad de mensajes, documentación y contenido | No redefine semántica de negocio ni interacción técnica. |

La tabla no es una lista de llamadas obligatorias. Para solapamientos, escoger un propietario del resultado y un contraste focalizado solo si aporta una garantía distinta. Evitar consultar varios roles para la misma decisión sin necesidad.

## 4. Puerta de preparación
Antes de cada Task, verificar:
- Resultado útil, dueño y alcance no duplicado.
- Entradas reales accesibles al hijo dentro de lo autorizado; incluir contexto concreto o referencia exacta. No asumir herencia completa de la conversación.
- Dependencias satisfechas, escrituras compatibles y capacidad/autorización efectiva.

Si falta una entrada, mantener planned/blocked; no enviar una tarea que solo puede esperar. Preparar criterios de revisión anticipadamente es un resultado distinto de revisar el objeto. Para revisar, entregar versión o texto concreto, criterios y supuestos. Un resultado completed/BLOCKED no satisface dependencias. Si el trabajo de dos escritores afecta el mismo objeto, unificar o secuenciar; contrato no equivale a bloqueo técnico.

## 5. Ejecutar la decisión
Code usa Task nativa con los parámetros expuestos en su sesión; no inventa category, load_skills ni otros argumentos de herramientas externas. Proporcionar objetivo, entrada, aceptación, alcance y dependencias en el prompt. Usar foreground para prerrequisito inmediato; background cuando haya trabajo independiente útil. No sobrescribir el modelo autorizado, ni delegar a un rol sin capacidad. Si falta una herramienta o especialista, evaluar una alternativa nativa autorizada con la misma garantía; si no existe, reducir alcance o declarar bloqueo, sin simular revisión ni eludir deny.

En N2–N4 basta comunicar el reparto y su razón en términos útiles al usuario; no crear planes persistentes por rutina. En cierre, comprobar llamadas reales, retornos, integración y revisión necesaria. Resolver únicamente el nodo bloqueado con entradas corregidas; si el objeto cambia materialmente, revisar el delta según riesgo. No declarar cierre completo si una garantía obligatoria sigue pendiente. No afirmar simultaneidad sin evidencia temporal.

## Contrastes rápidos
- Lectura conocida o etiqueta aislada: N1; no cargar skill ni convocar equipo por rutina.
- Diseño de permisos, transacciones y mensajes: N3/N4 según entradas; contrastar riesgos sobre diseño concreto, no sobre criterios solos.
- Defecto transversal con causa y archivos compartidos: una investigación cohesionada, N1/N2 según riesgo; separar revisión posterior, no multiplicar escritores.
- Dos implementaciones independientes con contrato estable: N3, propietarios exclusivos; un único consumidor dependiente espera su entrada.
- Prohibición de delegar: respetarla, declarar límite de independencia si necesario.

## Evidencia de utilidad
Comparar criterios satisfechos, duplicación, bloqueos evitables, llamadas y tiempos observables con política sola. No declarar mejora por cargar la skill ni por aumentar el número de hijos. Investigación y evaluación: docs/INVESTIGACION-SKILLS.md y tests/F06-SKILLS.md, rutas del repositorio de desarrollo, no dependencias runtime.
