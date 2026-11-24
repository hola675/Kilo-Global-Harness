# Plan maestro
Versión del archivo: 0.5.0 | Última modificación: 2026-11-24

## Misión
Convertir Kilo Desktop en un equipo de ingeniería que interpreta objetivos, planifica, ejecuta, delega, integra, certifica y aprende, con intervención mínima del usuario dentro de la autorización. Diseñar desde cero, con experiencia y patrones de las investigaciones y la auditoría de código fuente; legacy es referencia histórica inmutable.

## Alcance 1.0
Windows, versión real de Kilo Desktop instalada (referencia auditada: Desktop 1.0.0 + CLI 7.8.27; no se afirma que sea el binario instalado ni la última versión), Code nativo, agentes especialistas, políticas globales, skills propias, integración dinámica de herramientas/MCP existentes, aprendizaje controlado, instalador y desinstalador selectivos, pruebas y documentación. No construir otro motor, chat, proveedor de modelos, servicio permanente, base vectorial, orquestador externo o interfaz Desktop salvo necesidad posterior demostrada.

## Entregables
1. Inventario reproducible de runtime y matriz de capacidades confirmadas/ausentes.
2. Política global breve y contratos de tareas/evidencia; adaptación al esquema real.
3. Equipo de especialistas definido por competencias, no jerarquía redundante.
4. Catálogo de skills originales con fuentes, activación, límites, procedimientos, verificaciones y evaluaciones.
5. Coordinación nativa, registro de estado mínimo solo cuando haga falta, recuperación y trabajo simultáneo.
6. Integración MCP de terceros y MCP propios condicionados a brechas comprobadas.
7. Team Learning con propuestas, pruebas, revisión, aprobación y control de versiones.
8. Paquete global reproducible, instalador idempotente, actualización, rollback, diagnóstico, desinstalación y guía de uso.
9. Certificación en Windows Desktop y pilotos de proyectos representativos; release 1.0.0.

## Reglas de decisión
Nativo primero > configuración > skill > herramienta existente > MCP/plugin propio. Un cambio debe reducir fricción o habilitar una capacidad comprobablemente ausente. Usar contrato/validación mecánica donde una instrucción no basta. No confundir instrucciones con límites efectivos de seguridad; no asignar permisos universales por comodidad.
Trabajo sencillo directo; tareas independientes delegadas; tareas dependientes ordenadas; riesgo alto revisión independiente. Concurrencia ajustada por evidencia, no por cantidad de agentes.
Toda ampliación debe tener dueño, necesidad, alternativas, coste, dependencias, alcance, prueba, fallback y criterio de retirada. Evitar solapamientos entre agentes, skills y MCP.

## Gestión
Roadmap por puertas, no por fechas inventadas. Cada fase tiene entregable, criterios de entrada/salida y estado. Revisar y actualizar estado solo con pruebas. Cambios de alcance/arquitectura se registran como decisiones breves; no multiplicar documentación repetitiva. La release no es una suma de archivos: requiere ejecución real y aceptación. La política de limpieza sin respaldo de componentes antiguos no se aplica automáticamente a futuras actualizaciones del nuevo Harness; para ellas se propone rollback selectivo y reversible, sujeto a aprobación.

## Decisiones tras auditoría de código
Fuente normativa para estas decisiones: [auditoría fijada](AUDITORIA-CODIGO-KILO-DESKTOP.md). Distinguir implementación estática, exposición en runtime y certificación funcional.
- Integración en el CLI empaquetado (kilo serve), no en otro motor ni mediante fork de Electron. Desktop, CLI y SDK son versiones independientes; registrar binario real, hash y versión.
- Code (id code, compatibilidad build) único líder del Harness; conservar modos nativos. Task, sesiones hijas, notificación background, Swarm, catálogo de skills, compactación, cola y gateway MCP son capacidades existentes, no componentes a reconstruir.
- Separar global XDG del perfil administrado Desktop. La primera instrucción global existente puede ocultar otras. F02 debe resolver rutas y F03/F04 demostrar carga efectiva y merge sin invadir archivos administrados.
- Profundidad inicial nativa 1: Code delega a hijos directos. No equivale a límite de concurrencia. Ampliar solo tras caso, autorización y evidencia; no fijar un máximo de motor sin medición.
- Permisos independientes por rol y sesión, techos heredados, guardas de mutación y MCP. La auditoría detectó sandbox de ejecución deshabilitado en nuevos chats de ese snapshot; no asumir confinamiento. Worktree, política y permisos no sustituyen aislamiento técnico.
- Priorizar herramientas desktop_* y nativas realmente expuestas; diferenciar plugin de motor, plugin de interfaz y MCP estándar. No acceder a tokens internos ni ASAR; no exigir plugin propio ni MCP de estado para v1 si no existe brecha.
- Modelos: arquitectura independiente del proveedor y modelo; selección nativa centralizada por el usuario. Un modelo común por defecto; opciones gratuitas y de pago autorizadas, sin sustituciones silenciosas.
- Team Learning: metaskill semántica y observaciones mínimas; usar resultados/eventos nativos, no monitor paralelo por defecto. Introducir activación de la skill solo cuando exista y se pruebe (F11).
- Evidencia de cierre: retorno task, estado UI done, conexión MCP y recepción de board no equivalen a verificación de resultado. Distinguir cada uno.

## Principio de resiliencia frente al modelo (decisión del operador)
GPT-6 Luna es provisional, no dependencia, modelo fijo ni requisito de instalación. El objetivo es reducir la degradación de calidad, coordinación y autonomía al cambiar de modelo, sin prometer equivalencia de capacidades.
- Separar identidad/competencias, selección de modelo, contratos y verificación. Admitir modelos gratuitos, de pago o por suscripción que el usuario autorice y el catálogo ofrezca; modelos locales compatibles como opción futura. El precio no determina automáticamente capacidad ni fiabilidad.
- Usar el mismo contrato verificable de entrada/salida, criterios de aceptación, propiedad de archivos y estado de tarea. Preferir comprobaciones deterministas (tests, lint, tipos, diff, hashes, esquemas) a la autoevaluación del modelo. Revisores independientes según riesgo; mismo modelo no implica independencia de errores, por lo que exigir evidencia objetiva.
- Adaptar granularidad de tareas, contexto, paralelismo y complejidad de instrucciones a capacidades observadas; no a marcas ni precios. Si falla una herramienta o aceptación, reducir alcance, corregir con evidencia, usar mecanismo nativo alternativo autorizado y registrar bloqueo si persiste. Acotar reintentos y escalamiento; no repetir sin hipótesis nueva ni cambiar modelo/coste sin autorización.
- Mantener invariantes de seguridad y calidad para todos los modelos. Si un modelo no cumple una capacidad esencial, restringir su uso a tareas compatibles o detener esa tarea. No degradar criterios para obtener PASS.
- F03.4E verifica selección central en laboratorio; F04/F05 consolidan configuración y contratos. F12 compara modelos representativos gratuitos/de pago solo cuando autorizados, con mismos fixtures, criterios y métricas observables (aceptación, errores, reintentos, herramientas, latencia, coste cuando observable). Evaluar robustez y brechas, no declarar compatibilidad universal.
- Detalle técnico en [integración Kilo](../integration/kilo/README.md); evidencia histórica en [laboratorio](../tests/F03-LABORATORIO.md). Sin router externo salvo brecha comprobada.
