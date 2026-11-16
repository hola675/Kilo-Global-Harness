# VX Evolution — Política de permisos, autonomía y colaboración de agentes

**Fecha:** 2026-11-15 · **Versión:** 0.1.0-draft · **Estado:** SOLO DISEÑO. No cambia agentes, frontmatter, permisos, Kilo, HOME, AutoApprove, MCP, scheduler, ramas de código ni bases operativas.

## Fundamento y niveles de permisos

La definición en Kilo admite permisos `allow`, `ask` y `deny` por herramienta; `task` puede delimitar qué agentes se invocan, y existen modos `primary`, `subagent` y `all`. Las reglas de patrones pueden tener precedencia: verificar el comportamiento efectivo en la versión del runtime antes de declarar protección. Kilo `task` comparte el directorio del padre; Agent Manager puede crear sesiones con worktrees de Git aislados. Esta distinción es esencial para escritores simultáneos. Referencias: [Custom Subagents](https://kilo.ai/docs/customize/custom-subagents), [Custom Modes](https://kilo.ai/docs/customize/custom-modes), [Agent Manager](https://kilo.ai/docs/automate/agent-manager), [Agent Permissions](https://kilo.ai/docs/customize/agent-permissions).

**Autonomía operativa no equivale a nivel profesional.** Un agente de rol “líder” no queda acreditado como senior y no recibe permisos automáticamente. El alias «Yoan» del líder IA no es el operador humano ni una firma de aprobación.

| Nivel de autonomía | Qué permite | Puertas |
| --- | --- | --- |
| **A0: OBSERVE** | Lectura acotada, evidencia, análisis | Secretos y directorios fuera del alcance bloqueados |
| **A1: PROPOSE** | Diseñar planes, tests, diffs simulados y tareas para otros | Sin ejecutar cambios; consulta externa según permisos concretos |
| **A2: WORKTREE_WRITE** | Implementar y ejecutar pruebas en **un worktree autorizado y aislado**, bajo permisos de Kilo | Petición específica/consentimiento, ramas y archivos separados, bloqueo de producción y HOME |
| **A3: INTEGRATE** | Revisar, reunir resultados, resolver conflictos, abrir PR | CI, revisión independiente, reglas de merge, no autoaprobación |
| **A4: PUBLISH** | Instalar/alterar Pack VX global | **NO DISPONIBLE** hasta auth real, rollback, evidencia, consentimiento separado; `approval_granted=false`/`apply_supported=false` |

## Situación real actual vs objetivo propuesto

| Alias / ID | Capacidades actuales declaradas | Autonomía vigente no certificada | Propuesta futura |
| --- | --- | --- | --- |
| **Yoan / `vx-integrador`** | Primary, coordinación, `read/glob/grep/skill: allow`. Sus `edit/bash/task` no están fijados explícitamente en el archivo y pueden heredarse | **NO_VERIFICADO** en runtime; no suponer permiso efectivo de escritura | A1 y A3; A2 solo cuando actúe como único escritor de su worktree autorizado. Delegación a IDs VX acotada y probada |
| **Daniela / `vx-frontend-adviser`** | Subagente lectura; `edit/bash/mcp/task/agent_manager: deny` | A0–A1 declarados | **Candidata** a A2 frontend en worktree aislado, tras versión de permisos y prueba; no concedido hoy |
| **Rafael / `vx-test-analyst`** | Subagente lectura; `edit/bash/mcp/task/agent_manager: deny` | A0–A1 declarados | **Candidato** a A2 tests en rama separada; jamás considerar su informe de tests como ejecución |
| **Sofía / `vx-researcher`** | Subagente lectura; `edit/bash/mcp/task/agent_manager: deny` | A0–A1 declarados | Mantener lector por defecto; consulta de investigación externa solo si está permitida |
| **Valentina / `vx-security-reviewer`** | Subagente lectura; `edit/bash/mcp/task/agent_manager: deny` | A0–A1 declarados | Independencia y negación de aprobación/publicación; excepciones estrictas |
| **Lucas / `vx-inspector`** | Subagente lectura; `edit:deny`, Bash solo `git status/diff/log` según glob declarado | A0–A1 declarados; comandos efectivos NO_VERIFICADOS | Auditor independiente, nunca writer de los cambios que certifica |
| **Mateo / `vx-workers-adviser`** | Subagente lectura; `edit/bash/mcp/task/agent_manager: deny` | A0–A1 declarados | Candidato futuro a A2 en proyecto de pruebas, sin despliegue Cloudflare |

**Implementación paralela desde el Pack inicial, sin promover subagentes todavía:** Kilo `code` nativo en **sesiones independientes de Agent Manager y worktrees separados**, con un único escritor por worktree, bajo supervisión de Yoan. Esta es una **capacidad objetivo**, no una tarea activada. Cuando Daniela/Rafael u otro agente VX demuestren capacidad y se autorice nueva versión con escritura acotada, podrán sustituir o acompañar esos escritores por tareas independientes. Kilo Code nativo sigue siendo propiedad de Kilo: VX solo coordina su uso para tareas solicitadas; no gobierna su código ni versión.

## Matriz de herramientas por rol — target, no cambios activos

| ID / alias | Read | Edit | Terminal | MCP | Task | Agent Manager | HOME | Merge / deploy / instalación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Yoan | allow con exclusión de secretos | ask en worktree de tarea | ask comandos revisados | ask por servicio cuando proceda | allow solo VX listados, según configuración efectiva | ask para crear worktree aislado | deny sin autorización excepcional | prohibido automáticamente |
| Daniela | allow limitado | deny (futuro ask en worktree) | deny (futuro ask para tests frontend) | deny | deny | deny | deny | deny |
| Rafael | allow limitado | deny (futuro ask para tests) | deny (futuro ask comando de prueba) | deny | deny | deny | deny | deny |
| Sofía | allow limitado | deny | deny | deny | deny | deny | deny | deny |
| Valentina | allow limitado | deny | deny | deny | deny | deny | deny | deny |
| Lucas | allow limitado | deny | allow solo status/diff/log de Git si coincide patrón, demás deny | deny | deny | deny | deny | deny |
| Mateo | allow limitado | deny (futuro ask en worktree) | deny | deny | deny | deny | deny | deny |

**Restricciones universales:** ningún agente puede acceder a secretos por mera relación de jefatura, alterar `kilo.jsonc`, AutoApprove, permisos, modelos, providers, MCP o conexiones sin autorización propia. Ningún alias permite suplantar al operador; delegar no transfiere autorización. No habilitar `A4` porque el contrato V4.7.1 aún devuelve `approval_granted=false`, `apply_supported=false`. Los patrones `deny` de lectura de secretos necesitan validación real; no garantizan que un usuario no exponga un secreto por otro canal.

## Reglas de simultaneidad y acceso a Git

### Perfil STRICT, disponible como política actual
- `main` única rama permanente; una rama temporal `work/*`, un escritor, hasta 3 subagentes **lectores** concurrentes.
- Para cambios pequeños, críticos o con archivos compartidos; no requiere coordinación Git distribuida.

### Perfil PARALLEL_WORKTREES, **objetivo no habilitado**
- El operador deberá autorizar explícitamente la **excepción por proyecto/tarea** a “una sola rama temporal a la vez”; `main` sigue siendo la única permanente.
- Yoan crea/coordina un `work/*` por línea independiente, cada una en worktree aislado. Máximo inicial sugerido **2 escritores simultáneos** más lectores, ajustable tras medir capacidad real del equipo y recursos.
- Cada escritor obtiene contrato exclusivo: `task_id`, `assigned_agent`, `worktree`, `branch`, `base_sha`, `allowed_paths`, `blocked_paths`, `inputs`, `output_contract`, `acceptance_tests`, `requires`, `risk`. Nunca dos escritores sobre el mismo conjunto de archivos o migración compartida.
- Dependencias técnicas estrictas `depends_on` forman DAG; comunicaciones bidireccionales `collaborates_with` sí pueden formar ciclos, sin otorgar privilegios.
- Subagentes lanzados con `task(background:true)` comparten working tree: **solo lectura para ellos**. Swarm solo conecta una sesión y sus descendientes; **no** es bus garantizado entre sesiones independientes de Agent Manager.
- Intercambio entre worktrees mediante contratos/versiones, artefactos redactados y commits/PR vinculados. Yoan publica resumen de API/cambio sin secretos; consumidores se sincronizan cuando el contrato está estable, nunca mediante escritura concurrente del mismo archivo compartido.
- Los worktrees no se fusionan entre sí automáticamente: Yoan reúne commits o PR en orden de dependencias, revalida tests de integración, CI y revisión independiente. Conflictos => STOP, serialización de ese segmento o rediseño de límites.
- El merge a `main` y eliminación de ramas solo tras autorización prevista y CI PASS; no force push ni reset de cambios ajenos.
- **Nunca** activar por una simple petición conceptual de usar paralelismo; requiere prueba en repo desechable, permisos verificados y confirmación sobre tareas/espacios concretos.

## Facultades futuras por promoción

Una “promoción” puede ampliar responsabilidad o especialización sin elevar permisos. La autorización de `edit`, `bash` o `agent_manager` es una **decisión adicional e independiente** respaldada por diff, pruebas en Kilo y rollback. Un nuevo cargo no puede cambiar el YAML del agente padre ni su permiso en Kilo. Para `seniority`: registrar `SIN_EVALUAR` hasta que existan benchmarks ciegos con complejidad, regresiones, resultados de ejecución, evaluación independiente y coste cuando se mida. Prohibidos ascensos por autoinforme, antigüedad ficticia o número de conversaciones.

**No configurar modelos ni tokens por nombre humano; usar el proveedor/modelo ya autorizado por usuario.** Evaluar coste y latencia real antes de aumentar paralelismo.

## Fuentes

- https://kilo.ai/docs/customize/custom-subagents
- https://kilo.ai/docs/customize/custom-modes
- https://kilo.ai/docs/customize/agent-permissions
- https://kilo.ai/docs/automate/agent-manager
- `agents/vx-*.md`, `registry/vx-agent-registry-v4.json`
