# Laboratorio F03 — primer caso nativo
Versión del archivo: 0.1.0 | Última modificación: 2026-11-24
Estado: procedimiento propuesto; NOT_RUN. Fuente: auditoría Desktop 1.0.0 y CLI 7.8.27. Crear directorio nuevo fuera de proyectos reales y del Harness; sin credenciales, MCP externos ni cambios globales. Usar una sesión nueva de Desktop con Code nativo. Elegir explícitamente modelo autorizado; si se pretende usar suscripción, comprobar distintivo BYOK, proveedor y coste de una solicitud inocua antes de ejecutar tareas adicionales. No fijar modelo en agente hasta verificar ID y cobertura.

## Preparación
Crear un directorio nuevo con .kilo/agents/team-lab-reader.md, .kilo/skills/team-lab-marker/SKILL.md, AGENTS.md y fixture.txt. Marcadores independientes, no anticiparlos en prompt. Agent mode: subagent; permisos declarados de lectura/skill y denegación de edición/bash/task; son hipótesis de configuración, comprobar en ejecución. No modificar configuración global ni perfil administrado. La carpeta no contiene datos reales; si Desktop requiere Git, inicializar repositorio local sin remoto.

## Primera prueba
1. Abrir la carpeta como workspace, seleccionar Code, elegir modelo autorizado. Enviar solicitud inocua; comprobar uso del proveedor/coste en panel Kilo antes de ampliar prueba.
2. Pedir marcador de instrucciones raíz y carga real de team-lab-marker; registrar valor devuelto y evidencia de llamada skill. Pedir invocación foreground de team-lab-reader para leer fixture.txt y devolver su contenido. Registrar identidad del hijo, herramienta y retorno; no aceptar simulación por Code.
3. Pedir al hijo una edición inocua de fixture y registrar si permiso efectivo deniega/oculta herramienta; comprobar que contenido no cambió. No solicitar vías alternativas. Registrar NOT_RUN si no existe invocación.
4. Posteriormente F03.2–F03.5 prueban background con dos hijos, board, permisos y recuperación. No certificar por este primer caso. Conservar solo evidencia sanitizada, sin transcripciones ni datos de cuenta.
Retirada: cerrar workspace de laboratorio y eliminar solo su directorio nuevo tras autorización. No borrar worktrees existentes.
