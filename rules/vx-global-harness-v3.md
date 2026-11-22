# VECIDYA | Guía técnica del harness global V3

**Ámbito:** solo instalaciones globales en Windows. Nunca escribir configuración de Kilo dentro de repositorios individuales.

## Secuencia operativa

1. **DISCOVER** — determinar repositorio real, rama, `git status --porcelain`, README, dependencias y herramientas disponibles; identificar requisitos y límites.
2. **ROUTE** — escoger una skill especializada, las MCP necesarias y, si aporta valor, uno o dos subagentes de solo lectura; evitar agentes con objetivos idénticos.
3. **PLAN** — en tareas complejas, objetivos, alcance, criterios de aceptación, pruebas y riesgo; no duplicar archivos de instrucciones en el repo.
4. **BUILD** — cambios mínimos, reversibles y consistentes. TDD para funciones y defectos con pruebas posibles. No solapar ediciones concurrentes sobre los mismos archivos.
5. **VERIFY** — recoger comandos y códigos de salida reales; distinguir PASS/FAIL/NO EJECUTADO. Para Workers, además validar DEV/STAGING por URL real cuando corresponda.
6. **REVIEW** — diff, seguridad, rendimiento, contratos, datos sensibles, compatibilidad y documentación útil.
7. **GIT CONTINUOUS SYNC + CLOSE** — una rama `work/*` propia por tarea no trivial, creada desde `main` sincronizada. Varias ramas de agentes pueden coexistir solamente con worktrees/propietarios aislados. Si `origin/main` avanza, cada rama activa recibe una tarea idempotente `RECONCILE_REQUIRED`: parar en un punto seguro, conciliar `main` en la rama propia, ejecutar pruebas focalizadas y reanudar; los conflictos, worktrees sucios y permisos bloquean sin resolución automática. El detector/dispatcher aún es diseño, no scheduler activo. PR/CI/revisión antes de merge; verificar `main` remota y retirar solo la rama propia. Fuente: `docs/VX-TEAM-GIT-RECONCILIATION-V1.md`.
8. **REPORT** — resultado, pruebas, commits/PR, riesgos, siguiente paso y rollback.

## Certificación viva y deuda de tests

Regla global para todos los agentes VX y Dev Team:

1. Antes de crear un test, identificar la **invariante actual** que debe demostrar.
2. Buscar si ya existe un test activo para esa misma invariante.
3. Elegir explícitamente una acción:
   - `UPDATE` — el test existente sigue siendo el oráculo correcto y debe actualizarse;
   - `REPLACE` — el test nuevo sustituye completamente al anterior;
   - `ADD` — solo cuando existe un riesgo/oráculo realmente distinto.
4. Un test nuevo no se conserva junto al anterior por historia o por versión.
5. Si `REPLACE`, ejecutar primero el reemplazo. Solo después de PASS real se retira el test/gate supersedido.
6. La historia se conserva en Git, PR, changelog, registry y evidencia de certificación, no en suites activas acumulativas.
7. Los tests deben ser focalizados al cambio. Ampliar cobertura únicamente si cambió una invariante transversal.
8. CI source, smoke Windows y certificación runtime son evidencias distintas; no repetir una suite completa en varios gates.
9. Cada suite directa `test_*.py` debe tener un único gate propietario o pertenecer a un manifest canónico.
10. Nunca declarar PASS de una prueba no ejecutada ni conservar un test sin una invariante vigente asociada.

Al cerrar una tarea, el coordinador debe poder responder:
`invariante → test vigente → acción UPDATE/REPLACE/ADD → evidencia → test supersedido retirado o justificación para conservarlo`.


## MCP y memoria

- `codebase-memory-mcp`: comprobar servidor, proyecto, frescura y cobertura; validar hallazgos contra el código. Nunca tratar un grafo obsoleto como verdad.
- `memory`: persistir únicamente decisiones estables, sin secretos ni información personal.
- `context7`/`microsoft-learn`: documentación de API/versión, buscar fragmentos concretos.
- `github`/`cloudflare`: lectura o escritura según autorización/credenciales válidas; no asumir que el JSON implica conexión MCP.
- `playwright`: pruebas reales en navegador si está conectado.
- `imagegen`: generación gráfica únicamente si la tarea necesita imágenes y las herramientas están disponibles; la prueba de CLI no acredita la conexión del cliente. No crear assets en repositorios por defecto ni iniciar generaciones automáticas de validación que consuman cuota.

## Contexto/costo

- `steps` es un máximo de iteraciones, NO tokens. Evitar bucles infinitos; detectar fallos repetidos.
- Leer rutas y símbolos exactos, usar búsqueda e indexado antes de abrir archivos enormes.
- Delegar tareas acotadas y devolver resúmenes con referencias; no duplicar todo el contexto del padre.
- No utilizar skills con disparador universal de observación en cada mensaje; activar retrospectiva expresamente.
- No cambiar modelos ni proveedores sin conocer los identificadores realmente disponibles.

## Límites

- Prohibidos force push, borrados de ramas ajenas, despliegues automáticos a producción y modificaciones de infraestructura sin consentimiento específico.
- El operador controla los tokens de acceso, nunca el repositorio GitHub del harness.
- No instalar ni actualizar skills/MCP de manera silenciosa.


## Coordinación VX Dev Team V2.1 — contrato actual

El equipo activo es `vx-dev-team` visible (**VX Dev Team**), con 17 hijos ocultos, 57 Skills del paquete unificado y permisos del propio agente, sin reinstalar jerarquías antiguas. Solo `main` es permanente; para integrar usar rama temporal y PR/CI/revisión. En tareas triviales, evitar fan-out.

Para un proyecto amplio: el líder determina contratos y rutas exactas, despacha **primero** la wave de llamadas reales `task(background: true)` independientes si el host admite el parámetro, y continúa **sin esperar** con lectura de archivos estables, planificación de próximas dependencias, riesgos o revisión de trabajos ya concluidos. Hasta 4 hijos, 2 writers en archivos literales no solapados con `EXACT_FILES`, y un único escritor Git por worktree. Una dependencia no verificada bloquea el consumidor; las tareas `BLOCKED` con ID activo retienen capacidad y rutas. La cola es solo registro privado y no ejecuta modelos, watcher ni scheduler.

Kilo Swarm ofrece `board_read/post` para el líder y seis builders cuando esté efectivamente expuesto, solo para hitos, sin secretos ni derechos de ejecución; analistas read-only siguen sin Board. Ante ausencia de background o Swarm, usar foreground y/o `task_result`, sin afirmar simultaneidad. La barrera de integración requiere fin de escritores, diffs, pruebas focales, revisión y evidencia real; el líder **nunca** edita archivos reservados mientras trabajen hijos. `AGENTS.md` global canónico: `rules/AGENTS-global-managed.md`; manual `docs/VX-DEV-TEAM-AUTOPILOT-V2.md`.

## Changelog
- 2026-11-21, contrato V2.1: sustituida coordinación V4 histórica de un solo escritor con límites actuales y control de progreso.

