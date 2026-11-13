# VECIDYA | Guía técnica del harness global V3

**Ámbito:** solo instalaciones globales en Windows. Nunca escribir configuración de Kilo dentro de repositorios individuales.

## Secuencia operativa

1. **DISCOVER** — determinar repositorio real, rama, `git status --porcelain`, README, dependencias y herramientas disponibles; identificar requisitos y límites.
2. **ROUTE** — escoger una skill especializada, las MCP necesarias y, si aporta valor, uno o dos subagentes de solo lectura; evitar agentes con objetivos idénticos.
3. **PLAN** — en tareas complejas, objetivos, alcance, criterios de aceptación, pruebas y riesgo; no duplicar archivos de instrucciones en el repo.
4. **BUILD** — cambios mínimos, reversibles y consistentes. TDD para funciones y defectos con pruebas posibles. No solapar ediciones concurrentes sobre los mismos archivos.
5. **VERIFY** — recoger comandos y códigos de salida reales; distinguir PASS/FAIL/NO EJECUTADO. Para Workers, además validar DEV/STAGING por URL real cuando corresponda.
6. **REVIEW** — diff, seguridad, rendimiento, contratos, datos sensibles, compatibilidad y documentación útil.
7. **GIT CLOSE** — usar ramas `work/*` para tareas no triviales. Partir de `main` sincronizada sin perder cambios locales. PR y CI si el repo lo exige; merge solo tras validación. Verificar `main` remota antes de eliminar únicamente la rama creada por la tarea.
8. **REPORT** — resultado, pruebas, commits/PR, riesgos, siguiente paso y rollback.

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
