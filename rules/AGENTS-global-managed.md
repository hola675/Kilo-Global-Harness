# VECIDYA GLOBAL HARNESS V3.0 — preferencia vigente

Esta seccion global sustituye indicaciones anteriores de este mismo AGENTS.md si entran en conflicto con las preferencias siguientes. Idioma: espanol; nombres de codigo segun el repositorio.

- GLOBAL ONLY: agente, skill, MCP, workflow, reglas de Kilo y ajustes de Kilo se instalan SOLO bajo HOME. NO crear carpetas `.kilo`, `.agents`, `.kilocode`, `.claude` ni ficheros `AGENTS.md` o `kilo.jsonc` dentro de ningun proyecto para configurar Kilo. Se permite editar codigo, pruebas y documentacion del proyecto cuando la tarea lo exige.
- AUTONOMIA: el usuario desea conservar AutoApprove. Ejecutar autonomamente lecturas, ediciones ordinarias, tests, commits y flujo de ramas Git dentro de repositorios autorizados y tareas solicitadas. NO interpretar AutoApprove como autorizacion para exponer secretos, borrar datos ajenos, ejecutar comandos destructivos, desplegar a produccion o cambiar infraestructura.
- GIT: `main` es la unica rama PERMANENTE deseada. Para tareas no triviales, partir de `main` actualizada, crear UNA rama temporal `work/<tema>`, implementar y verificar; integrar mediante PR o merge permitido por las protecciones del repo; comprobar resultado de `main` antes de borrar SOLO la rama temporal propia (local/remota) si es seguro. No borrar otras ramas, no hacer force push, no usar `reset --hard` ni rebase destructivo de ramas compartidas. Si GitHub impide merge/borrado, informar en lugar de eludir politicas.
- CALIDAD: primero inspeccionar estado Git, archivos relevantes y pruebas; cambios minimos, TDD cuando aplique; lint/typecheck/tests/build; nunca afirmar PASS sin salida real; revisar diff y cambios no relacionados.
- CONTEXTO: usar busqueda focalizada/Codebase Memory solo con indice valido, evitar dumps masivos, activar skills por necesidad, delegar subagentes sobre tareas independientes, y resumir descubrimientos antes de compactar.
- SEGURIDAD: no copiar tokens a chat, archivos del repositorio, logs o MCP; no reescribir configuraciones privadas desde ZIP sanitizados. Produccion, permisos IAM, firewall, migraciones destructivas y borrados masivos exigen autorizacion especifica.
- IMAGEGEN: utilizar el MCP global solo para solicitudes con salida grafica explicita, despues de comprobar las herramientas disponibles; las pruebas de CLI no demuestran acceso del cliente. Nunca generar imagenes de prueba ni consumir cuota solo para diagnosticar conectividad. Guardar fuera del repo salvo solicitud concreta.
- ACTUALIZACIONES: no instalar o actualizar skills/MCP/agentes automaticamente; versiones fijadas y cambios revisados. No desactivar por defecto actualizaciones de seguridad de VS Code ni de Windows.
- CIERRE: informar cambios, pruebas reales, resultado Git, riesgos y capacidad de rollback. Si no hay conectividad, separar los hechos verificados de los pendientes.

Para tareas complejas invocar `vx-engineering-harness`; no cargar todas las skills ni todos los MCP simultaneamente.
