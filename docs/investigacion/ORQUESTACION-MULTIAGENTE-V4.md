# Arquitectura: Kilo Global Harness V4 (implementación incremental)

**Objetivo:** agentes globales de Kilo, activación contextual, trabajo paralelo seguro, evidencia y control de contexto/costo. **Estado:** V4.0–V4.2 implementados; V4.3 añade base SQLite global y propuestas bajo demanda. El enrutamiento por coste real, plugin observador y reuniones programadas siguen pendientes. Ningún proyecto recibe configuración Kilo local.

## Motor y capas

```text
Usuario en VS Code/Kilo
        |
  VX Dispatcher (global, selecciona objetivo, alcance, presupuesto)
        |---- Skill Registry (búsqueda y ranking; on-demand)
        |---- MCP Router (solo herramientas disponibles para esa tarea)
        |---- Agent Registry (capability, condiciones, permisos, artefacto esperado)
        |---- Context Manager (memoria grafo fresca + evidencia de fuentes)
        |
  Workflow DAG + Task Scheduler [carga <= límites, sin duplicidad]
       |                     |                       |
   Explore (R/O)        Security (R/O)         Research (R/O)  EN PARALELO
       \                     |                    /
         Plan + contratos de interfaces aprobados
                         |
            Implementer (UN SOLO WRITER)
                         |
       +-----------------+------------------+
       |                 |                  |
     Review R/O        Test R/O           Docs R/O
       +-----------------+------------------+
                         |
              Integrador + QA final
                         |
         PR / CI / merge -> main -> cleanup
```

R/O = solo lectura. El dispatcher no debe disparar todos los roles por inercia. Dedupe por `capability`, `file_scope` y evidencia. Roles no deben votar sobre los mismos hechos sin diversidad de método.

## Compatibilidad Kilo nativa

- `task(background: true)`: consultas de lectura independientes, prompts pequeños; devuelve respuesta al padre; no crea worktree.
- `task` foreground: tareas secuenciales dependientes de un resultado previo.
- **Kilo Swarm**: `board_post`/`board_read` solo para comunicación de padres/descendientes de una misma sesión; no coordina distintas sesiones del Agent Manager.
- **Agent Manager**: sesiones paralelas y worktrees separados para tareas de escritura aisladas. Cada worktree exige rama propia y almacenamiento adicional. No usar el modo avanzado de edición paralela mientras la regla del usuario exija UNA sola rama temporal.
- **Plugin global Kilo** (fase posterior): puede añadir tools, interceptar ejecuciones y llevar telemetría básica; evitar instalarlo antes de pruebas y medir compatibilidad con context-mode.

## Registro de capacidades (esquema propuesto)

```yaml
id: vx-security-reviewer
role: subagent
capabilities: [security-review, secrets-risk, auth-review]
when: [auth-change, dependencies-change, risky-diff]
writes: false
tools: [read, grep, git-diff]
output: {format: structured-findings, severity: required, evidence: required}
limits: {calls: bounded, retry: 1}
source: {origin: upstream, license: check, upstream_sha: pin}
```

*El YAML es un contrato del futuro catálogo del harness, no un archivo de configuración reconocido directamente por Kilo.* El generador debe producir agentes nativos Markdown con frontmatter documentado y pruebas. No inferir APIs inexistentes.

## Equipos compuestos (selección contextual)

| Tarea | Paralelos de lectura | Escritura | Validaciones |
| --- | --- | --- | --- |
| Error de backend | explorer, debugger, reviewer de contratos | backend developer | tests, regression, security si hay auth |
| Frontend premium | UX, accesibilidad, performance | frontend developer | visual QA, a11y, build, testing navegador |
| Cloudflare Workers | workers, observability, security | worker developer | lint, typecheck, DEV URL, compatibilidad bindings |
| Base de datos | schema reviewer, riesgos de migración | DB engineer | plan de rollback, migración de prueba, tests |
| Refactor grande | domain reviewer, test analyst | refactor engineer | diff de contrato, regresiones, build |
| Diseño + ImageGen | art director, UX strategist | imagegen solo si se solicita imagen; otro writer único | dimensiones, relevancia, cuota consciente |
| Revisión PR | reviewer, security, test engineer | sin escritor en fase review | findings vinculados a diff |

