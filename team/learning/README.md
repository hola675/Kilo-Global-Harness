# Team Learning — diseño
Versión del archivo: 0.1.0 | Última modificación: 2026-11-24

Basado en la investigación Task Observer, no una copia ni reactivación de VX.
Detectar correcciones, aciertos, tareas repetidas, pérdida de contexto, fallos de routing, herramientas no disponibles y complejidad inútil. Distinguir incidencia local de patrón reutilizable.
Code consolida hallazgos de subagentes al finalizar tareas/fases. Un escritor por sesión raíz; sesiones independientes no mezclan registros. Consultar solo observaciones relevantes. Almacenamiento local privado, fuera de worktrees y del repositorio; límites de retención/volumen definidos y probados F11. Sin secretos ni datos crudos, sin sincronización automática.
Pipeline: detectar→clasificar/deduplicar→proponer delta→staging→evaluar baseline/candidato→revisión independiente→aprobación→activar/verificar. No autoelevar permisos, publicar ni instalar cambios globales. Si una regla se incumple repetidamente, valorar control mecánico y no añadir texto sin fin. Posibilidad de consolidar, simplificar y retirar. Si falla el almacenamiento o la metaskill, devolver nota al líder y continuar tarea principal.
Plugin observador opcional solo si el runtime nativo no da evidencia suficiente; prueba aislada de hooks, no interceptar ni modificar solicitudes o respuestas. No inferir éxito de session.idle.
