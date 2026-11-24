# Team Learning — diseño
Versión del archivo: 0.2.0 | Última modificación: 2026-11-24

Basado en la investigación Task Observer, no una copia ni reactivación de VX.
Detectar correcciones, aciertos, tareas repetidas, pérdida de contexto, fallos de routing, herramientas no disponibles y complejidad inútil. Distinguir incidencia local de patrón reutilizable.
Code consolida hallazgos de subagentes al finalizar tareas/fases. Un escritor por sesión raíz; sesiones independientes no mezclan registros. Consultar solo observaciones relevantes. Almacenamiento local privado, fuera de worktrees y del repositorio; límites de retención/volumen definidos y probados F11. Sin secretos ni datos crudos, sin sincronización automática.
Pipeline: detectar→clasificar/deduplicar→proponer delta→staging→evaluar baseline/candidato→revisión independiente→aprobación→activar/verificar. No autoelevar permisos, publicar ni instalar cambios globales. Si una regla se incumple repetidamente, valorar control mecánico y no añadir texto sin fin. Posibilidad de consolidar, simplificar y retirar. Si falla el almacenamiento o la metaskill, devolver nota al líder y continuar tarea principal.
Plugin observador opcional solo si el runtime nativo no da evidencia suficiente; prueba aislada de hooks, no interceptar ni modificar solicitudes o respuestas. No inferir éxito de session.idle.

## Integración revisada
El motor auditado ya compone contexto, gestiona compactación, sesiones hijas, notificaciones y estados; reutilizar esas señales, sin asumir que todas son accesibles al agente. No construir otro observador de ciclo ni persistencia MCP antes de F11. F11 prueba primero metaskill y almacenamiento mínimo; F10 decide luego si una brecha restante justifica adaptador. Activación global tras descubrimiento y prueba de sesión nueva; no editar perfil administrado Desktop. Hook técnico solo si la evidencia falta, y distinto de plugin de interfaz. Estado UI done o retorno Task no prueba aceptación.