## Modos de paralelismo

1. **STRICT (predeterminado):** `main` + una `work/<tarea>`; lectores concurrentes, un único escritor. Se integra y elimina la rama temporal solo tras verificarse `origin/main`. Respeta tu preferencia actual.
2. **ISOLATED (solo autorización explícita):** trabajo realmente independiente en worktrees con ramas auxiliares `work/<tarea>-lane-1`, `lane-2`; gate de conflictos y CI; integrar una por vez; borrar ramas auxiliares al cierre. Requiere relajar temporalmente la restricción de una sola rama activa.
3. **EXTERNAL (futura fase opcional):** usar adapters de CLI externos solo cuando estén instalados, autenticados y autorizados; no se presuponen cuotas cruzadas ni compatibilidad de sesiones.

## Control de coste sin degradar calidad

- Enrutamiento por tarea: consulta trivial = 0 subagentes, normal = 1-2, compleja = max 3 lectores concurrentes inicialmente.
- Seleccionar modelo disponible por rol, no fijar IDs no confirmados; registrar tokens solamente cuando el proveedor reporte uso real.
- Skills y MCP **por demanda**, memoria con índice fresco; contexto entregado a cada agente = objetivo, rutas, interfaces y criterios, no transcript completo.
- Límite de iteraciones y reintentos acotado para evitar loops; no interpretar `steps` como tokens.
- Revisar con prompts/fixtures repetibles: calidad, tasa de errores, duración, llamadas a herramientas, gastos declarados, divergencia de roles.
- Regresar a modo single-agent si la delegación añade costo sin beneficios medibles.

## Condiciones de incorporación (próxima implementación)

1. Resolver y auditar las **12 definiciones mezcladas** JSON/Markdown por propiedades; no borrar por nombre sin comparar precedencia.
2. Instrumentar pruebas e inventario de los **19 steps = 10,000,000**, reajustar con benchmark y rollback.
3. Crear catálogo global versionado y validador de rutas/licencias, con origen por commit.
4. Añadir router y 5 perfiles piloto: `vx-researcher`, `vx-security-reviewer`, `vx-tester`, `vx-frontend-specialist`, `vx-workers-specialist`.
5. Probar parejas de agentes, no importación masiva. Evaluar 3 tareas representativas frente a single-agent y conservar logs sin secretos.
6. Piloto aislado de context-mode con Kilo, no activarlo sin evaluar colisión de hooks con otras extensiones.
7. Integrar CI y workflow de promoción de skills. No activar autoaprendizaje o actualización automática antes de pruebas.

**Política:** solo global, AutoApprove conservado, Git `main` permanente, ningún MCP nuevo/skill externo activo por esta documentación.


## Incremento V4 implementado (registro + orquestacion nativa)

Se crea un registro JSON de agentes/perfiles globales, cinco subagentes de solo lectura, `/vx-equipo` y dos scripts PowerShell: seleccion de equipo SIN efectos y validacion de registro. Los perfiles cubren general, backend, frontend, cloudflare, database, security, refactor, design y docs. No hay llamadas automaticas a modelos ni importacion masiva de codigos externos.

El validador comprueba rutas VX, identidades, frontmatter, limites de iteraciones, separacion de escritores y referencias de perfiles. El selector **solo recomienda**, no lanza agentes; Kilo `task(background: true)` es el mecanismo de ejecucion real. CI Windows prueba instalacion, seguridad de configuracion y restauracion. No se resuelven en este incremento los 12 agentes preexistentes JSON/MD ni los 19 limites `steps=10000000`; deben tratarse por compatibilidad y medicion.

La instalacion V4 usa manifiesto 4.0.0 y permite restaurar respaldos 3.0.0 de V3 sin cambiar los archivos privados JSONC, AutoApprove o MCP. El modo de multi-escritura en worktrees auxiliares sigue desactivado hasta consentimiento del operador.
