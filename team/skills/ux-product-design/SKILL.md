---
name: ux-product-design
description: "Diseña y mejora recorridos de producto, navegación, formularios y flujos de trabajo: tareas reales, jerarquía de información, estados, decisiones, prevención de errores y recuperación accesible. Usar al definir o cambiar materialmente cómo una persona cumple un objetivo en una interfaz. No cargar para ajustes de estilo aislados, corrección textual sin efecto de interacción, requisitos sin diseño de flujo ni cambios internos sin impacto de usuario."
metadata:
  version: "0.1.0"
  last_modified: "2026-11-28"
---

# Diseño de producto orientado a tareas

## Alcance
Lumen convierte el objetivo y las restricciones aceptadas en una interacción utilizable; Code conserva alcance y aceptación. No inventes investigación, roles, endpoints, permisos, capacidades offline ni reglas de negocio. No fijes tecnología, marca, estética o nueva biblioteca por defecto. El diseño no autoriza implementación ni operaciones externas. Para trabajo sencillo decide localmente dentro del contrato; no impongas un documento, prototipo, reunión o delegación por pantalla.

## 1. Identificar la tarea real
- Determina quién actúa, qué intenta conseguir, qué información necesita para decidir, con qué frecuencia y en qué condiciones (dispositivo, entrada, conectividad, tiempo, capacidad y contexto operativo cuando importen). Identifica el resultado que puede observar, no solo el clic que realiza.
- Reutiliza contrato, interfaz, navegación, patrones y resultados existentes pertinentes. Distingue observación verificada, hipótesis de diseño y dato desconocido. Una persona ficticia no es evidencia de investigación. Si una incógnita cambia autoridad, coste, seguridad o regla de negocio, eleva la pregunta concreta a Code; continúa partes independientes. Para decisiones reversibles justificadas, declara supuesto y criterio de comprobación.
- Identifica la tarea primaria, tareas secundarias y puntos de abandono o error. Prioriza por impacto y frecuencia observados cuando existan; no simules métricas ni priorización basada en usuarios no investigados.

## 2. Diseñar el recorrido mínimo completo
- Delimita punto de entrada, precondiciones, pasos necesarios, información y acciones por estado, salida y forma de retomar. Compara mantener lo existente, simplificar o introducir un nuevo patrón; elige el menor cambio que satisfaga el objetivo sin ocultar información decisiva.
- Organiza navegación y contenido por tareas y significado para el usuario, con posición, retorno, acciones y consecuencias comprensibles. No confundir profundidad visual con jerarquía funcional. Agrupa información relacionada, revela opciones avanzadas cuando sean pertinentes, evita recorridos que obliguen a recordar datos disponibles. Ajusta densidad, controles y atajos a novatos, uso repetido y dispositivos; no escondas acciones esenciales tras gestos exclusivos.
- Solicita solo datos necesarios. Usa etiquetas persistentes, unidades, ejemplos y restricciones antes del error; orden de lectura, teclado y foco coherentes. Distingue obligatorio/opcional y permite revisar o corregir cuando proceda. No borres entradas válidas por errores de otra parte ni persistas información sensible sin contrato. Coordina textos y estados con Ágora si aporta valor.
- Para tareas de consecuencias importantes, elige revisión previa, corrección o reversión efectiva según contrato y riesgo; no inventes deshacer ni confirmación para cada acción trivial. Haz inequívoco qué objeto, importe, destino o alcance se afecta. En interfaces industriales no modifiques autoridad de operación, interlocks ni estados de alarma.

## 3. Especificar estados, transiciones y recuperación
Diseña los estados realmente alcanzables: inicial, vacío, carga, edición, validación, éxito, rechazo, desconexión, datos desactualizados, sin permiso, conflicto, resultado incierto o recuperación cuando apliquen. Para flujo con persistencia, latencia o efectos consulta [contrato de interacción](references/interaction-contract.md). Para cambio local basta describir estados afectados.
- Cada transición material tiene evento, precondición, autoridad que confirma el resultado, información visible, acciones permitidas y salida segura. No conviertas una espera, timeout, cierre de pantalla o respuesta parcial en éxito, fallo definitivo o cancelación. No expongas detalles sensibles en errores.
- Diferencia dato inválido corregible, operación no autorizada, indisponibilidad técnica y resultado incierto. Conserva entradas seguras, muestra el siguiente paso apropiado y ofrece acceso a estado confirmado si existe. No presentar control deshabilitado como enforcement ni prometer reintento seguro, cancelación, sincronización u operación offline sin contrato.
- Evita doble envío y reintentos ciegos: la UI puede proteger la interacción, pero requiere garantía de dominio para evitar duplicados. Si falta reconciliación, impide que la UI induzca una segunda operación con efecto; deriva a Code la dependencia de contrato y mantén el resultado pendiente. No ejecutar efectos reales para demostrar un diseño.

## 4. Validar experiencia y entregar
- Formula tareas representativas y observaciones concretas: completar, corregir, regresar, distinguir resultado y recuperar sin perder datos autorizados. Para cada riesgo material verifica alternativas válidas y negativas; revisa estados y rutas de salida antes de pulir presentación. Criterios de accesibilidad y diseño visual no se sustituyen por esta skill; usa procedimientos pertinentes si disponibles, sin cadena obligatoria.
- Evalúa lo construido con herramientas y entorno autorizados. La inspección heurística genera hipótesis, no resultados de usuarios; prototipo no acredita persistencia ni integración. Si se autoriza investigación con personas, usa tareas neutrales, consentimiento y datos ficticios o debidamente protegidos; registra observación y limitación sin inventar participantes. No recopiles información personal por defecto.
- Para misión de diseño devuelve flujo/diagrama o contrato breve, estados y acciones, decisiones y supuestos, criterios observables, dependencias y límites. Para cambio de implementación dentro de alcance entrega el incremento, no solo el diseño. Distingue revisión propia de independiente; conserva identidad del objeto para Veritas/Bastión cuando el riesgo lo requiera. Reporta qué se observó, qué no se probó y qué bloquea aceptación; no certifiques toda la experiencia por una captura, build o prueba parcial.
