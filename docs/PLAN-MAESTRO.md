# Plan maestro
Versión del archivo: 0.2.0 | Última modificación: 2026-11-24

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
- Modelos: respetar resolución nativa y configuración autorizada; no imponer overrides de modelo/proveedor/variant dinámicos por coste o complejidad.
- Team Learning: metaskill semántica y observaciones mínimas; usar resultados/eventos nativos, no monitor paralelo por defecto. Introducir activación de la skill solo cuando exista y se pruebe (F11).
- Evidencia de cierre: retorno task, estado UI done, conexión MCP y recepción de board no equivalen a verificación de resultado. Distinguir cada uno.
