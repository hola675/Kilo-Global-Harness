# Plan de scripts Windows
Versión del archivo: 0.2.0 | Última modificación: 2026-11-24

F02: Diagnosticar-KiloTeam.ps1 (solo lectura, versiones, paths, presencia de configuraciones sin secretos, procesos, herramientas y salida JSON sanitizada). F03: fixture de PoC aislado y verificación manual de sesión. F13: Administrar-KiloTeam.ps1 con modos Diagnostico, Simular, Instalar, Verificar, Actualizar, Desinstalar y Restaurar. No hay scripts ejecutables aquí todavía. PowerShell 7, rutas con espacios y Unicode, códigos de salida documentados, sin admin por defecto, sin sobrescribir archivos no administrados, pruebas idempotentes y protección de junctions. No utilizar legacy como instalador.

## Alcance actualizado F02
Inventariar binario CLI empaquetado (diferente de PATH), versión Desktop/CLI y hash, rutas globales y perfil Desktop, presencia/hash de instrucciones, posibles duplicados y fallbacks de worktree. No volcar líneas de comando completas, variables de entorno completas, tokens ni archivos auth; no arrancar/terminar procesos ni escribir configuración. Marcar capacidades no observables como NOT_RUN y trasladar a F03 las pruebas de invocación. F03 fixture de laboratorio con marcador benigno, eliminación selectiva autorizada y evidencia del motor real.
